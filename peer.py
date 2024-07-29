import socket
import threading
import sys
import os


class Peer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False

    def start_server(self):
        self.is_host = True
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Listening on {self.host}:{self.port}...")
        while True:
            self.client_socket, self.client_address = self.socket.accept()
            print(f"Connection established with {self.client_address}")

            self._start_threads(self.client_socket)

    def connect_to_peer(self, port):
        self.socket.connect(('192.168.16.1', port))  # Replace with actual peer IP
        print(f"Connected to 192.168.16.1:{port}")

        self._start_threads(self.socket)

    def _start_threads(self, connection):
        threading.Thread(target=self.receive_messages, args=(connection,)).start()
        threading.Thread(target=self.send_messages, args=(connection,)).start()

    def receive_messages(self, connection):
        while True:
            try:
                message = connection.recv(1024).decode("utf-8")
                if message:
                    if message.startswith("FILE:"):
                        print("Receiving file...")
                        filename = message[5:]
                        self.receive_file(connection, filename)
                    else:
                        print(f"Peer: {message}")
                else:
                    print("Connection closed by the peer.")
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def send_messages(self, connection):
        while True:
            message = input()
            if message.startswith("SEND_FILE:"):
                filepath = message[10:]
                if os.path.isfile(filepath):
                    filename = os.path.basename(filepath)
                    connection.send(f"FILE:{filename}".encode("utf-8"))
                    self.send_file(connection, filepath)
                else:
                    print("File not found.")
            else:
                connection.send(message.encode("utf-8"))

    def receive_file(self, connection, filename):
        with open(f"received_{filename}", "wb") as f:
            print('aqui')
            data = connection.recv(1024)
            print(data)

            f.write(data)
        print(f"File {filename} received.")

    def send_file(self, connection, filepath):
        with open(filepath, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                connection.send(data)
        print(f"File {filepath} sent.")


def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    mode = sys.argv[1]
    port = int(sys.argv[2])

    host = "0.0.0.0"
    peer = Peer(host, 5000)
    if mode == "host":
        peer.start_server()
    elif mode == "connect":
        peer.connect_to_peer(port)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
