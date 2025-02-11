#!/bin/bash
gnome_path="$(readlink -f ../bin/gnome-screenshot)"
current_gnome_path=/usr/bin/gnome-screenshot
if [ -e $current_gnome_path ]
then
	sudo mv $current_gnome_path /usr/bin/gnome-screenshot-original
fi
sudo cp "$gnome_path" "$current_gnome_path"

stereo_path=/usr/share/sounds/freedesktip/stereo
if [ -e $stereo_path/camera-shutter.oga ]
then
	mv $stereo_path/camera-shutter.oga $stereo_path/camera-shutter-disabled.oga
else
	echo "Camera shutter path already moved or doesn't exist"
fi

exec_path=$(realpath '../dist/screen-notifier/screen-notifier')
icon_path=$(realpath '../assets/icon.svg')
desktop_content="
[Desktop Entry]
Type=Application
Name=Screen Notifier
Comment=Record screen area for changes and notify
Exec=${exec_path}
Icon=${icon_path}
Categories=Utility;
"

desktop_file_name=screen-notifier.desktop
touch $desktop_file_name
echo "$desktop_content" > $desktop_file_name;
chmod +x $desktop_file_name
sudo mv $desktop_file_name /usr/share/applications
# sudo rm /usr/share/applications/$desktop_file_name
sudo update-desktop-database
