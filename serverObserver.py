class ServerObserver:
    def update_new_client(self, client):
        print(f"Observer notified of new client: {client.address}")

