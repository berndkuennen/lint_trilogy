FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV LISTEN_PORT 8080
EXPOSE          8080

RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx

# patch section to make image runnable on OpenShift
# see: https://github.com/tiangolo/uwsgi-nginx-flask-docker/issues/29
#COPY nginx.conf    /etc/nginx/conf.d/nginx.conf
#COPY entrypoint.sh /entrypoint.sh
#RUN  chmod +x      /entrypoint.sh

COPY ./app /app

RUN  touch /etc/nginx/conf.d/nginx.conf \
 &&  chmod -R g+rwx /var/cache/nginx /var/run /var/log/nginx  /etc/nginx/  \
 &&  chmod -R a+rwx /var/log/supervisor  \
 &&  pip3 install -r /app/requirements.txt
