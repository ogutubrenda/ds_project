# README

## Customizable Load Balancer for Distributed Systems

### 128099 Brenda Ogutu
### 145353 Yvonne Ndambiri
### 139840 Wendo Mbijiwe

## Overview
This project implements a customizable load balancer designed to route asynchronous requests from multiple clients to multiple servers, ensuring an even distribution of the load. The load balancer uses consistent hashing to efficiently distribute requests and maintain system performance even in the event of server failures.

## Features
1. **Asynchronous Request Handling**: Routes requests from several clients asynchronously among several servers.
2. **Consistent Hashing**: Utilizes consistent hashing to distribute client requests evenly across server instances.
3. **Docker Deployment**: Both the load balancer and server instances are containerized using Docker.
4. **Scalability**: Supports dynamic scaling by adding or removing server instances.
5. **Fault Tolerance**: Automatically spawns new server instances to handle requests in case of server failures.

## System Components

### Server
- **Endpoints**:
  - `/home` (GET): Returns a unique identifier to distinguish among replicated server containers.
  - `/heartbeat` (GET): Sends heartbeat responses to check server health.

### Consistent Hashing
- **Parameters**:
  - Number of Server Containers: 3
  - Total Slots in Consistent Hash Map: 512
  - Number of Virtual Servers for Each Server Container: log2(512) = 9
  - Request Mapping Hash Function: `H(i) = i + 2i^2 + 17`
  - Virtual Server Mapping Hash Function: `Φ(i, j) = i + j + 2j^2 + 25`

### Load Balancer
- **Endpoints**:
  - `/rep` (GET): Returns the status of the replicas managed by the load balancer.
  - `/add` (POST): Adds new server instances to the load balancer.
  - `/rm` (DELETE): Removes server instances from the load balancer.
  - `/<path>` (GET): Routes the request to a server replica based on consistent hashing.

## Installation and Deployment

### Prerequisites
- **OS**: Ubuntu 20.04 LTS or above
- **Docker**: Version 20.10.23 or above
- **Languages**: Python (preferred), C++, Java, or any other language

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>

#Features


