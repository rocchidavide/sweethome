#!/bin/bash

#DISPLAY_NOTEBOOK="eDP"
DISPLAY_HDMI="HDMI-A-0"
DISPLAY_DP1="DisplayPort-1"
SCRIPTS_DIR="$SWEETHOME_PATH/dots/usageprofiles/bin"

function isDisplayConnected {
    xrandr | grep $1 | grep -w connected > /dev/null
}

isDisplayHDMIConnected=$(isDisplayConnected $DISPLAY_HDMI)
isDisplayDP1Connected=$(isDisplayConnected $DISPLAY_DP1)

if $isDisplayHDMIConnected && $isDisplayDP1Connected
then
    source "${SCRIPTS_DIR}/set_usageprofile_box.sh"
    notify-send --icon=gtk-info "Profilo Box" "Setup per il box abilitato" --expire-time=3000
elif ! $isDisplayHDMIConnected && ! $isDisplayDP1Connected
then
    source "${SCRIPTS_DIR}/set_usageprofile_mobile.sh"
    notify-send --icon=gtk-info "Profilo Mobile" "Setup mobile abilitato" --expire-time=3000
fi

nitrogen --restore &
