# Collecting metrics from multiple machines with OpenTelemetry

## Architecture
Basically, one machine will be a server, which will collect the metrics from the other machines and expose them to a local Prometheus instance.

This code currently assumes all machines are in the same network and can communicate with one another.

## Collecting metrics
### Server side
#### Install Docker
Open a new terminal (CTRL+ALT+T), then run:

```bash
sudo pacman -S docker-compose
```

#### Pull an image of OpenTelemetry Collector
In this project, OpenTelemetry Collector Core is being used.

```bash
sudo docker pull otel/opentelemetry-collector
```

#### Run OpenTelemetry Collector
Then, all you have to do is run the following command:
```bash
sudo docker run --rm -p 4318:4318 -p 8889:8889 -v "$(pwd)/otel_collector_config.yaml":/etc/otelcol/config.yaml otel/opentelemetry-collector:latest
```

### Client side
#### Set up environment variables
Based on **.env_example.txt**, create a **.env** file in OpenTelemetry/ and replace <central_collector_IP> with your server's actual IP address.

#### (Optional) Make sure the server is reachable
Replace "central_collector_IP" in the following command with your server's actual IP address.
```bash
ping central_collector_IP
```

If it fails, make sure your machine is in the same network as the server machine.

#### Collect metrics
First, go to src:
```bash
cd src
```

Then, run:
```bash
python3 app_collector_local.py
```