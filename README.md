
**README: Task 1 - Task 4**
### Design Section

#### Overview
The project implements a customizable load balancer with consistent hashing to distribute client requests across multiple server replicas. The system is designed to be scalable and fault-tolerant, ensuring efficient load distribution and quick recovery from server failures. The architecture employs Docker for containerization, allowing seamless deployment and management of server instances. Each server instance operates independently, enabling elastic scaling where servers can be added or removed based on current load and performance metrics.

Additionally, the system includes monitoring and logging mechanisms to track server health and request distribution. This helps in proactive identification and resolution of potential issues, ensuring high availability and reliability of the service.

#### Components
1. **Web Server**: Handles HTTP requests and provides endpoints for home and heartbeat. Each server instance runs inside a Docker container, making it easy to scale horizontally by adding more instances. The web server also includes basic health checks to ensure each instance is operational.
2. **Consistent Hash Map**: Used for mapping client requests to server instances. The consistent hash map ensures that the addition or removal of servers minimally impacts the mapping of existing requests. This reduces the need for rehashing and helps maintain a stable request distribution across servers.
3. **Load Balancer**: Routes client requests using consistent hashing and manages server replicas. It monitors the health of server instances using heartbeat signals and dynamically adjusts the server pool based on load and server availability. The load balancer can also redistribute requests in case of server failures to ensure continuous service availability.

**System Architecture Diagram**:
```plaintext
+---------------------+
|      Client         |
+---------+-----------+
          |
          v
+---------+-----------+
|    Load Balancer    |
+---------+-----------+
          |
  +-------+-------+
  |       |       |
  v       v       v
+---+   +---+   +---+
| S |   | S |   | S |
| e |   | e |   | e |
| r |   | r |   | r |
| v |   | v |   | v |
| e |   | e |   | e |
| r |   | r |   | r |
| 1 |   | 2 |   | 3 |
+---+   +---+   +---+
```

---

### Distributed Queue with Sharding

#### Overview
A distributed queue with sharding is implemented to divide the workload among multiple server instances. Each shard represents a portion of the queue, and consistent hashing ensures that each shard is mapped to a specific server instance. This approach minimizes the load on any single server and provides a mechanism for scaling the system by adding more shards and servers. The sharding mechanism allows for efficient handling of high throughput and ensures that the system can accommodate growing demand.

#### Implementation
1. **Consistent Hashing**: Ensures that each request is mapped to the appropriate server based on the hash value. This technique reduces the number of remappings required when a server is added or removed. Consistent hashing distributes the keys (or requests) uniformly across the available nodes (servers), minimizing hotspots and ensuring balanced load distribution.
2. **Queue Sharding**: Divides the queue into multiple shards, each managed by a different server instance. The consistent hashing algorithm ensures that the mapping of requests to shards remains balanced, even as servers are added or removed from the cluster. Each shard operates independently, processing requests assigned to it, which reduces contention and improves overall system performance.

**Distributed Queue with Sharding Diagram**:
![image](https://github.com/alexwafula/Customizable_Load_Balancerr/assets/136974351/43ed11fc-ed87-440a-9143-7cd7e113b919)


### Assumptions

1. **Network Reliability**: Assumes a reliable network with minimal packet loss. The system is designed to handle transient network issues, but prolonged network failures could affect performance.
2. **Uniform Load Distribution**: Assumes that client requests are uniformly distributed. If the requests are skewed towards specific keys, additional mechanisms might be needed to balance the load more effectively.
3. **Server Homogeneity**

### Prerequisites
1. Docker: latest [version 20.10.23, build 7155243]
   sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

2.  Docker-compose standalone [version v2.15.1]
   sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose 

**Docker**: To containerize the application.

2. **Python**: For implementing the server, load balancer, and consistent hash map.
3. **Flask**: For handling HTTP requests within the server and load balancer.
4. **Git**: For version control and managing the project repository.
5. **Miniconda**: This is a free minimal installer for Anaconda with minimum packages that allows one to use virtual environments. It is lightweight and quick.

---

### Installation Steps

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/alexwafula/Customizable_Load_Balancerr.git
   cd Customizable_Load_Balancerr
   ```

2. **Build Docker Images**:

   ```sh
   docker-compose build
   ```

3. **Run Docker Containers**:

   ```sh
   docker-compose up
   ```

4. **Set Up Environment Variables**:

   Ensure the `.env` file is correctly configured with necessary environment variables.

5. **Set up Miniconda**:
   **Windows**
   These three commands quickly and quietly install the latest 64-bit version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for Windows, change the name of the .exe installer in the curl command.

   curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
   start /wait "" miniconda.exe /S
   del miniconda.exe

   After installing, open the “Anaconda Prompt (miniconda3)” program to use Miniconda3. For the Powershell version, use “Anaconda Powershell Prompt (miniconda3)”.
   **Mac OS**
 mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
   **Linux**

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

---

### Testing
Here 10.110.10.216 is used as an example broker-cluster instance.

run a producer instance from log file
COMMAND
└──python runproduce.py --id 1 --topics T1:P1 T2:P2 T3:* --broker 10.110.10.216 --log_loc ./test/{EXP}
** producer_{id}.txt log file format must be maintained else throws Exception("log file:incompitable")

run a consumer instance and store log
COMMAND
└──python runconsume.py --id 1 --topics T1:* T2:P1 --broker 10.110.10.216 --log_loc ./test/{EXP}

run API test cases
COMMAND
└──bash testAPI.sh 10.110.10.216

![image](https://github.com/alexwafula/Customizable_Load_Balancerr/assets/136974351/82bbbb76-a13d-4d37-9ca2-6fbafd898bf6)

run 2-producer, 2-consumer setup
Question: Implement 2 Producers and 2 consumers with 2 topics T1 & T2 each having partitions as shown in Fig. 2 using the library developed. Given below is the "topic (partition):producers:consumers" mapping.

T1(P1): Producer1 Producer2: Consumer1 Consumer2
T1(P2): Producer1 Producer2: Consumer1 Consumer2
T2(P1): Producer1 Producer2: Consumer1 Consumer2
T2(P2): Producer1 Producer2: Consumer1 Consumer2
Here, the last point means that Producer1 and Producer2 will produce to topic T2 partition P2;  Consumer1, Consumer2 will consume from T2 partition P2.
[Producers]
└──python runproduce.py --id 1 --topics T1:P1 T2:P1 T1:P2 T2:P2 --broker  10.110.10.216 --log_loc ./test/2P2C
└──python runproduce.py --id 2 --topics T1:* T2:* --broker  10.110.10.216 --log_loc ./test/2P2C

[Consumers]
└──python runconsume.py --id 1 --topics T1:P1 T2:P1 T1:P2 T2:P2 --broker  10.110.10.216 --log_loc ./test/2P2C
└──python runconsume.py --id 2 --topics T1:* T2:* --broker  10.110.10.216 --log_loc ./test/2P2C

Run all commands together
-------------------------
+ bash test2P2C.sh 10.110.10.216

#### Unit Tests
1. **Run Unit Tests**:

   ```sh
   python -m unittest discover -s tests
   ```

#### Functional Tests
1. **Test Endpoints**:
   - Use tools like `curl` or Postman to test the following endpoints:
     - `/home`: Returns a unique identifier for the server.
     - `/heartbeat`: Returns the heartbeat status.
     - `/rep`: Checks the status of replicas.
     - `/add`: Adds a new server instance.
     - `/rm`: Removes a server instance.

   Example using `curl`:

   ```sh
   curl http://localhost:5000/home
   curl http://localhost:5000/heartbeat
   curl -X POST http://localhost:5000/add -d 'server_id=new_server'
   curl -X DELETE http://localhost:5000/rm -d 'server_id=existing_server'
   ```

#### Performance Tests
1. **Load Testing**:
   - Use tools like `Apache JMeter` or `Locust` to simulate high traffic and observe the load distribution and fault tolerance.

2. **Experiment Scenarios**:
   - **A-1**: Launch 10000 async requests on 3 server containers and report the request count handled by each server instance.
   - **A-2**: Increment server instances from 2 to 6, launching 10000 requests on each increment, and report the average load.
   - **A-3**: Test all load balancer endpoints and demonstrate quick spawning of new instances upon server failure.
   - **A-4**: Modify hash functions and observe changes from A-1 and A-2.

By following these sections, you can understand the design, implement the distributed queue with sharding, and set up and test the customizable load balancer.


**Task 1: Server Implementation**

**Overview:**
In Task 1, we implemented a simple web server that accepts HTTP requests on port 5000 and provides two endpoints: `/home` and `/heartbeat`. The `/home` endpoint returns a string with a unique identifier to distinguish among replicated server containers. The `/heartbeat` endpoint sends heartbeat responses upon request, allowing the load balancer to identify failures in the set of containers maintained by it.

**Implementation:**
We implemented the server using Python, utilizing the Flask framework for handling HTTP requests. The server runs on port 5000 and provides the required endpoints as specified in the assignment. The server's unique identifier is set as an environment variable while running a container instance from the Docker image of the server.

**Dockerfile:**
We included a Dockerfile to containerize the server as an image, making it deployable for subsequent tasks. The Dockerfile installs necessary dependencies and sets up the environment for running the Flask application.

**Deployment:**
To deploy the server, build the Docker image using the provided Dockerfile and run a container instance from the built image. Ensure that the container is exposed on port 5000 to accept incoming HTTP requests.

**Task 2: Consistent Hashing Implementation**

**Overview:**
In Task 2, we implemented a consistent hash map using Python, which serves as the underlying data structure for the load balancer in Task 3. We utilized an array-based implementation to represent the hash map, with provisions for handling collisions using linear or quadratic probing.

**Implementation:**
We implemented the consistent hash map using Python, utilizing an array data structure to represent the hash map and hash functions provided in the assignment. The implementation ensures that requests are mapped to the appropriate server instances based on the consistent hashing algorithm.

**Task 3: Load Balancer Implementation**

**Overview:**
Task 3 involves building a load balancer container that uses the consistent hashing data structure from Task 2 to manage a set of server replicas. The load balancer is responsible for routing client requests to server replicas in a balanced manner and maintaining the desired number of replicas even in case of failure.

**Implementation:**
We implemented the load balancer container using Python and Flask, leveraging the consistent hashing data structure implemented in Task 2. The load balancer provides HTTP endpoints for modifying configurations, checking the status of managed web server replicas, and routing client requests to server replicas.

**Endpoints:**
- `/rep`: Returns the status of the replicas managed by the load balancer.
- `/add`: Adds new server instances to scale up with increasing client numbers.
- `/rm`: Removes server instances to scale down with decreasing client or system maintenance.
- `/<path>`: Routes client requests to a server replica as scheduled by the consistent hashing algorithm.

**Deployment:**
Deploy the load balancer container using the provided Dockerfile, Docker-compose file, and Makefile. Ensure that the load balancer is exposed on port 5000 to accept incoming HTTP requests.

**Task 4: Analysis**

**Overview:**
Task 4 involves testing and analyzing the performance of the load balancer implementation in different scenarios, including load distribution among server containers and recovery from server container failure.

**Experiments:**
- **A-1:** Launch 10000 async requests on N = 3 server containers and report the request count handled by each server instance. Below is a snapshot of the result
  ![image](https://github.com/alexwafula/Customizable_Load_Balancerr/assets/91899603/d0d6956d-4d32-48ef-a02d-f108d8887771)

- **A-2:** Increment N from 2 to 6 and launch 10000 requests on each increment. Report the average load of the servers at each run. Below is a snapshot of the result
  ![image](https://github.com/alexwafula/Customizable_Load_Balancerr/assets/91899603/fc842e83-eb33-4bb2-954b-67f9141ede24)

- **A-3:** Test all endpoints of the load balancer and demonstrate that it spawns a new instance quickly in case of server failure.
- **A-4:** Modify the hash functions and report the observations from A-1 and A-2.

**Conclusion:**
Overall, the load balancer implementation effectively distributes the load among server containers and demonstrates scalability and fault tolerance. The analysis provides insights into the performance and behavior of the load balancer in various scenarios, contributing to the understanding of distributed systems and load balancing techniques. The other testing images are found in rm_responses.json.

Footer

