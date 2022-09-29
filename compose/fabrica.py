import paho.mqtt.client as paho
import sys
import numpy as np

factory_id = -1
def on_message(client, userdata, msg):
    global factory_id
    result = np.fromstring(msg.payload.decode("UTF-8"),dtype=int, sep=";") #[factory_id product_id qtd] = result

    if(result[0] == factory_id and result[1]//3 == factory_id):
        print("Enviando" + str(result))
        payload = str(result[1])+ ";" + str(result[2])
        client.publish("2y4hT7cR", payload , qos=1)

if __name__ == "__main__":

    factory_id = int(sys.argv[1])

    client = paho.Client()
    client.on_message = on_message

    client.connect('broker.hivemq.com', 1883) 
    client.subscribe('UjK54bM', qos=1)

    client.loop_forever()
        