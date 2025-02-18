# Train Station

A simplified train, station, travel and crew management system. Built on Django Rest Framework

## Installing / Getting started

Build containers in docker-compose file with command

```shell
docker-compose build
```

And start it with command

```shell
docker-compose up
```

Open your browser and enter the domain

```shell
http://127.0.0.1:8001/api/station/
```

You can create your user own User here

```shell
http://127.0.0.1:8001/api/user/create/
```

Or you can use already created users:
Regular user:
    username: sampleuser@test.com
    password: samplepassword3223
Admin or Superuser:
    username: sampleadmin@test.com
    password: heater2332

## Features

We have user and station Apps to get acquainted with all endpoints you can read
swagger documentation by link

```shell
http://127.0.0.1:8001/api/doc/swagger/#/station
```