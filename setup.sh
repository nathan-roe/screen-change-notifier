#!/bin/bash
gnome_path="$(readlink -f ./bin/gnome-screenshot)"
current_gnome_path=/usr/bin/gnome-screenshot
if [ -e $current_gnome_path ]
then
	sudo mv $current_gnome_path /usr/bin/gnome-screenshot-original
	sudo cp $gnome_path $current_gnome_path

fi

stereo_path=/usr/share/sounds/freedesktip/stereo
if [ -e $stereo_path/camera-shutter.oga ]
then
	mv $stereo_path/camera-shutter.oga $stereo_path/camera-shutter-disabled.oga
else
	echo "Camera shutter path already moved or doesn't exist"
fi
