import telnetServer
import serverObserver

server = telnetServer.TelnetServer(host="0.0.0.0", port=23)

observer = serverObserver.ServerObserver()
server.register_observer(observer)
server.start()
print("WOPR Running")

try:
    while True:
        server.handle_clients()
except KeyboardInterrupt:
    server.stop()