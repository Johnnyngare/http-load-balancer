# Customizable Load Balancer

## Introduction
This project implements a customizable load balancer using consistent hashing to distribute client requests among several server replicas. The load balancer ensures an even distribution of load and handles server failures by spawning new replicas.

## Setup and Installation
1. Ensure Docker and Docker Compose are installed.
2. Clone the repository.
3. Run `make build` to build the Docker images.
4. Run `make up` to start the services.

## Design Choices
- **Consistent Hashing**: Ensures minimal disruption when servers are added or removed.
- **Docker**: Simplifies deployment and scaling.

## Usage
The load balancer exposes the following endpoints:
- `/rep`: Returns the status of server replicas.
- `/add`: Adds new server instances.
- `/remove`: Removes server instances.
- `/<path>`: Routes the request to the appropriate server based on the consistent hashing algorithm.

## Testing and Performance Analysis
- Launch `tests/test_script.py` to generate 10,000 asynchronous requests and observe load distribution.
- Monitor how the load balancer handles server failures and spawns new instances.

## Future Work
- Enhance failure detection and recovery mechanisms.
- Implement advanced load balancing strategies.

