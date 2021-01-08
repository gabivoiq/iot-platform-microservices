import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import logging
import os
import sys
import time

logger = logging.getLogger("main_adapter")

INFLUXDB_HOST = os.getenv("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = int(os.getenv("INFLUXDB_INTERNAL_PORT", 8086))
INFLUXDB_DB = os.getenv("INFLUXDB_DB", "db")

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_INTERNAL_PORT", 1883))
IS_DEBUG = os.getenv("DEBUG_DATA_FLOW", "false")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    str_payload = msg.payload.decode("utf-8")
    logger.info("%s %s", msg.topic, str_payload)
    try:
        json_payload = json.loads(str_payload)
    except json.decoder.JSONDecodeError as e:
        logger.error("An error occurred when deserializing json: ", exc_info=e)

    # json_body = [
    #     {
    #         "measurement": msg.topic +
    #         "tags" : {
    #
    #         }
    #     }
    # ]
    # influxDB_client.write_points()
    # print(influxDB_client.get_list_database())


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
