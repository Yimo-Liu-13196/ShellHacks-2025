#!/bin/sh
set -e
: "${API_BASE_URL:=http://api:8000}"

for file in /usr/share/nginx/html/*.html; do
  tmp_file="${file}.tmp"
  sed "s#__API_BASE_URL__#${API_BASE_URL}#g" "$file" > "$tmp_file"
  mv "$tmp_file" "$file"
done

exec "$@"
