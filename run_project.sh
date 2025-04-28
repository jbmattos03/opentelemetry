#!/bin/bash

start_server=false
start_client=false
build=false
down=false

while getopts "scdbh" opt; do
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
        b)
            build=true
            ;;
        h)
            echo "Usage: $0 [-s] [-c] [-d] [-b] [-h]"
            echo "  -s  Start the server"
            echo "  -c  Start the client"
            echo "  -d  Stop a container. Use with -s and/or -c"
            echo "  -b  Build the images"
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
if [[ $build == true ]]; then
    echo "Building images..."
    docker compose -f docker-compose-server.yml build
    docker compose -f docker-compose-client.yml build
fi

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