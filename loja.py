import string
import time
import random
import paho.mqtt.client as paho

class Loja:
    def _on_message(client, userdata, msg):
        mensagem = msg.payload.decode("utf-8")
        # Ainda não implementado
        pass
    def __init__(self, Id: int):
        self.Id = Id
        self.estoque = [100, 60, 20]
        self.client = paho.Client()

    def connect(self, broker_IP: string, port: int):
        self.client.connect(broker_IP, port=port)