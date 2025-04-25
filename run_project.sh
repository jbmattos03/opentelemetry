#!/bin/bash

start_server=false
start_client=false
down=false

while getopts "scdh" opt; do
    case $opt in
        s)
            start_server=true
            ;;
        c)
            start_client=true
            ;;
        d)
            down=true
            ;;
        h)
            echo "Usage: $0 [-s] [-c] [-h]"
            echo "  -s  Start the server"
            echo "  -c  Start the client"
            echo "  -h  Show this help message"
            exit 0
            ;;
        *)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

# Executing commands
if [[ $start_server == true && $down == false ]]; then
    echo "Starting server..."
    docker compose -f docker-compose-server.yml up -d
fi

if [[ $start_client == true && $down == false ]]; then
    echo "Starting client..."
    docker compose -f docker-compose-client.yml up -d
fi

if [[ $start_client == true && $down == true ]]; then
    echo "Stopping client..."
    docker compose -f docker-compose-client.yml down
fi

if [[ $start_server == true && $down == true ]]; then
    echo "Stopping server..."
    docker compose -f docker-compose-server.yml down
fi