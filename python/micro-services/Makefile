# PROJECT=project
# TAG="lghive/einston/${PROJECT}"
# REGISTRY = "scm.logichive.in:5050/einston-labs/${PROJECT}"
# GITLAB_REGISTRY_URL = scm.logichive.in:5050

# setting the GIT_BRANCH to the current branch on git
GIT_BRANCH:=$(or $(CI_COMMIT_REF_NAME), $(shell git symbolic-ref --short HEAD))

# setting the branch variable to either PROJECT_BRANCH or GIT_BRANCH, preference is given to PROJECT_BRANCH
BRANCH:=$(or $(PROJECT_BRANCH), $(GIT_BRANCH))


# Default python: 3.7
PY = py38


# prompt_example> make test PY=py35 OPTIONS="-- -s"
.PHONY: test
test:
	@tox -e $(PY) $(OPTIONS)


.PHONY: coverage
coverage:
	@tox -e coverage


.PHONY: isort
isort:
	@tox -e isort


.PHONY: lint
lint:
	@tox -e lint


# prompt_example> make bumpversion OPTIONS="-- --allow-dirty patch"
.PHONY: bumpversion
bumpversion:
	@tox -e bumpversion $(OPTIONS)


.PHONY: find_todo
find_todo:
	@grep --color=always -PnRe "(#|\"|\').*TODO" src/ || true


.PHONY: find_fixme
find_fixme:
	@grep --color=always -nRe "#.*FIXME" src/ || true


.PHONY: find_xxx
find_xxx:
	@grep --color=always -nRe "#.*XXX" src/ || true


.PHONY: count
count: clean
	@# @find src/ -type f \( -name "*.py" -o -name "*.rst" \) | xargs wc -l
	@echo "Lines of documentation:"
	@find docs/source/ -type f -name "*.rst" | xargs wc -l
	@echo "Lines of code:"
	@find src/ tests/ -type f -name "*.py" | xargs wc -l


.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@find . -type d -name '*.ropeproject' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -f src/*.egg
	@rm -f src/*.eggs
	@rm -rf src/*.egg-info/
	@rm -f MANIFEST
	@rm -rf docs/build/
	@rm -rf htmlcov/
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf .cache/
	@rm -f coverage.xml
	@rm -f *.cover
	@rm -rf .pytest_cache/


.PHONY: install-dev
install-dev:
	@pip install -e .


##### Build #####

.PHONY: build-python-source
build-python-source:
	@python setup.py sdist


##### Docker #####

.PHONY: build-docker
build-docker: clean build-python-source build-pip-dependencies _build-docker

.PHONY: build-pip-dependencies
build-pip-dependencies:
	@pip download --no-deps -d dist/ -r scm_requirements.txt



.PHONY: _build-docker
_build-docker:
	@docker build -t ${REGISTRY}:${BRANCH} -f docker/Dockerfile --build-arg https_proxy=${https_proxy} --build-arg http_proxy=${http_proxy} .

##### Docker #####

.PHONY: run-docker
run-docker:
	@docker run --rm -ti -d --name=project-${BRANCH} -p 5000:5000 ${REGISTRY}:${BRANCH}



.PHONY: kill-docker
kill-docker:
	@docker kill project-${BRANCH}

##### docker login, push to LGHIVE registry #####
# Create two new environment variable as
# GITLAB_REGISTRY_URL = scm.logichive.in:5050
# GITLAB_USERNAME= username e.g. prathikpaip
# GITLAB_PASSWORD= password

.PHONY: login-registry
login-registry:
	@docker login  ${GITLAB_REGISTRY_URL} -u ${GITLAB_USERNAME} -p ${GITLAB_PASSWORD}


.PHONY: push-registry
push-registry:
	@docker push ${REGISTRY}:${BRANCH}


##### Run #####
# App needs to be installed (can use -e)

.PHONY: run-dev-server
run-dev-server:
	@uvicorn project.app:app --host 0.0.0.0 --port 5016


.PHONY: run-server
run-server:
	@uvicorn project.app:app --host 0.0.0.0 --port 5016


##### Docs #####

.PHONY: docs-html
docs-html:
	@tox -e docs-html


.PHONY: docs-singlehtml
docs-singlehtml:
	@tox -e docs-singlehtml


.PHONY: docs-pdf
docs-pdf:
	@tox -e docs-pdf

.PHONY: code-formatter-check
code-formatter-check:
	@tox -e code-formatter-check


.PHONY: code-formatter
code-formatter:
	@tox -e code-formatter


.PHONY: generate-openapi
generate-openapi:
	@tox -e generate-openapi

.PHONY: validate-openapi
validate-openapi:
	@tox -e validate-openapi
