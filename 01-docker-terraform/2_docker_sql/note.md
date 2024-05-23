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
  --network=pg-network \
  --name pg-database \
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
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

- Create a docker network

```bash
docker network create pg-network
```

- Convert jupyter to .py script

```bash
jupyter nbconvert --to=script ingest_data.ipynb
```

- run ingest_data.py

```bash
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --tb=ny_taxi_data \
  --url=${URL}
```

- build and run data ingest docker container

```bash
docker build -t taxi_ingest:v001 .
```

```bash
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pg-database \
  --port=5432 \
  --db=ny_taxi \
  --tb=ny_taxi_data \
  --url=${URL}
```

# Docker Compose

```bash
docker-compose up -d
```
