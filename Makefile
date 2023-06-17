#!make

.PHONY: help env init_linters up stop rm rmv rmi logs sh lint test

# --- Application virtual environment settings (can be changed)
env_file_name := .env
env_snippet_repo := git@github.com:d3b0c0b8e69f2ad215a15d3c0eb7b12f.git

# --- Application settings
default_env_file_name := .env
env_clone_dir := env_gist_temp

# --- Docker
compose := docker compose -f docker-compose-local.yml


help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "    up               Run docker containers"
	@echo "    stop             Stop docker containers"
	@echo "    rm               Stop and remove docker containers"
	@echo "    rmv              Stop and remove docker containers with their volumes"
	@echo "    rmi              Stop and remove docker containers with their images and volumes"
	@echo "    logs             Stdout logs from docker containers"
	@echo "    sh SERVICE       Run the command line in the selected SERVICE docker container"
	@echo "    lint             Run linting"
	@echo "    test             Run tests for the API service"


env:
	@if [ ! -f $(default_env_file_name) ]; then \
  		git clone  $(env_snippet_repo) $(env_clone_dir) && \
  		mv $(env_clone_dir)/$(env_file_name) ./$(default_env_file_name) && \
  		rm -rf $(env_clone_dir); \
  	fi
  	env_arg := --env-file $(default_env_file_name)

init_linters:
	@pre-commit install

up: env
	@$(compose) $(env_arg) up -d

stop: env
	@$(compose) $(env_arg) stop

rm: env
	@$(compose) $(env_arg) down

rmv:
	@$(compose) $(env_arg) down -v

rmi: env
	@$(compose) $(env_arg) down --rmi all -v

logs:
	@$(compose) logs -f

sh: up
	@docker exec -it $(firstword $(filter-out $@,$(MAKEOVERRIDES) $(MAKECMDGOALS))) sh

lint: init_linters
	@pre-commit run -a

test: up
	@docker exec -it api pytest
