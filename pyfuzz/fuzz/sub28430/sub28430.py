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
reg_data[UC_ARM_REG_R0]=0x20008d00
reg_data[UC_ARM_REG_R1]=0x2001fc7c
reg_data[UC_ARM_REG_R2]=0x0
reg_data[UC_ARM_REG_R3]=0x1
reg_data[UC_ARM_REG_R4]=0x20008d00
reg_data[UC_ARM_REG_R5]=0x2001fcb2
reg_data[UC_ARM_REG_R6]=0x0
reg_data[UC_ARM_REG_R7]=0x28431
reg_data[UC_ARM_REG_R8]=0x20008f08
reg_data[UC_ARM_REG_R9]=0x0
reg_data[UC_ARM_REG_R10]=0x0
reg_data[UC_ARM_REG_R11]=0x0
reg_data[UC_ARM_REG_R12]=0x20002a5c
reg_data[UC_ARM_REG_SP]=0x2001fc78
reg_data[UC_ARM_REG_LR]=0x3134d
reg_data[UC_ARM_REG_PC]=0x28430
reg_data[UC_ARM_REG_XPSR]=0x21000026
reg_data[UC_ARM_REG_FPSCR]=0x0
reg_data[UC_ARM_REG_MSP]=0x2001fc78

mem_data={}
mem_data[reg_data[UC_ARM_REG_R1]]=b'\x02\x00\x00\x00'

ram_fname='data/sram_1104.bin'
exits=[0x000284fe]

def place_input_callback(uc, input, persistent_round, data):
    if len(input)>8+0x100 or len(input)<8:
        return False
    uc.reg_write(UC_ARM_REG_R2,int.from_bytes(input[:4],'little'))
    uc.reg_write(UC_ARM_REG_R3,int.from_bytes(input[4:8],'little'))
    uc.mem_write(0xdead0000,input[8:])

protect=[(537001048, 537001080), (537001096, 537001120), (537001636, 537001648), (537001664, 537001688), (537001688, 537001712)]
emu.start(reg_data,mem_data,ram_fname,input_fanme,exits,place_input_callback,protect)