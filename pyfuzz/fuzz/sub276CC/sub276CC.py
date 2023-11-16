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

## TODO ##

reg_data={}
mem_data={}
ram_fname=''
exits=[0x278D0]
def place_input_callback(uc, input, persistent_round, data):
    

##########

emu.start(reg_data,mem_data,ram_fname,input_fanme,exits,place_input_callback)