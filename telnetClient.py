class TelnetClient:
    #Used to negotiate protocol
    TN_INTERPRET_AS_COMMAND = 255
    TN_WILL = 251
    TN_WONT = 252
    TN_ECHO = 1

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.buffer = ""
        self.message_received = []
        
        #I want to ensure modern clients behave similarly to my C64 connection style
        self.request_echo_off()

    def send_data(self, data):
        self.socket.sendall(data.encode())

    def setup_message_receiver(self, callback):
        self.message_received = callback

    def receive_data(self):
        try:
            data = self.socket.recv(1024).decode('utf-8', errors='ignore')
            self.buffer += data
            if "\n" in self.buffer or "\r" in self.buffer:
                message, self.buffer = self.buffer.split("\r", 1)
                for n in self.message_received:
                    n(message)
                return message
        except UnicodeDecodeError:
            pass
        except BlockingIOError as e:
            pass
        return None

    def request_echo_off(self):
        self.socket.sendall(bytes([self.TN_INTERPRET_AS_COMMAND, self.TN_WILL, self.TN_ECHO]))

    def request_echo_on(self):
        self.socket.sendall(bytes([self.TN_INTERPRET_AS_COMMAND, self.TN_WONT, self.TN_ECHO]))


    def close(self):
        self.socket.close()
