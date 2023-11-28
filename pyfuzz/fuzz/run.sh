if [ $# -ne 1 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

folder_name=$1
cd $folder_name
cp ../../emulator_fuzz.py emulator.py || exit
cp -r ../../data . 
cd ../../../AFLplusplus/unicorn_mode || exit
cp -r ../../pyfuzz/fuzz/$folder_name . || exit
cd $folder_name || exit
../../afl-fuzz -U -m none -i ./"${folder_name}_input" -o ./"${folder_name}_output" -- python3 "${folder_name}.py" @@
cp -r "${folder_name}_output" ../../../pyfuzz/fuzz/$folder_name
cd ../
rm -r $folder_name
cd ../../pyfuzz/fuzz/$folder_name
rm -r data emulator.py
