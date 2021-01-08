docker stack rm sprc3
sleep 5
docker container rm $(docker ps -q)
docker volume rm $(docker volume ls -q)
