#!/bin/bash
set -e

# Wait for the PostgreSQL server to start
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Import the database dump
echo "Importing database dump..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/pg_backup.sql

echo "Database import completed!" 