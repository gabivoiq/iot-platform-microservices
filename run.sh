docker build -t db_adapter:latest .
docker stack deploy -c stack.yml sprc3
