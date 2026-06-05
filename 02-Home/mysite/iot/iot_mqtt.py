import paho.mqtt.client as mqtt
from .models import Event
import json

ID = "30" # Your personal Sensor ID for tracking
mqtt_broker = "ia.ic.polyu.edu.hk" # Broker
mqtt_port = 1883 # Default
mqtt_qos = 1 # Quality of Service = 1
mqtt_topic = "iot/sensor"

def mqtt_on_message(client, userdata, msg):
    try:
        # 1. Decode the raw binary packet into a standard readable UTF-8 string format
        d_msg = str(msg.payload.decode("utf-8"))
        
        # 2. Parse the JSON data
        iotData = json.loads(d_msg)
        
        # 3. Print out the incoming message in your terminal
        if iotData["id"] == ID:
            print(f"⭐ [MY SENSOR] Received on topic {msg.topic} : {iotData}")
        else:
            print(f"📡 [OTHER SENSOR] Received from ID={iotData['id']} at {iotData['loc']} : temp={iotData['temp']}")
        
        # 4. Save EVERY valid data packet to your SQLite database for historical logs
        p = Event(node_id=iotData["id"], node_loc=iotData["loc"], temp=iotData["temp"])
        p.save()
        print("Successfully saved data packet to SQLite!")

    # Prevents non-JSON messages sent by other students from crashing your background loop
    except (json.JSONDecodeError, KeyError, ValueError):
        pass

mqtt_client = mqtt.Client() # Create a Client Instance (leaving it empty lets paho generate a unique ID automatically)
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(mqtt_broker, mqtt_port) # Establish a connection to a broker
print("Connect to MQTT broker")
mqtt_client.subscribe(mqtt_topic, mqtt_qos)
mqtt_client.loop_start()