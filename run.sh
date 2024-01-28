#!/bin/bash

ARG_ERROR_MESSAGE="Use 'prod' or 'dev' arguments to either run production or development contatiner"
POSTGRES_COMMANDS=(
	"CREATE USER twitteradmin WITH PASSWORD 'twitterAdmin123';"
	"CREATE DATABASE twitter;"
	"GRANT ALL PRIVILEGES ON DATABASE twitter TO twitteradmin;"
	"ALTER DATABASE twitter OWNER TO twitteradmin;"
)


if [ $# != 1 ]
then
	echo "You should provide 1 and only 1 argument."
	exit
fi

if [ $1 == 'prod' ]
then
	COMPOSE_CONFIG='./docker/production.yml'
	CONTAINER_GROUP='twitter'
elif [ $1 == 'test' ]
then
	COMPOSE_CONFIG='./docker/testing.yml'
    CONTAINER_GROUP=twitter-testing
else
	echo $ARG_ERROR_MESSAGE
	exit
fi

docker compose -f $COMPOSE_CONFIG -p $CONTAINER_GROUP up -d

if [ $1 == 'test' ]
then
	sleep 2
	for i in ${!POSTGRES_COMMANDS[@]};
	do
		echo "------"
		echo "Running command: " ${POSTGRES_COMMANDS[$i]}
		psql -h 0.0.0.0 -p 8080 -U postgres -c "${POSTGRES_COMMANDS[$i]}"
	done
	pytest -s
	docker-compose -p $CONTAINER_GROUP down
fi

