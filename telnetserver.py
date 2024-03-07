import socket
import select
import threading
import telnetClient

class TelnetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers_new_client(self, client):
        for observer in self.observers:
            observer.update_new_client(client)
        

    def start(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.socket.setblocking(False)
        threading.Thread(target=self.accept_clients, daemon=True).start()
        print(f"Server started on {self.host}:{self.port}")

    def accept_clients(self):
        while self.running:
            ready, _, _ = select.select([self.socket], [], [], 0.5)
            if ready:
                client_socket, client_address = self.socket.accept()
                client = telnetClient.TelnetClient(client_socket, client_address)
                self.clients.append(client)
                self.notify_observers_new_client(client)

    def broadcast(self, message):
        for client in self.clients:
            client.send_data(message)

    def handle_clients(self):
        for client in self.clients[:]:
            if client.socket.fileno() != -1:
                message = client.receive_data()
                if message:
                    print(f"Message from {client.address}: {message}")
                    self.broadcast(f"{client.address} says: {message}")
            else:
                client.close()
                self.clients.remove(client)
                print(f"Client disconnected from {client.address}")

    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.socket.close()
        print("Server stopped")

if __name__ == "__main__":
    server = TelnetServer("0.0.0.0", 1234)
    server.start()

    try:
        while True:
            server.handle_clients()
    except KeyboardInterrupt:
        server.stop()
