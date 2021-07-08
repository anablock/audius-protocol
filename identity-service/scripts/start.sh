#!/bin/bash

if [ -z "$redisHost" ]; then
    redis-server --daemonize yes
    export redisHost=localhost
    export redisPort=6379
    export WAIT_HOSTS="localhost:6379"
    /usr/bin/wait
fi

if [ -z "$dbUrl" ]; then
    sudo -u postgres pg_ctl start -D /db
    export dbUrl=postgresql://postgres:postgres@localhost:5432/audius_identity_service
    export WAIT_HOSTS="localhost:5432"
    /usr/bin/wait
fi

node src/index.js