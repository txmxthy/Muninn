#!/bin/sh
set -e

if ! [ -e "/var/run/postgresql/*.pid" ]
then
    /etc/init.d/postgresql start
fi

if ! [ -e "/usr/share/metasploit-framework/config/database.yml" ]
then
    sudo msfdb init
fi

sudo msfdb start
