FROM tiangolo/uwsgi-nginx

# Remove uWSGI config
RUN rm -f /etc/nginx/conf.d/nginx.conf 

# Copy standard nginx config 
COPY nginx/nginx.conf /etc/nginx

# Copy chat-server app
COPY chat-server.py /app/
COPY config.ini /app/
COPY lib/ /app/lib/
COPY requirements.txt /app/
COPY web/ /app/web/
COPY nginx/start.sh /app/

# Install python packages
RUN pip install -r requirements.txt

# Run chat server
ENTRYPOINT ["/app/start.sh"]
