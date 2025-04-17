IP_ADDRESS=$(ip route get 8.8.8.8 | grep -oP 'src \K[^ ]+')

if grep -q "^IP_ADDR=" ./.env; then
    sed -i "s/^IP_ADDR=.*/IP_ADDR=$IP_ADDRESS/" ./.env
else
    echo "IP_ADDR=$IP_ADDRESS" >> ./.env
fi