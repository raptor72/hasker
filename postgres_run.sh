docker kill hasker_postgres
y | docker container prune
docker pull postgres:12
docker run -d --name=hasker_postgres -e POSTGRES_USER=hasker -e POSTGRES_DB=hasker -e POSTGRES_PASSWORD=qwe123 -p 5432:5432 -v /opt/postgres_docker/hasker/:/var/lib/postgresql/data postgres:12

