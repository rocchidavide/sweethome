# SweetHome
### _There is not place like ~_

This is my personal implementation of a dotfiles manager written in Python.

## Features

- no third party libs used 
- can use non-versioned local modules (called "dots"): you can either version them in a dedicated private git repository using git submodules
- can compose dotfiles creating 'dotfiles_build'
- can install desktop entries
- can install icons
- can set aliases and exports for each dots

## Requirements
- Python >= 3.4

## Installation

1) clone the repository

`git clone https://github.com/rocchidavide/sweethome ~/.sweethome`

2) install stuff

`~/.sweethome install`