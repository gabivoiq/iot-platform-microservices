docker stack rm sprc3
docker container rm $(docker ps -q)
docker volume rm $(docker volume ls -q)
