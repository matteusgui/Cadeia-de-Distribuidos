import time
from random import randint
import paho.mqtt.client as paho

def on_message(client, userdata, msg):
    mensagem = msg.payload.decode("utf-8")
    lista = mensagem.split()
    who_talks, for_who, pid, quant = lista
    if who_talks != "CD":
        pass
    else:
        if for_who == userdata[0]:
            time.sleep(randint(1,5))
            response = for_who + " " + who_talks + " " + pid + " " + quant
            client.publish("CD-Fabrica",response, qos=1)

def fabrica():
    client = paho.Client()
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883)
    client.subscribe(("CD-Fabrica", 1))

    client.loop_forever()