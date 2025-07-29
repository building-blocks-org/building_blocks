#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE app_db_strongly_typed;
    CREATE DATABASE app_db_primitive_obsession;
EOSQL
