from barelib import Client
import threading
import queue
import sys
import time
import getpass

username = getpass.getuser()
print(f"your user is: {username}")

helptxt = """
/ping
lists all active clients

/ping <target_client_id>
pings the target and sends back "Echo"

/relay <target_client_id> <optional message>
relays a message to the target. if optional message is blank, sends "Echo"

/chat <message>
sends a message to everyone

/exec <code>
executes python code on the server. data can be sent back using "self.send(<your id>, <message>)"

/sshcrack <target_client_id> <command>
executes any of these commands on the target's machine
"""

# add command to get this own client's id

print("default port is 5667")
ip = input("ip: ")
if ip == "":
    ip = "127.0.0.1"
port = input("port: ")
if port == "":
    port = 5667

print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    with print_lock:
        print("\r", end="")  # reset to line start
        print(*args, **kwargs)
        print("> ", end="", flush=True)

def threaded_input(prompt, input_queue):
    while True:
        try:
            user_input = input(prompt)
            input_queue.put(user_input)
        except EOFError:
            input_queue.put(None)
            break

input_queue = queue.Queue()
input_thread = threading.Thread(target=threaded_input, args=("> ", input_queue), daemon=True)
input_thread.start()

client = Client(ip, int(port))
client.connect()
safe_print("Use /help to see commands")

try:
    while True:
        if not input_queue.empty():
            msg = input_queue.get()
            if msg is None:
                safe_print("Server:", incoming)
                break
            elif msg == "/help":
                safe_print(helptxt)
            elif msg == "/quit":
                exit()
            else:
                client.send(msg)        
        incoming = client.receive()
        if incoming:
            if incoming is None:
                safe_print("Disconnected")
                break
            safe_print("From server:", incoming)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    client.disconnect()