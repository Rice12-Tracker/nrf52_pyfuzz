1-a. Pull the image directly
```
docker pull ksprsk/nrf52-pyfuzz
docker run -it ksprsk/nrf52-pyfuzz
```
1-b. ..or Build AFL++&unicorn_mode with ./build.sh
2. At pyfuzz/fuzz, fuzzing with ./run.sh dirname
3. It will fuzz dirname.py with dirname_input and save output at dirname_output
