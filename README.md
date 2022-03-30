# 🏠 SweetHome
### There is no place like ~

This is my personal implementation of a dotfiles manager written in Python.

![](https://github.com/rocchidavide/sweethome/blob/master/docs/media/sweethome-install.gif)

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

run

`~/.sweethome/dotmanage.py install --force`

logout and login again to permit profile settings to be loaded.

## Usage

- install all dots

  `sweethome install`


- install a specific dot

  `sweethome install <dot name>`


- remove all dots

  `sweethome remove`

## Credits

- [Cristiano Verondini](http://www.verondini.it/) for the precious help along the years, the friendly company, for sharing coding passion and for the suggestion of the tagline "There is no place like ~"
