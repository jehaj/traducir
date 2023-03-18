FROM python:alpine AS builder
WORKDIR /usr/src/app
RUN pip install --no-cache-dir lxml
RUN pip install --no-cache-dir requests
RUN apk -q add sqlite

COPY database-setup.py ./
COPY ["sql traducir.txt", "./"]

RUN [ "python", "./database-setup.py" ]


FROM python:alpine
WORKDIR /usr/src/app

EXPOSE 5000

COPY --from=builder /usr/src/app/traducir.db ./
COPY app.py ./

RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir waitress
RUN apk -q add sqlite

CMD [ "waitress-serve", "--listen=127.0.0.1:5000", "app:app" ]
