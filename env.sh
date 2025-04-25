#!/bin/bash
IP_ADDRESS=$(ip route get 8.8.8.8 | grep -oP 'src \K[^ ]+')
hostname=$(hostnamectl | grep -oP "Static hostname\s*: \K.+")

# Check if the .env file exists; if not, create it
if [ ! -e ".env" ]; then
    touch ./.env
fi

# Check if the IP_ADDR variable exists in the .env file
# If it does, update it
# If not, add it
if grep -q "^IP_ADDR=" ./.env; then
    sed -i "s/^IP_ADDR=.*/IP_ADDR=$IP_ADDRESS/" ./.env
else
    echo "IP_ADDR=$IP_ADDRESS" >> ./.env
fi

# Check if the hostname variable exists in the .env file
# If it does, update it
# If not, add it
if grep -q "^hostname=" ./.env; then
    sed -i "s/^hostname=.*/hostname=$hostname/" ./.env
else
    echo "hostname=$hostname" >> ./.env
fi