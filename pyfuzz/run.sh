if [ $# -ne 1 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

folder_name=$1
cd $folder_name
cp ../emulator.py . || exit
cp -r ../data . 
cd ../../AFLplusplus/unicorn_mode || exit
cp -r ../../pyfuzz/$folder_name . || exit
cd $folder_name || exit
../../afl-fuzz -U -m none -i ./"${folder_name}_input" -o ./"${folder_name}_output" -- python "${folder_name}.py" @@
cp -r "${folder_name}_output" ../../../pyfuzz/$folder_name
cd ../
rm -r $folder_name
cd ../../pyfuzz/$folder_name
rm -r data emulator.py
