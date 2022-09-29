import string
import time
import random
import paho.mqtt.client as paho

from fabrica import on_message

class Loja:
    def on_message(self, client, userdata, msg):
        mensagem = msg.payload.decode("utf-8")
        # Ainda não implementado
        pass

    def __init__(self, Id: int):
        self.Id = Id
        self.estoque = [100, 60, 20]
        self.client = paho.Client()
        self.client.on_message = self.on_message

    def connect(self, broker_IP: string, port: int):
        self.client.connect(broker_IP, port=port)

def on_message(client, userdata, msg):
    mensagem = msg.payload.decode("utf-8")
    lista = mensagem.split()
    who_talks, for_who, pid, quant = lista
    if who_talks != "CD":
        pass
    else:
        if for_who == userdata[0]:
            pass

def loja():
    client = paho.Client()
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883)
    client.subscribe(("Loja-CD", 1))