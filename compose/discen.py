from fileinput import filename
import paho.mqtt.client as paho
import sys
from time import sleep
import numpy as np
import datetime
import random

#---------------------------------------
A = 0
B = 1
C = 2
MAX_STOCK = np.array([200, 120, 40], dtype = np.int32)
stock = np.empty(200, dtype=np.int32)
for i in range(len(stock)):
    stock[i] = MAX_STOCK[i%3]/2

CD_log = "CD_log.txt"

#-------------------------------------------
def register_stock():
    print("wow")

def on_message(client, userdata, msg):
    global stock
    result = np.fromstring(msg.payload.decode("UTF-8"),dtype=int, sep=";") #[store_id product_id qtd] = result
    
    if(msg.topic == "Kx9Z4Ya"):
        
        dif = result[2] if (stock[result[1]] - result[2]) >= 0 else stock[result[1]]
        stock[result[1]] -= dif
        #payload = str(result[0]) + ";" + str(result[1]) + ";" + str(dif)
        payload_loja = str(result[0]) + ";" + str(result[1]) + ";" + str(dif)
        if(dif != 0):
            client.publish('3OFu5lq', payload_loja , qos=1)
            print("enviou para loja:"+ payload_loja)

        if(stock[result[1]] < MAX_STOCK[result[1]%3]/4):
            payload_fabrica = str(result[1]//3)+";"+str(result[1]) + ";" + str(MAX_STOCK[result[1]%3] - stock[result[1]])
            client.publish('UjK54bM', payload_fabrica , qos=1)
        

    
    elif(msg.topic == "2y4hT7cR"):
        print("chegou da fabrica:" + str(result))
        dif = MAX_STOCK[result[0]%3] - stock[result[0]]
        if(dif > result [1]):
            stock[result[0]] += result[1]
        else:
            stock[result[0]] += dif



def saveonfile():
    t = str(datetime.datetime.now())
    with open(CD_log, 'a', encoding='utf-8') as f:
        f.write(t + ";")
        np.savetxt(f, stock,fmt='%d', delimiter=";", newline=";")
        f.write("\n")

if __name__ == "__main__":
    now = datetime.datetime.now()

    client = paho.Client()
    client.on_message = on_message

    client.connect('broker.hivemq.com', 1883) 
    client.subscribe('Kx9Z4Ya', qos=1)
    client.subscribe('2y4hT7cR', qos=1)

    client.loop_forever()
        
        