import socket
from barelib import Server
print("default port is 5667")
    
def get_local_ipv4():
    """
    Retrieves the local IPv4 address of the machine.
    """
    try:
        hostname = socket.gethostname()
        ipv4_address = socket.gethostbyname(hostname)
        return ipv4_address
    except socket.gaierror:
        return "Could not resolve hostname to IP address."
        
print(f"your local ip is: {get_local_ipv4()}")

ip = input("ip: ")
if ip == "":
    ip = "0.0.0.0"
port = input("port")
if port == "":
    port = 5667

server = Server(ip, int(port))
server.start()

try:
    while True:
        msg = server.receive()
        if msg:
            client_id, text = msg
            if text is None:
                print(f"Client {client_id} disconnected")
            else:
                print(f"Client {client_id} sent: {text}")
                # Echo back to sender:
except KeyboardInterrupt:
    print("Shutting down server...")
    server.stop()