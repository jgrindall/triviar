#!/bin/bash

export PGUSER=postgres
export PGPASSWORD=thisismypassword

echo "Drop and create database forcefully"

psql -U $PGUSER -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'trivia_test' AND pid <> pg_backend_pid();"
psql -U $PGUSER -c "DROP DATABASE IF EXISTS trivia_test;"
psql -U $PGUSER -c "CREATE DATABASE trivia_test;"

echo "Importing..."

psql -U $PGUSER -d trivia_test -f "trivia.psql"

echo "DONE, running tests"

python -m test_flaskr
