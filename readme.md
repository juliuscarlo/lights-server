# Flash the OS
Flash raspbian light 32bit on your raspberry pi zeros

# Upgrade packages
    sudo apt update && sudo apt upgrade

# Install pip3 and flask
    sudo apt-get install python3-pip
    pip3 install flask

# Enable remote gpio
    sudo raspi-config

# install pigpio
    sudo apt install pigpio

# enable the pigpio service
    sudo systemctl enable pigpiod.service
    sudo systemctl start pigpiod.service

