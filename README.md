# 🏠 SweetHome
### There is not place like ~

This is my personal implementation of a dotfiles manager written in Python.

![](https://github.com/rocchidavide/sweethome/blob/master/docs/media/sweethome-install.png)

## Features
- no third party libs used 
- you can use non-versioned local modules (called "dots"): you can either version them in a dedicated private git repository using git submodules
- you can compose dotfiles creating 'dotfiles_build'
- you can install desktop entries
- you can install icons
- you can set aliases and exports for each dots

## Requirements
- Python >= 3.4

## Installation

clone the repository

`git clone https://github.com/rocchidavide/sweethome ~/.sweethome`

## Usage

- install all dots

  `~/.sweethome/dotmanage.py install`


- install a specific dot

  `~/.sweethome/dotmanage.py install <dot name>`


- remove all dots

  `~/.sweethome/dotmanage.py remove`
