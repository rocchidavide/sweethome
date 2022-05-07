#!/bin/bash

function printHeader() {
  echo -e "[*] \e[36m$1"
}


printHeader "APT: update sources"
apt update
printHeader "APT: install packages"
apt install --yes \
    sshfs \
    htop \
    tilix \
    flameshot peek \
    fonts-firacode fonts-powerline ttf-mscorefonts-installer \
    rofi \
    python3.8-venv python3-pyqt5 \
    # megasync \
    # python3-dev python3-pip python3-venv python3-setuptools python3-wheel \
    # git \
    # build-essential \

if ! command -v starship &> /dev/null
then
  printHeader "Install Starship"
  curl -sS https://starship.rs/install.sh | sh
else
  printHeader "Starship already installed"
fi

# ~/.sweethome/dotmanage.py install --force
