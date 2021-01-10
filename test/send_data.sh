for _ in {0..100}
do
  sleep 1
  mosquitto_pub -d -t HAHA/Mongo -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"HUMID\" : 22.221312312, \"BAT\" : 44}"
  mosquitto_pub -d -t UPB/RPI_D -m "{\"timestamp\":\"2019-11-26T03:54:20+03:00\", \"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"HUMID\" : 5.2, \"BAT\" : 50}"
  sleep 1
  mosquitto_pub -d -t UPB/RPI_O -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"HUMID\" : 22.221312312, \"BAT\" : 44}"
  sleep 1
  mosquitto_pub -d -t UPB/RPI_O -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"IMP\" : 45.223423423, \"BAT\" : 43.23}"
  mosquitto_pub -d -t UPB/RPI_E -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"IMP\" : 22.1423432423, \"BAT\" : 56}"
  mosquitto_pub -d -t UPB/RPI_C -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"AQI\" : 55.1423432, \"BAT\" : 54.42}"
  mosquitto_pub -d -t UPB/RPI_C -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"AQI\" : 99.2345435, \"BAT\" : 86}"
  sleep 1
  mosquitto_pub -d -t UPB/RPI_C -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"RSSI\" : 11.12324, \"BAT\" : 12}"
  mosquitto_pub -d -t UPB/RPI_B -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"RSSI\" : 55.323423, \"BAT\" : 5}"
  sleep 1
  mosquitto_pub -d -t UPB/RPI_B -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"RSSI\" : 43.5423432, \"BAT\" : 90}"
  mosquitto_pub -d -t UPB/RPI_A -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"AQI\" : 24.234543, \"BAT\" : 95.3232}"
  sleep 1
  mosquitto_pub -d -t UPB/RPI_A -m "{\"imp\":\"Heello\", \"var\":\"aaaaaaa\", \"RSSI\" : 2.112312312, \"BAT\" : 100.12}"
done
