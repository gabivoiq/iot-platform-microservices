docker swarm init

docker pull grafana/grafana:7.3.6
docker pull influxdb:1.8.3
docker pull eclipse-mosquitto:2.0.4
docker build -t python_adapter:latest .

docker stack deploy -c stack.yml sprc3
