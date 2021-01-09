import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import logging
import os
import sys
import time
from datetime import datetime

logger = logging.getLogger("main_adapter")

INFLUXDB_HOST = os.getenv("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = int(os.getenv("INFLUXDB_INTERNAL_PORT", 8086))
INFLUXDB_DB = os.getenv("INFLUXDB_DB", "db")

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_INTERNAL_PORT", 1883))
IS_DEBUG = os.getenv("DEBUG_DATA_FLOW", "true")


def filter_json(msg):
    try:
        str_payload = msg.payload.decode("utf-8")
        json_data = json.loads(str_payload)
        logger.debug("Received a message by topic [%s]", msg.topic)
        logger.debug("Data timestamp is: %s", 'NOW' if 'timestamp' not in json_data else json_data['timestamp'])
        topic = str(msg.topic).replace("/", ".")
        for key in dict(json_data):
            if key == "timestamp":
                continue
            if type(json_data[key]) is int or type(json_data[key]) is float:
                logger.debug('{}.{} {}'.format(topic, key, json_data[key]))
                continue
            del json_data[key]

        return json_data, str(msg.topic)
    except Exception as e:
        logger.error("An error occurred when deserializing json: ", exc_info=e)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info("Connected to MQTT broker with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


def send_data_db(json_data, topic):
    try:
        location, workstation = topic.split("/", 2)
        if "timestamp" in json_data:
            timestamp = json_data["timestamp"]
            del json_data["timestamp"]
        else:
            timestamp = str(datetime.now())

        json_body_db = []
        for key in json_data:
            json_body_db.append({
                "measurement": location,
                "tags": {
                    "workstation": workstation,
                    "metric": key
                },
                "time": timestamp,
                "fields": {
                    "value": float(json_data[key])
                }
            })

        logger.debug(json_body_db)
        influxDB_client.write_points(json_body_db)
    except ValueError as ve:
        logger.error("An error occurred when parsing json data", exc_info=ve)
    except Exception as e:
        logger.error("An error occurred when sending data to influxDB", exc_info=e)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    json_data, topic = filter_json(msg)
    send_data_db(json_data, topic)


def exception_hook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def init_logger():
    level = "DEBUG" if IS_DEBUG == "true" else "INFO"
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')
    logger.setLevel(level)
    sys.excepthook = exception_hook


def connect_mqtt_broker():
    start_time = time.time()
    while True:
        try:
            code = mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
            if code == 0:
                logger.info("Successfully connected to MQTT broker")
                break
        except Exception as e:
            if start_time + 15 < time.time():
                sys.exit("Error connecting to MQTT broker - " + MQTT_BROKER_HOST + ":" + str(MQTT_BROKER_PORT))
            logger.warning("Error connecting to MQTT broker. Trying again...", exc_info=e)
            time.sleep(1)


if __name__ == "__main__":
    init_logger()

    logger.info("LOG level - %s", logging.getLevelName(logger.getEffectiveLevel()))
    logger.info("InfluxDB - %s:%d, database name - %s", INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DB)
    logger.info("MQTT Broker - %s:%d", MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    influxDB_client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
    influxDB_client.switch_database(INFLUXDB_DB)

    connect_mqtt_broker()
    mqtt_client.loop_forever()
