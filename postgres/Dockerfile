FROM postgres:13.1-alpine

# Copy st-chat.sql to /docker-entrypoint-initdb.d/ where postgres will import the database on container start. 
COPY postgres/st-chat.sql /docker-entrypoint-initdb.d/
RUN chmod a+r /docker-entrypoint-initdb.d/st-chat.sql
