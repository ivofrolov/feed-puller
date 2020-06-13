TAG = feedpuller
DOCKER_RUN = docker run -v $$PWD:/usr/src/app --rm ${TAG}

help: 
	# see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-10s %s\n", $$1, $$2}'

spider: ## generate new spider using template
	${DOCKER_RUN} scrapy genspider -t feedpull ${SPIDER} ${DOMAIN}

crawl: ## run spider
	${DOCKER_RUN} scrapy crawl ${SPIDER} -a deltafetch_reset=1

deploy: ## deploy project to scrapyd instance
	${DOCKER_RUN} scrapyd-deploy
	ls -1 | grep -x -e build -e project.egg-info -e setup.py | xargs rm -r

build: ## build docker image
	docker build --force-rm -t ${TAG} .

clean: ## remove python cache
	find . \( -name \*.pyc -or -name \*.pyo -or -name __pycache__ \) -delete

.PHONY .SILENT: help spider crawl deploy build clean