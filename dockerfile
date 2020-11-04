FROM tiangolo/uwsgi-nginx-flask:python3.8

LISTEN_PORT 8080
EXPOSE      8080

# patch section to make image runnable on OpenShift
# see: https://github.com/tiangolo/uwsgi-nginx-flask-docker/issues/29
#COPY nginx.conf    /etc/nginx/conf.d/nginx.conf
#COPY entrypoint.sh /entrypoint.sh
#RUN  chmod +x      /entrypoint.sh

COPY ./app /app

RUN  chgrp -R root /var/cache/nginx  \
 &&  chmod -R g+w  /var/cache/nginx  \
 &&  pip3 install -r /app/requirements.txt

