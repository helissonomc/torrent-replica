import socket
import threading
import sys


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
        self.socket.connect(('peer1', port))
        print(f"Connected to 192.168.16.1:{port}")

        self._start_threads(self.socket)

    def _start_threads(self, connection):
        print(f'Thread started {threading.current_thread()}')
        threading.Thread(target=self.receive_messages, args=(connection,)).start()
        threading.Thread(target=self.send_messages, args=(connection,)).start()

    def receive_messages(self, connection):
        while True:
            try:
                message = connection.recv(1024).decode("utf-8")
                if message:
                    print(f"Peer: {message}")
                else:
                    print("Connection closed by the peer.")
                    break
            except:
                print("An error occurred.")
                break

    def send_messages(self, connection):
        while True:
            message = input()
            connection.send(message.encode("utf-8"))


def main():
    if len(sys.argv) != 3:
        print("Usage: python peer.py <host|connect> <port>")
        sys.exit(1)

    mode = sys.argv[1]
    port = int(sys.argv[2])

    host = "0.0.0.0"
    peer = Peer(host, 5000)
    print(f"main thread {threading.current_thread()}")
    if mode == "host":
        peer.start_server()
    elif mode == "connect":
        peer.connect_to_peer(port)
    else:
        print("Invalid choice. Please enter 'host' or 'connect'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
