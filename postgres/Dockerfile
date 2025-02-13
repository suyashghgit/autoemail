FROM postgres:latest

# Copy the SQL dump file into the container
COPY pg_backup.sql /docker-entrypoint-initdb.d/

# Add a script to import the database
COPY init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# The official postgres image will automatically execute any .sql files 
# in /docker-entrypoint-initdb.d/ during container initialization 