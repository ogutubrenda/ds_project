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

## Task Analysis
## A-1: Distribution of Load Among Server Containers (N = 3)
Experiment:

Launched 10,000 asynchronous requests to a load balancer with 3 server containers.

Output:

Generated a bar chart showing the number of requests handled by each server instance.
Observations:

Bar Chart: The bar chart displays the distribution of requests among the three server containers.
Outcome: The load was distributed fairly evenly across the three servers.
Explanation:

Balanced Distribution: If the chart shows roughly equal bars, it indicates that the load balancer is effectively distributing requests across the available servers.
Performance View: A balanced distribution suggests that the load balancer implementation is functioning as expected for a small number of servers. If there is significant imbalance, it could point to potential issues in the load balancing algorithm.
## A-2: Scalability with Incremental N (2 to 6)
Experiment:

Incremented the number of server containers (N) from 2 to 6 and launched 10,000 requests for each increment.
Output:

Created a line chart showing the average load per server for different values of N.
Observations:

Line Chart: The line chart shows the average number of requests handled per server as N increases.
Expected Outcome: As N increases, the average load per server should decrease, assuming the load balancer distributes requests evenly.
Explanation:

Scalability: A decreasing trend in the average load per server with increasing N indicates good scalability. This means the load balancer effectively manages the load as more servers are added.
Performance View: If the average load per server remains relatively constant or decreases as expected, it suggests that the load balancer scales well with the number of server containers.
## A-3: Response to Server Failure
Experiment:

Tested all endpoints of the load balancer and simulated a server failure by killing the process on a specific port.
Output:

Observed how the load balancer handles the failure and whether it quickly spawns a new instance to handle the load.
Observations:

Server Failure Handling: After simulating a failure, the load balancer should detect the unavailability of the server and redirect requests to available servers. Ideally, it should also spawn new instances if configured to do so.
Expected Outcome: The load balancer should continue to operate and handle requests, possibly with a brief period of reduced capacity during recovery.
Explanation:

Recovery Speed: A quick recovery and continued operation indicate that the load balancer is robust and responsive to server failures.
Performance View: Effective failure handling demonstrates resilience and reliability of the load balancer in maintaining service availability.
## A-4: Observations with Modified Hash Functions
Experiment:

Modified the hash functions H(i) and Φ(i, j) and repeated the experiments from A-1 and A-2.
Output:

Reported observations based on changes to hash functions.
Observations:

Hash Function Impact: Changes in hash functions can affect how requests are distributed across servers. Analyzing the results of A-1 and A-2 with modified hash functions can reveal if the load distribution has improved or worsened.
Expected Outcome: Depending on the new hash functions, the distribution of requests might become more or less balanced.
Explanation:

Hash Function Effectiveness: Effective hash functions should ideally lead to more balanced distribution and better scalability. Observing how the distribution and scalability change with different hash functions provides insights into the impact of these functions on the load balancer's performance.
Performance View: Analyzing the results helps in understanding the impact of hash functions on load distribution and identifying optimal hash functions for improved performance.

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
   


