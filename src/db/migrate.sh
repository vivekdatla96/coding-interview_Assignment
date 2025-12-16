#!/bin/bash
set -e

echo "Running DB migrations..."

for file in db/init/*.sql
do
  echo "Applying $file"
  mysql \
    -h "$DB_HOST" \
    -u "$DB_USER" \
    -p"$DB_PASSWORD" \
    "$DB_NAME" < "$file"
done

echo "DB migrations completed"
