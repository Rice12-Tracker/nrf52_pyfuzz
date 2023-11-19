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
reg_data[UC_ARM_REG_R0]=0x2001fcac          
reg_data[UC_ARM_REG_R1]=0x20008c08          
reg_data[UC_ARM_REG_R2]=0x33a6d             
reg_data[UC_ARM_REG_R3]=0x3ee64             
reg_data[UC_ARM_REG_R4]=0x1f4               
reg_data[UC_ARM_REG_R5]=0x43de0             
reg_data[UC_ARM_REG_R6]=0xe000e000          
reg_data[UC_ARM_REG_R7]=0x4c                
reg_data[UC_ARM_REG_R8]=0x20008f08          
reg_data[UC_ARM_REG_R9]=0
reg_data[UC_ARM_REG_R10]=0
reg_data[UC_ARM_REG_R11]=0
reg_data[UC_ARM_REG_R12]=0x20002a5c          
reg_data[UC_ARM_REG_SP]=0x2001fca0          
reg_data[UC_ARM_REG_LR]=0x37257             
reg_data[UC_ARM_REG_PC]=0x33a6c             
reg_data[UC_ARM_REG_XPSR]=0x21000026          
reg_data[UC_ARM_REG_FPSCR]=0
reg_data[UC_ARM_REG_MSP]=0x2001fca0          
reg_data[UC_ARM_REG_PSP]=0
reg_data[UC_ARM_REG_PRIMASK]=0
reg_data[UC_ARM_REG_BASEPRI]=0
reg_data[UC_ARM_REG_FAULTMASK]=0
reg_data[UC_ARM_REG_CONTROL]=0

mem_data={}
ram_fname='data/sub_33A6C_sram.bin'

exits=[0x33BA6,0x33A92]
def place_input_callback(uc, input, persistent_round, data):
    if len(input)!=16+208:
        return False
    uc.mem_write(reg_data[UC_ARM_REG_R0],input[:16])
    uc.mem_write(reg_data[UC_ARM_REG_R1],input[-208:])

emu.start(reg_data,mem_data,ram_fname,input_fanme,exits,place_input_callback)