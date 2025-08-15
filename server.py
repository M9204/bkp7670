from flask import Flask, request
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

MQTT_HOST = "ddf927fd9af44789b245774345c7bf14.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "user9"
MQTT_PASS = "hknnQlRofqnyqj_aQxmeoJ6vPbvK-4fX"

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()

@app.route("/relay", methods=["POST"])
def relay():
    data = request.json
    topic = "arduino/relays"
    client.publish(topic, str(data))
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
