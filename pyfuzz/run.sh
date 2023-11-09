if [ $# -ne 1 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

# Use pwd to get the current working directory
current_dir=$(
current
pwd)
# Use parameter expansion to extract the folder name
folder_name="${current_dir##*/}"

cd ../AFLplusplus/unicorn_mode
cp -r ../../$folder_name .
cd $folder_name
../../afl-fuzz -U -m none -i ./"$1_input" -o ./"$1_output" -- python "$1.py" @@
cp -r "$1_output" ../../../$folder_name
cd ..
#rm -r $folder_name
