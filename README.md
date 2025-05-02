# OpenTelemetry

## Table of contents
1. [What is OpenTelemetry?](#what-is-opentelemetry)
2. [Concepts](#concepts)
3. [Getting started with OpenTelemetry on Python](#getting-started-with-opentelemetry-on-python)
4. [Collecting telemetry data on multiple machines with OpenTelemetry](#collecting-telemetry-data-on-multiple-machines-with-opentelemetry)
4. [Glossary](#glossary)

## What is OpenTelemetry?
OpenTelemetry is an observability¹ framework and toolkit designed to facilitate the **generation**, **extraction** and **collection** of telemetry² data.

**Warning:** OpenTelemetry is **not** an observability backend on itself.

## Concepts
### Architecture
OpenTelemetry is composed of microservices³ that communicate with each other via gRPC⁴ and HTTP.

#### Learn more
[OpenTelemetry's architecture](https://opentelemetry.io/docs/demo/architecture/)

### Signals
The data utilized by OpenTelemetry.

They are **system outputs** that describe the operation of a system.

Currently, OpenTelemetry supports the following types of signals:
1. Traces: The path of a request through the application.
2. Metrics: A measurement captured at runtime.
3. Logs: A recording of an event.
4. Baggage: Contextual information passed between signals.

### Context propagation
Allows for signals to be correlated to each other. That way, traces can build information about a system across services.

In OpenTelemetry, **context** is an object which receives information pertaining the sender and the receiver of a signal. In that case, context **propagation** is the mecanism which moves context across services, serializing or deserializing information the context object and provides the relevant information to transmitted from a service to another.

### Components
Currently, OpenTelemetry is made of several components:
1. [Specification](#1-specification)
2. [Collector](#2-collector)
3. [Language-specific API and SDK implementations](#3-language-specific-api-and-sdk-implementations)
4. [Kubernetes operator](#4-kubernetes-operator)
5. [Function as a Service assets](#5-function-as-a-service-assets)

#### 1. Specification
Cross-language requirements and expectations.
+ API: Data types and operating for generating and correlating [signals](#signals)
+ SDK: Requirements for a language-specific implementation of the API, configuration, data processing and exporting concepts
+ Data: OpenTelemetry Protocol (OTLP) and vendor-agnostic semantics

#### 2. Collector
A vendor-agnostic proxy that can receive, process, and export telemetry data.

It can support various file formats for telemetry data, such as:
+ Prometheus
+ OTLP
+ Jaeger

#### 3. Language-specific API and SDK implementations
OpenTelemetry has language-specific SDKs (software development kits) that allow you to use the OTel API to generate telemetry data and export it to your preferred backend.

They also let you incorporate instrumentation libraries for common libraries and frameworks that you can use to connect to manual instrumentation in your application.

+ Instrumentation libraries: OpenTelemetry supports a broad number of components that generate relevant telemetry data from popular libraries and frameworks for supported languages.

+ Exporters: An intermediate between an application and the backend to which you want to export the data. It's best practice to use them in production environments. OTLP exporters are designed with the OpenTelemetry data model in mind, emitting OTel data without any **loss of information.** Furthermore, many tools that operate on telemetry data support OTLP.

+ Zero-code instrumentation: Provides a way to instrument an application without touching its source code (when applicable).

+ Resource detectors: A resource represents an entity producing telemetry as resource attributes. The language specific implementations of OpenTelemetry provide resource detection from the OTEL_RESOURCE_ATTRIBUTES environment variable and for many common entities, like process runtime, service, host, or operating system.

+  Cross-service propagators: Context propagation happens through instrumentation libraries. If needed, you can use propagators yourself to serialize and deserialize cross-cutting concerns such as the context of a span and baggage.

+  Samplers: Processes that restrict the amount of traces generated. Each language-specific implementation of OTel offers its own head samplers.

#### 4. Kubernetes operator
Manages the OpenTelemetry Collector and auto-instrumentation of the workloads using OpenTelemetry.

#### 5. Function as a Service assets
OpenTelemetry supports various methods of monitoring Function-as-a-Service provided by different cloud vendors.

## Getting started with OpenTelemetry on Python
This repository includes a small demonstration of the practical applications of OpenTelemetry.

It is a small application that collects the CPU and RAM usage of your machine every 5 seconds and exports it to Prometheus.

There are two versions of this app: 
+ app.py exports the telemetry data directly to Prometheus
+ app_collector.py exports it to OpenTelemetry Collector, which exposes the data to Prometheus.

To run it, follow these steps:

### 1. Preparing the environment
First, run:
```bash
source venv.sh
```

Then, make sure you are in src/getting_started:

```bash
cd src/getting_started
```

### 1.1 Install Prometheus
```bash
sudo pacman -S prometheus
```

#### 1.1.1 Modify /etc/prometheus/prometheus.yml
Modify the **global** and **scrape_configs** sections based on the example provided in **src/prometheus.txt**. 

You can use your text editor of choice to do so. The following example uses nano: 

```bash
nano /etc/prometheus/prometheus.yml
```

#### 1.1.2 Enable Prometheus (if you have just installed it)
```bash
sudo systemctl enable --now prometheus
```

#### 1.1.3 Restart Prometheus (if you had it running and modified prometheus.yml)
```bash
sudo systemctl restart prometheus
```

#### 1.1.4 Verify Prometheus is running
```bash
sudo systemctl status prometheus
```

You should see something like this:

![Screenshot of a bit of the output of sudo systemctl status prometheus. The image shows that prometheus is enabled and active (running).](imgs/image-1.png)

### 1.2 (Optional) Install Docker
Open a new terminal (CTRL+ALT+T), then run:

```bash
sudo pacman -S docker-compose
```

#### 1.2.1 Pull an image of OpenTelemetry Collector
In this project, OpenTelemetry Collector Core is being used.

```bash
sudo docker pull otel/opentelemetry-collector
```

#### 1.2.2 Run OpenTelemetry Collector
Make sure you are in OpenTelemetry/, and **not** in src, then run:
```bash
sudo docker run --rm -p 4318:4318 -p 8889:8889 -v "$(pwd)/otel_collector_config.yaml":/etc/otelcol/config.yaml otel/opentelemetry-collector:latest
```

### 2. Begin monitoring
Open a new terminal (CTRL+ALT+T) and run:

```bash
python3 app.py
```

Or:

```bash
python3 app_collector.py
```

#### 2.1 Observe results
Go to http://localhost:8001/metrics to see the Prometheus server (if you are running app.py).

Go to http://localhost:9090 to use Prometheus' GUI to see and query results.

### 3. Stop monitoring
Press CTRL + C.

## Collecting telemetry data on multiple machines with OpenTelemetry
This project also features a more complex project utilizing the power of OpenTelemetry. This app collects metrics on multiple machines connected to the same network as one server machine running a container⁵ of OpenTelemetry Collector Core.

Refer to [this file](src/README.md) to know more.

## Glossary
1. Observability: The ability to learn about a system's status at a point in time by asking questions about it.
2. Telemetry: The collection and transmission of the performance data of a device or product.
3. Microservices: A type of software architecture which divides a bigger application into serveral smaller ones, each one self-sufficient, independent and representing one _responsibility_. The parts usually communicate with each other using APIs. 
4. gRPC: Google Remote Procedure Control (gRPC) is an open code framework for communication between systems.
5. Container: A container is a unit of software that packages both the source code and dependencies of an app in an standalone environment, with the goal of ensuring it will run regardless of the machine.