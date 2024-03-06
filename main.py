import ollamaAPI
from telnetserver import TelnetServer

server = TelnetServer(port=2222)

clients = []

# Make a keyvalue hash with client as the key, and the message string as the value
messages = {}
print("WOPR Running")

while True:
    # Make the server parse all the new events
    server.update()

    # For each newly connected client
    for new_client in server.get_new_clients():
        # Add them to the client list 
        clients.append(new_client)
        # Send a welcome message
        server.send_message(new_client, "Welcome, you are client {}.".format(new_client))
        server.send_character(new_client, "USER: ")


    # For each client that has recently disconnected
    for disconnected_client in server.get_disconnected_clients():
        if disconnected_client not in clients:
            continue

        # Remove him from the clients list
        clients.remove(disconnected_client)

        # Send every client a message saying "Client X disconnected"
        for client in clients:
            server.send_message(client, "Client {} disconnected.".format(disconnected_client))

    # For each message a client has sent
    for sender_client, message in server.get_messages(): 
        if sender_client not in clients:
            continue
        
        server.send_character(sender_client, message)
        if sender_client not in messages:
            messages[sender_client] = message
        else:
            messages[sender_client] = messages[sender_client] + message 
        if(message=="\r"):
            fullMessage = messages[sender_client].strip()
            response = ollamaAPI.AskOllama(fullMessage)
            server.send_character(sender_client, "WOPR: ")
            server.send_message(sender_client, response)
            messages[sender_client] = ""
            server.send_character(sender_client, "USER: ")