.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		   Run App"
	@echo "  debug 	       Run with stacktrace"
	@echo "  stop          Stop docker-compose"
	@echo "  lint		   Reformat code & check with flake8, pyright"
	@echo "  requirements  Export poetry.lock to requirements.txt"

.PHONY:	black
black:
	poetry run black app/

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
.PHONY: debug
debug:
	docker-compose up --force-recreate ${MODE}

.PHONY: run
run:
	docker-compose up -d ${MODE}

.PHONY: stop
stop:
	docker-compose down --remove-orphans ${MODE}
