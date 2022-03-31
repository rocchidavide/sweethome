#!/bin/bash

function printHeader() {
  echo -e "[*] \e[36m$1"
}


printHeader "Install APT packages"
apt update
apt install --yes \
  tilix \
  flameshot peek \
  megasync \
  fonts-firacode fonts-powerline ttf-mscorefonts-installer
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
