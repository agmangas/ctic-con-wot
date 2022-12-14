include .env.default
export $(shell sed 's/=.*//' .env.default)

ifneq (,$(wildcard ./.env.local))
	include .env.local
	export $(shell sed 's/=.*//' .env.local)
endif

DEFAULT_GOAL: up

up: slides
	docker-compose -p ${COMPOSE_PROJECT_NAME} up -d --build

down:
	docker-compose -p ${COMPOSE_PROJECT_NAME} down -v

slides:
	cd slides && npm i && npm run build

.PHONY: up down slides
