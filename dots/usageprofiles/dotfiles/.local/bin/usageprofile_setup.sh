#!/bin/bash
DISPLAY_HDMI="HDMI-A-0"
DISPLAY_DP1="DisplayPort-1"
DISPLAY_DP3="DisplayPort-3"
DISPLAY_DP4="DisplayPort-4"
SCRIPTS_DIR="$SWEETHOME_PATH/dots/usageprofiles/bin"

function isDisplayConnected() {
  xrandr | grep -w "$1" | grep -w connected >/dev/null
  echo "$?"
}

isDisplayHDMIConnected="$(isDisplayConnected "$DISPLAY_HDMI")"
isDisplayDP1Connected="$(isDisplayConnected "$DISPLAY_DP1")"
isDisplayDP3Connected="$(isDisplayConnected "$DISPLAY_DP3)"
isDisplayDP4Connected="$(isDisplayConnected "$DISPLAY_DP4")"

if [ "$isDisplayDP3Connected" -eq 0 ] && [ "$isDisplayDP4Connected" -eq 0 ]; then
  source "${SCRIPTS_DIR}/set_usageprofile_box.sh"
  notify-send --icon=gtk-info "Profilo Box" "Setup per il box abilitato" --expire-time=3000
elif [ ! "$isDisplayDP3Connected" -eq 0 ] && [ ! "$isDisplayDP4Connected" -eq 0 ]; then
  source "${SCRIPTS_DIR}/set_usageprofile_mobile.sh"
  notify-send --icon=gtk-info "Profilo Mobile" "Setup mobile abilitato" --expire-time=3000
fi

nitrogen --restore &