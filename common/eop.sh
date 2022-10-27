#!/bin/bash

# This script is used to elevate the current user to root privileges, activate the venv, and then run the specified command.

if [[ $EUID -ne 0 ]];
then
    # Print user

    exec sudo /home/kali/Desktop/Muninn/venv/bin/python3 /home/kali/Desktop/Muninn/main.py

fi
