#!/bin/bash

# Display setup
# -----------------------------------------------------------------------------
# source $HOME/.screenlayout/box.sh
source $HOME/.screenlayout/box-dock.sh

# Disable wifi
# -----------------------------------------------------------------------------
nmcli radio wifi off

# Apple Keyboard setup
# -----------------------------------------------------------------------------
# function keys first
# echo 2 | sudo tee /sys/module/hid_apple/parameters/fnmode
# fix swapped keys
# echo 0 | sudo tee /sys/module/hid_apple/parameters/iso_layout


# Distribute i3 workspaces to monitors
# -----------------------------------------------------------------------------
# i3-msg move workspace to output HDMI-A-0