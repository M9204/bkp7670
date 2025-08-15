import socket, ssl, threading, os

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = int(os.environ.get("PORT", 5000))  # Render sets PORT env
MQTT_HOST = "ddf927fd9af44789b245774345c7bf14.s1.eu.hivemq.cloud"
MQTT_PORT = 8883

def handle_client(client_socket):
    context = ssl.create_default_context()
    broker_socket = context.wrap_socket(socket.socket(), server_hostname=MQTT_HOST)
    broker_socket.connect((MQTT_HOST, MQTT_PORT))

    def forward(src, dst):
        try:
            while True:
                data = src.recv(4096)
                if not data: break
                dst.sendall(data)
        except: pass

    t1 = threading.Thread(target=forward, args=(client_socket, broker_socket))
    t2 = threading.Thread(target=forward, args=(broker_socket, client_socket))
    t1.start(); t2.start()
    t1.join(); t2.join()
    client_socket.close(); broker_socket.close()

server = socket.socket()
server.bind((LISTEN_HOST, LISTEN_PORT))
server.listen(5)
print(f"TCP proxy listening on {LISTEN_HOST}:{LISTEN_PORT}")

while True:
    client_sock, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_sock,)).start()
