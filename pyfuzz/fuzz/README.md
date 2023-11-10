# How to fuzz
1. Directory must be consist of  Dirname/Dirname.py & Dirname/Dirname_input/samplexx.bin
2. Start fuzzing with command `run.sh Dirname`
# How to write Harness
## `emu.start(reg_data,mem_data,ram_fname,input_fanme,exits,place_input_callback)`
- reg_data: Init register data
- mem_data: Init memory data
- ram_fname: sram file name
- exits: list of exit addresses
- place_input_callback: function to manage input data
