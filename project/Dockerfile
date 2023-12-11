FROM jwilder/dockerize as dockerize
FROM node:21-alpine
COPY --from=dockerize /usr/local/bin/dockerize /usr/local/bin/dockerize
WORKDIR /workspaces/tailwind-flask-starter/project
COPY /package*.json ./
RUN npm ci
COPY . .
RUN npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch

FROM python:3.8-alpine
RUN pip install --upgrade pip
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev bash postgresql postgresql-client nano postgresql postgresql-client supervisor
WORKDIR /workspaces/tailwind-flask-starter/project
COPY /requirements.txt ./
COPY /supervisord.conf /etc/supervisord.conf
RUN pip3 install -r ./requirements.txt
COPY . .
USER postgres
RUN initdb -D /var/lib/postgresql/data
RUN echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf
RUN echo "unix_socket_directories = '/tmp'" >> /var/lib/postgresql/data/postgresql.conf
ENV PGHOST=/tmp

USER root
WORKDIR /workspaces/tailwind-flask-starter

ENV FLASK_APP=project
ENV FLASK_DEBUG=1
CMD ["supervisord", "-n", "-c", "/etc/supervisord.conf"]
