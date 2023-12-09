from unicorn import *
from unicorn.arm_const import *
from capstone import *
from capstone.arm import *
from unicornafl import *

from collections import OrderedDict
import struct

monitor=[]#"MSP","XPSR","CPSR","CONTROL","APSR","IPSR","EPSR"]
mreg={}
for reg in monitor:
    mreg[reg]=[(0,0)]

RAM_START_ADDRESS = 0x20000000
RAM_SIZE = 0x40000
NRF52840_REGISTERS = {}
NRF52840_PERIPHERALS = {}
# NOTE: you'd need to handle mrs & msr properly in 
# firmware running on top of a RTOS
INSTRUCTIONS_TO_SKIP = []#"vmsr"]
RADIO_INT_RETURN = False

class VectorTable(OrderedDict):
    def __repr__(self) -> str:
        str = ""
        for key, value in self.items():
            str += key + ":" + hex(value) + "\n"
        return str

def get_uc_aligned_size(length):
    if length % (1024) == 0:
        return length
    return 1024*(length // 1024) + 1024

def skip_instr(mn, uc, address, size):
    #print("[!] skipping %s instruction" %mn)
    uc.reg_write(UC_ARM_REG_PC, (address + size) | 1)

def parse_vector_table(content):
    vector_table = VectorTable({
        "initial_sp" : 0,
        "reset_handler": 0,
        "nmi_handler": 0,
        "hardfault_handler": 0,
        "mgnmem_handler": 0,
        "busfault_handler": 0,
        "usefault_handler": 0,
        "reserved1": 0,
        "reserved2": 0,
        "reserved3": 0,
        "reserved4": 0,
        "svc_handler": 0,
        "dbgmon_handler": 0,
        "reserved5": 0,
        "pendsvc_handler": 0,
        "systick_handler": 0,
        "wdtirq_handler": 0,
        "radioirq_handler": 0
    })
    i = 0
    for name in vector_table.keys():
        vector_table[name] = struct.unpack('<I', content[i:i+4])[0]
        i += 4
    return vector_table


class Emulator:
    def __init__(self, fw_path, base_addr) -> None:
        self.uc = Uc(UC_ARCH_ARM, UC_MODE_ARM + UC_MODE_THUMB)
        self.uc.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_M4)
        self.func_stack=[]
        self.funcs=1
        self.lr = 0
        self.protect =[]
        
        self.cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
        self.cs.detail = True
        self.base_addr = base_addr
        self.met_branch=False
        self.marked=[]
        self.handler=False
        # setup flash      
        vector_table = None
        self.fw_size = None
        with open(fw_path, 'rb') as fp:
            content = fp.read()
            self.fw_size = len(content)
            self.vector_table = parse_vector_table(content)
            # map flash memory
            size = get_uc_aligned_size(len(content))    
            self.uc.mem_map(base_addr, size)
            self.uc.mem_write(base_addr, content)
        # setup SRAM and map peripherals
        self.uc.mem_map(RAM_START_ADDRESS, RAM_SIZE)
        self.uc.mem_map(0xf0000000, 0x1000)
        self.uc.mem_map(0xe0000000, 0x10000)
        self.uc.mem_map(0x10000000, 0x10000)
        self.uc.mem_map(0x40000000, 0x40000)
        self.uc.mem_map(0x50000000, 0x1000)

        # special value for EXC_RETURN
        self.uc.mem_map(0xfffff000, 0x1000)

        # input
        self.uc.mem_map(0xdead0000, 0x1000)

        # setup uc hooks
        self.uc.hook_add(UC_HOOK_INTR, self.uc_intr_cb)        
        self.uc.hook_add(UC_HOOK_BLOCK, self.uc_mem_block_cb, begin=0xfffff000, end=0xffffffff)
        self.uc.hook_add(UC_HOOK_BLOCK, self.uc_dec, begin=0x23288+4, end=0x23288+8)
        #self.uc.hook_add(UC_HOOK_MEM_WRITE, self.uc_mem_cb)
        
        
    
    def start(self,reg_data,mem_data,ram_fname,input_fanme,exits,place_input_callback,protect=None):
        if protect:
            self.protect=protect
            prot_min=min([_[0] for _ in protect])
            prot_max=max([_[1] for _ in protect])
            self.uc.hook_add(UC_HOOK_MEM_WRITE, self.uc_mem_cb, begin = prot_min, end = prot_max)
        # subscribe to TASKS_RXEN envet from radio
        self.uc.reg_write(UC_ARM_REG_MSP, self.vector_table['initial_sp'])
        self.uc.reg_write(UC_ARM_REG_PC, self.vector_table['reset_handler'])
        
        with open(ram_fname,"rb") as f:
            sram_data=f.read()
            #assert len(sram_data)==RAM_SIZE
            self.uc.mem_write(RAM_START_ADDRESS, sram_data)
        for reg,val in reg_data.items():
            self.uc.reg_write(reg, val)
        for addr,val in mem_data.items():
            self.uc.mem_write(addr,val)
        
        
        #self.uc.emu_start(self.uc.reg_read(UC_ARM_REG_PC)+1, exits[1], 600 * UC_SECOND_SCALE , 0)
        uc_afl_fuzz(uc=self.uc, input_file=input_fanme, place_input_callback=place_input_callback, exits=exits)
        
    def uc_intr_cb(self, uc, exc_no,user_data):
        pass
        #print("exception",exc_no)

    def uc_mem_block_cb(self, uc, address, size, data):
        interrupt_return(uc)
    
    def uc_code_cb(self, uc, addr, size, user_data):
        pass
    
    def uc_dec(self, uc, address, size, data):
        input_data=uc.mem_read(0xdead0000,0x100)
        uc.mem_write(uc.reg_read(UC_ARM_REG_R2),input_data)
        uc.reg_write(UC_ARM_REG_PC,0x232E8+1)
    
    def uc_mem_cb(self, uc, access, address, size, value, user_data):
        for prot in self.protect:
            if address+size<prot[0] or prot[1]<=address:
                continue
            uc.mem_write(0xdeadbeef,b'dead')