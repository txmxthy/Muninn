#!/bin/bash

# Install dependencies
echo "Starting Metasploit DB as Kali..."

# Ask Select init or start
echo "Select an option:"
echo "1) Start Metasploit DB"
echo "2) Init Metasploit DB"

read -p "Select an option (init if no db exists) [1-2]: " option
case $option in
    1) echo "Starting Metasploit DB..."
#       service postgresql start
       msfdb start
       ;;
    2) echo "Init Metasploit DB..."
#       service postgresql start
       msfdb init
       ;;
    *) echo "Invalid option"
       exit 1
       ;;
esac

