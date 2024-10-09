# Module responsible to prepare monitoring feature

For database we are using the cloud service [Neon](https://neon.tech/)

In this folder we will have only prepare db, the code to insert new msgs and update with user feedback will be on ui 

## To prepare the database

1. UV installed

2. Enviromental variables

```bash
export PGHOST='<your-host>'
export PGDATABASE='<your-db>'
export PGUSER='<your-user>'
export PGPASSWORD='<your-password>'
```

3. Run python dependencies

```bash
uv sync
```

4. Run code

```bash
uv run prepare_db.py
```