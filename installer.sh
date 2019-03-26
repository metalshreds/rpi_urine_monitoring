#!/usr/bin/env bash

# This is an installer script for Rpi Urine Monitor station
# It is based on the MagicMirror2 installer script.

echo -e "\e[0m"
echo ''
echo 'Installing Rpi Urine Monitor' 
echo '' 
echo -e "\e[0m"

# Determine which Pi is running.
ARM=$(uname -m) 

# Check the Raspberry Pi version.
if [ "$ARM" != "armv7l" ]; then
	echo -e "\e[91mSorry, your Raspberry Pi is not supported."
	echo -e "\e[91mPlease run Rpi Urine Monitor on a Raspberry Pi 2 or 3."
	exit;
fi

# Define helper methods.
function version_gt() { test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }
function command_exists () { type "$1" &> /dev/null ;}

# Update before first apt-get
echo -e "\e[96mUpdating packages ...\e[90m"
sudo apt-get update || echo -e "\e[91mUpdate failed, carrying on installation ...\e[90m"

# Installing helper tools
echo -e "\e[96mInstalling helper tools ...\e[90m"
sudo pip install ipython pyserial mettler_toledo_device || exit

# Download Rpi Urine Monitor script, and check if it has already been downloaded
cd ~ || exit #if cant change directory something is quite wrong...
if [ -d "$HOME/rpi_urine_monitoring" ] ; then
	echo -e "\e[93mThe rpi_urine_monitoring appears to already be in this raspberry pi."
	echo -e "To prevent overwriting, the installer will be aborted."
	echo ""
	echo -e "To check for any updates \e[1m\e[97mgit pull\e[0m from the ~/rpi_urine_monitoring directory."
	echo ""
	exit;
fi

echo -e "\e[96mCloning Rpi Urine Monitor Script...\e[90m"
if git clone --depth=1 https://github.com/metalshreds/rpi_urine_monitoring.git; then 
	echo -e "\e[92mCloning Rpi Urine Monitor Script Done!\e[0m"
else
	echo -e "\e[91mUnable to clone Rpi Urine Monitor Script."
	exit;
fi

echo -e "\e[92m"
echo " "
# echo -e "\e[92mWe're ready! Run \e[1m\e[97mDISPLAY=:0 npm start\e[0m\e[92m from the ~/MagicMirror directory to start your MagicMirror.\e[0m"
echo -e "The Rpi Urine Monitor script and dependencies have been successfully installed!"
echo -e "Take the mettler toledo scale out of standby mode, navigate to the script directory"
echo -e " \e[97m~/rpi_urine_monitor\e[92m and run the script:"
echo -e "\e[97mpython circularBuffer_latest.py\e[92m to run on this raspberry pi"
echo -e "Otherwise see other intructions on the website to run remotely through PuTTY"
echo " "
echo " "
echo -e "\e[0m"