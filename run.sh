#!/bin/bash

ARG_ERROR_MESSAGE="Use 'prod' or 'dev' arguments to either run production or development contatiner"

if [ $# != 1 ]
then
	echo "You should provide 1 and only 1 argument."
	exit
fi

if [ $1 == 'prod' ]
then
	COMPOSE_CONFIG='./docker/production.yml'
	CONTAINER_GROUP='twitter'
elif [ $1 == 'dev' ]
then
	COMPOSE_CONFIG='./docker/testing.yml'
    CONTAINER_GROUP=twitter-testing
else
	echo $ARG_ERROR_MESSAGE
	exit
fi

docker compose -f $COMPOSE_CONFIG -p $CONTAINER_GROUP up -d

if [ $1 == 'dev' ]
then
	sleep 2
	psql -h 0.0.0.0 -p 8080 -U postgres -c "CREATE USER twitteradmin WITH PASSWORD 'twitterAdmin123';"
    psql -h 0.0.0.0 -p 8080 -U postgres -c "CREATE DATABASE twitter;"
    psql -h 0.0.0.0 -p 8080 -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE twitter TO twitteradmin;"
	psql -h 0.0.0.0 -p 8080 -U postgres -c "ALTER DATABASE twitter OWNER TO twitteradmin;"

fi

