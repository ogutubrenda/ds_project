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

## Implementation
1. Consistent Hashing: Maps each request to the appropriate server based on the hash value, reducing remappings when servers are added or removed. This technique distributes keys (or requests) uniformly across nodes, minimizing hotspots and ensuring balanced load distribution.
2. Queue Sharding: Splits the queue into multiple shards, each managed by a different server instance. Consistent hashing ensures balanced mapping of requests to shards, even with server changes. Each shard operates independently, reducing contention and improving system performance.

**Distributed Queue with Sharding Diagram**:
<img width="612" alt="Screenshot 2024-07-19 at 13 18 41" src="https://github.com/user-attachments/assets/a6e4578b-26c7-4115-9c2d-b4acdf7dd153">


## Assumptions
1. Network Reliability: Assumes a reliable network with minimal packet loss, designed to handle transient issues, though prolonged failures could impact performance.
2. Uniform Load Distribution: Assumes client requests are uniformly distributed. If requests skew towards specific keys, additional mechanisms might be needed for effective load balancing.
3. Server Homogeneity: Assumes all servers have similar capabilities and performance characteristics to ensure uniformity and predictability in handling requests.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ogutubrenda/ds_project
   cd ds_project
2. **Build Docker Images**:
   ```bash
   docker-compose build
3. **Run the Docker Containers**:
   ```bash
   docker-compse up
4. **Set up Environment Variables**: 
Refer to the system components
   


