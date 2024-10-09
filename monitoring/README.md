# Module responsible to prepare monitoring feature

For the database it use a Postgres:16

In this folder we will have only prepare db, the code to insert new msgs and update with user feedback will be on ui 

## How to see the metrics

The metrics will be available in streamlit separated page, this page is not explicity on chat page but can be access if you have the link

link: `https://chat-gourmet-ai.streamlit.app/monitoring`

## To prepare the database

1. UV installed

2. Enviromental variables

```bash
export PGHOST='localhost'
export PGDATABASE='cgourmetfb'
export PGUSER='cgourmet_user'
export PGPASSWORD='P@ssw0rd2024'
```

3. Run postgres on docker

```bash
docker run -d \
  --name postgres_service \
  -e POSTGRES_DB="cgourmetfb" \
  -e POSTGRES_USER="cgourmet_user" \
  -e POSTGRES_PASSWORD="P@ssw0rd2024" \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

3. Run python dependencies

```bash
uv sync
```

4. Run code

```bash
uv run prepare_db.py
```