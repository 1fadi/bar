#!/bin/sh

while :; do
	script_output=$(python ~/scripts/barscript.py 2>&1)
  	echo " $script_output "
	sleep 0.5

done
