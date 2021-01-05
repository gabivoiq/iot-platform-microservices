docker volume rm $(docker volume ls -q)
docker container rm $(docker ps -q)
