- build docker image

```bash
docker build -t <image-name>:<tag-name> .
```

- run docker container

```bash
docker run -it test:pandas
```

- running Postgres on Windows (note the full path)
- for UNIX, we can use `$(pwd)` in path

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v d:/05-repo/data-engineering-zoomcamp/01-docker-terraform/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

- run postgres on localhost

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

- Running pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```
