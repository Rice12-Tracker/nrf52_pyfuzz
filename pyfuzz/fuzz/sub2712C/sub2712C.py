from emulator import Emulator
from unicorn.arm_const import *
import argparse
parser = argparse.ArgumentParser(description="Test harness for sub_28430.bin")
parser.add_argument(
        "input_file",
        type=str,
    help="Path to the file containing the mutated input to load",
)
parser.add_argument(
    "-t",
    "--trace",
    default=False,
    action="store_true",
    help="Enables debug tracing",
)
args = parser.parse_args()
emu = Emulator('data/samsung_tag1.flash.bin', 0x0)
input_fanme=args.input_file

reg_data={}
reg_data[UC_ARM_REG_R0]=0x2001fc7c          
reg_data[UC_ARM_REG_R1]=0x0                 
reg_data[UC_ARM_REG_R2]=0x2001fb6c          
reg_data[UC_ARM_REG_R3]=0x1
reg_data[UC_ARM_REG_R4]=0x0                 
reg_data[UC_ARM_REG_R5]=0x1a                
reg_data[UC_ARM_REG_R6]=0x1                 
reg_data[UC_ARM_REG_R7]=0x2001fc7c          
reg_data[UC_ARM_REG_R8]=0x200086d6          
reg_data[UC_ARM_REG_R9]=0x20008689          
reg_data[UC_ARM_REG_R10]=0x0
reg_data[UC_ARM_REG_R11]=0x0
reg_data[UC_ARM_REG_R12]=0x2001fb68          
reg_data[UC_ARM_REG_SP]=0x2001fb58          
reg_data[UC_ARM_REG_LR]=0x286dd             
reg_data[UC_ARM_REG_PC]=0x2712c             
reg_data[UC_ARM_REG_XPSR]=0x61000026          
reg_data[UC_ARM_REG_FPSCR]=0x0
reg_data[UC_ARM_REG_MSP]=0x2001fb58

mem_data={}

ram_fname='data/sub_2712c_sram.bin'
exits=[0x27182,0x271BC]

def place_input_callback(uc, input, persistent_round, data):
    if len(input)>20+4+0x100 or len(input)<20+4:
        return False
    uc.mem_write(reg_data[UC_ARM_REG_R2],input[:20])
    uc.reg_write(UC_ARM_REG_R3,int.from_bytes(input[20:24],'little'))
    uc.mem_write(0xdead0000,input[24:])

protect=[(537000768, 537000792)]
emu.start(reg_data,mem_data,ram_fname,input_fanme,exits,place_input_callback,protect)