#!/bin/bash

export PGUSER=postgres
export PGPASSWORD=thisismypassword

echo "Drop and create database forcefully"

psql -U $PGUSER -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'trivia' AND pid <> pg_backend_pid();"
psql -U $PGUSER -c "DROP DATABASE IF EXISTS trivia;"
psql -U $PGUSER -c "CREATE DATABASE trivia;"

echo "Importing..."

psql -U $PGUSER -d trivia -f "trivia.psql"

echo "DONE"