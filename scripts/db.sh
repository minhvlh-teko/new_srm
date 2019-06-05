#!/bin/bash
set -e
export PGUSER=postgres

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER flask_wms;
    CREATE DATABASE flask_wms;
    ALTER USER flask_wms WITH PASSWORD '1234';
    GRANT ALL PRIVILEGES ON DATABASE flask_wms TO flask_wms;
EOSQL
