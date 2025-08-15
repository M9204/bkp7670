import socket, ssl, threading

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 5000

BROKER_HOST = "dog.lmq.cloudamqp.com"
BROKER_PORT = 5671  # TLS

def handle_client(client_socket):
    try:
        context = ssl.create_default_context()
        broker_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=BROKER_HOST)
        broker_socket.connect((BROKER_HOST, BROKER_PORT))

        def forward(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data: break
                    dst.sendall(data)
            except:
                pass

        t1 = threading.Thread(target=forward, args=(client_socket, broker_socket))
        t2 = threading.Thread(target=forward, args=(broker_socket, client_socket))
        t1.start(); t2.start()
        t1.join(); t2.join()
    finally:
        client_socket.close()
        broker_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LISTEN_HOST, LISTEN_PORT))
server.listen(5)
print(f"Proxy listening on {LISTEN_HOST}:{LISTEN_PORT}")

while True:
    client_sock, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_sock,)).start()
