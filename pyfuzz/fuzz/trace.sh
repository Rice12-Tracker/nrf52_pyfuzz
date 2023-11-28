if [ $# -ne 1 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

folder_name=$1
cd $folder_name
cp ../../stack_tracer.py emulator.py || exit
cp -r ../../data . 


python3 "${folder_name}.py" "${folder_name}_input/sample1.bin" 
rm -r data emulator.py
