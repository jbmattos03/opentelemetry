# OpenTelemetry

## Table of contents
1. [What is OpenTelemetry?](#what-is-opentelemetry)
2. [Concepts](#concepts)
3. [Getting started with OpenTelemetry on Python](#getting-started-with-opentelemetry-on-python)
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


#### 4. Kubernetes operator
Manages the OpenTelemetry Collector and auto-instrumentation of the workloads using OpenTelemetry.

#### 5. Function as a Service assets
OpenTelemetry supports various methods of monitoring Function-as-a-Service provided by different cloud vendors.

## Getting started with OpenTelemetry on Python
This folder includes a small demonstration of the practical applications of OpenTelemetry.

It is a small application that collects the CPU and RAM usage of your machine every 5 seconds and exports it to a Prometheus backend server.

To run it, follow these steps:
### 1. Install necessary libraries
```bash
source venv.sh
```

### 1.1 Install Prometheus
```bash
sudo pacman -S prometheus
```

### 2. Begin monitoring
```bash
prometheus --config.file=prometheus.yml
```

```bash
python3 main.py
```

### 2.1 Observe results
Go to http://localhost:8001/metrics to see the Prometheus server.

Go to http://localhost:9090 to use Prometheus' GUI to see and query results.

### 3. Stop monitoring
Press CTRL + C.

## Glossary
1. Observability: The ability to learn about a system's status at a point in time by asking questions about it.
2. Telemetry: The collection and transmission of the performance data of a device or product.
3. Microservices: A type of software architecture which divides a bigger application into serveral smaller ones, each one self-sufficient, independent and representing one _responsibility_. The parts usually communicate with each other using APIs. 
4. gRPC: Google Remote Procedure Control (gRPC) is an open code framework for communication between systems.