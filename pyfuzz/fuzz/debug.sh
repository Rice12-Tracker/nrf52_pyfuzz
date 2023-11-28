if [ $# -ne 1 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

folder_name=$1
cd $folder_name
cp ../../emulator_debug.py emulator.py || exit
cp -r ../../data . 

for file in "${folder_name}_output/default/queue"/* ; do
    echo "$file"
    python3 "${folder_name}.py" "$file"
done

for file in "${folder_name}_output/default/hangs"/* ; do
    echo "$file"
    python3 "${folder_name}.py" "$file"
done

for file in "${folder_name}_output/default/crashes"/* ; do
    echo "$file"
    python3 "${folder_name}.py" "$file"
done


#python3 "${folder_name}.py" "${folder_name}_input/sample1.bin" 
rm -r data emulator.py
