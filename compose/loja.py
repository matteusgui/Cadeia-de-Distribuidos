from fileinput import filename
import paho.mqtt.client as paho
import sys
from time import sleep
import numpy as np
import datetime
import random
import multiprocessing as mp
#---------------------------------------
A = 0
B = 2
C = 3
MAX_STOCK = np.array([100, 60, 20], dtype = np.int32)
stock = np.empty(200, dtype=np.int32)
for i in range(len(stock)):
    stock[i] = MAX_STOCK[i%3]/2
store_id = 0
stock_log = ""

#-------------------------------------------


def register_stock():
    print("wow")

def on_message(client, userdata, msg):
    global stock
    global store_id
    result = np.fromstring(msg.payload.decode("UTF-8"),dtype=int, sep=";")
    if(result[0] == store_id):
        print("chegou: "+str(result))
        dif = MAX_STOCK[result[1]%3] - stock[result[1]]
        if(dif > result[2]):
            stock[result[1]] += result[2]
        else:
            stock[result[1]] += dif

def debito_e_credito():
    global stock
    for i in range(len(stock)):
        qtd = random.randint(2,7)
        stock[i] -= qtd if (stock[i] - qtd) >= 0 else stock[i]
        if(stock[i] < MAX_STOCK[i%3]/4):
            payload = str(store_id) + ";" + str(i) + ";" + str( MAX_STOCK[i%3]-stock[i])
            client.publish('Kx9Z4Ya', payload , qos=1)
            #pedir restock

def saveonfile():
    t = str(datetime.datetime.now())
    with open(stock_log, 'a', encoding='utf-8') as f:
        f.write(t + ";")
        np.savetxt(f, stock,fmt='%d', delimiter=";", newline=";")
        f.write("\n")

if __name__ == "__main__":
    now = datetime.datetime.now()
    store_id = int(sys.argv[1])
    stock_log = "stock_log_" + str(store_id) + ".txt"

    client = paho.Client()
    client.on_message = on_message
    client.connect('broker.hivemq.com', 1883) 
    client.subscribe('3OFu5lq', qos=1)

    client.loop_start()
    saveonfile()
    #sleep(random.randint(1,30))
    while np.sum(stock) > 0:
        #print(stock)
        debito_e_credito()
        saveonfile()
        sleep(random.randint(30,50))