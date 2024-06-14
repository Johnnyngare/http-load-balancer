from flask import Flask, request, jsonify
import requests
import hashlib

app = Flask(__name__)

servers = ['server1:5000', 'server2:5000', 'server3:5000']
virtual_servers = []
hash_slots = 512
replicas = 9

def hash_fn(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % hash_slots

def get_server(key):
    hash_key = hash_fn(key)
    for vs in sorted(virtual_servers):
        if hash_key <= vs[0]:
            return vs[1]
    return virtual_servers[0][1]

def setup_virtual_servers():
    for server in servers:
        for i in range(replicas):
            virtual_key = f"{server}#{i}"
            hash_key = hash_fn(virtual_key)
            virtual_servers.append((hash_key, server))
    virtual_servers.sort()

setup_virtual_servers()

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"replicas": servers}), 200

@app.route('/add', methods=['POST'])
def add_server():
    data = request.json
    new_servers = data.get("hostnames", [])
    for server in new_servers:
        servers.append(server)
        for i in range(replicas):
            virtual_key = f"{server}#{i}"
            hash_key = hash_fn(virtual_key)
            virtual_servers.append((hash_key, server))
    virtual_servers.sort()
    return jsonify({"message": "Servers added successfully"}), 200

@app.route('/remove', methods=['POST'])
def remove_server():
    data = request.json
    to_remove = data.get("hostnames", [])
    for server in to_remove:
        servers.remove(server)
        virtual_servers[:] = [vs for vs in virtual_servers if vs[1] != server]
    return jsonify({"message": "Servers removed successfully"}), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    server = get_server(path)
    response = requests.get(f"http://{server}/{path}")
    return response.content, response.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

