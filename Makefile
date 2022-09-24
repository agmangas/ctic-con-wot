include .env.default
export $(shell sed 's/=.*//' .env.default)

ifneq (,$(wildcard ./.env.local))
	include .env
	export $(shell sed 's/=.*//' .env.local)
endif

DEFAULT_GOAL: up

up:
	docker-compose -p ${COMPOSE_PROJECT_NAME} up -d --build

down:
	docker-compose -p ${COMPOSE_PROJECT_NAME} down -v

.PHONY: up down
