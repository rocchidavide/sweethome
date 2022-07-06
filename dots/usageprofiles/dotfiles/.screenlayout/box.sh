#!/bin/sh
xrandr \
  --output eDP --off \
  --output HDMI-A-0 --mode 1920x1080 --pos 0x0 --rotate normal \
  --output DisplayPort-0 --off \
  --output DisplayPort-1 --off \
  --output DisplayPort-2 --off \
  --output DisplayPort-3 --mode 2560x1440 --pos 4480x0 --rotate normal \
  --output DisplayPort-4 --primary --mode 2560x1440 --pos 1920x0 --rotate normal
