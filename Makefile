.PHONY: all pip clean test deploy

all: env pip

env:
	virtualenv env -p `which python3`

pip: requirements.txt
	env/bin/pip install -r requirements.txt

test: all
	env/bin/python3 -m unittest discover

clean:
	rm -rf .env

deploy: all
	env/bin/python3 ./deploy.py

