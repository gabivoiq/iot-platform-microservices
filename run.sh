if [ ! -f Dockerfile ]; then
  echo "You should launch this script from project root dir as ./run.sh"
  exit 1
fi

docker build -t python_adapter:latest .

docker swarm init

docker pull grafana/grafana:7.3.6
docker pull influxdb:1.8.3
docker pull eclipse-mosquitto:2.0.4

docker stack deploy -c stack.yml sprc3
