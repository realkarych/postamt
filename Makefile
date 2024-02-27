.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Run App (production)"
	@echo "  debug		Run with stacktrace"
	@echo "  stop		Stop docker-compose"
	@echo "  build		Run with stacktrace"
	@echo "  lint		Reformat code & check with flake8, pyright"
	@echo "  requirements	Export poetry.lock to requirements.txt"

.PHONY:	black
black:
	poetry run black --line-length 119 app/

.PHONY: flake
flake:
	poetry run flake8 app/

.PHONY: flake
pyright:
	poetry run pyright app/

.PHONY: lint
lint: black flake pyright

# Poetry and environments utils
REQUIREMENTS_FILE := requirements.txt

.PHONY: requirements
requirements:
	# Export poetry.lock to requirements.txt if needed
	poetry check
	poetry export -o ${REQUIREMENTS_FILE} --without-hashes


# Alembic utils
.PHONY: generate
generate:
	source .env
	poetry run alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	source .env
	poetry run alembic upgrade head

# Docker utils
.PHONY: build
build:
	docker compose build ${MODE}

.PHONY: debug
debug:
	docker compose down --remove-orphans ${MODE}
	docker rmi postamt-bot
	docker compose build ${MODE}
	docker compose up --force-recreate ${MODE}

.PHONY: run
run:
	docker compose up -d ${MODE}

.PHONY: stop
stop:
	docker compose down --remove-orphans ${MODE}
