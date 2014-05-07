#!/bin/bash
$HOME/.winon/automount.sh
output_dir=/home/winon/filedrop
input_dir=/home/winon/input
mkdir $output_dir
cd /media
python2 /home/cmat/main.py $output_dir $input_dir &
xfe &
exit 0
