# How to install
- Pull the image directly
```
docker pull ksprsk/nrf52-pyfuzz
docker run -it ksprsk/nrf52-pyfuzz
```
- Or build AFL++&unicorn_mode with ./build.sh
# How to fuzz
- At pyfuzz/fuzz, fuzzing with ./run.sh dirname
- It will fuzz dirname.py with dirname_input and save output at dirname_output
