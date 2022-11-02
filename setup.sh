#!/bin/bash

# Install dependencies
echo "Starting Metasploit DB as Kali..."
msfdb init

# Press any key to continue
read -n 1 -s -r -p "Press any key to continue"
