from flask import Flask
import redis
app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/')
def hello():
	redis_client.incr('compteur')
	count = redis_client.get('compteur')
	return "Nombre de fois consulté : {"+count+"}"
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)



"""
--  setup.py

from setuptools import setup, find_packages

setup(
    name='python_redis_simple_app',
    version='1.0.0',
    py_modules=['app'],
    install_requires=[
        'Flask',
        'redis',
    ],
    entry_points={
        'console_scripts': [
            'mon_app=app:app',
        ],
    },
    author='Votre Nom',
    description='Une application Flask utilisant Redis pour compter le nombre de fois qu\'elle est consultée.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

--  Dockerfile

# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /



--  gitlab-ci.yaml 

variables:
  USERNAME: pr-tcwsvndq-communautedesrefer
  PASSWORD: tcKE61uTMhs6NBlVMg_!G4e_2p+imvoFayW8
stages:
  - sonarqube-check
  - build
  - deploy

# Define a cache to speed up the SonarQube Scanner installation
cache:
  key: "${CI_JOB_NAME}"
  paths:
    - .sonar/cache

sonarqube-check:
  stage: sonarqube-check
  image:
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"  # Defines the location of the analysis task cache
    GIT_DEPTH: "0"  # Tells git to fetch all the branches of the project, required by the analysis task
    # SonarQube variables (used in the sonar-scanner command)
    SONAR_TOKEN: "sqp_563da1a7ecb72760e20eb3c06170379a4f5d2c1e"
    SONAR_HOST_URL: "https://sqaas.dos.tech.orange"
    BRANCH_NAME: "${BRANCH_NAME}"
  script:
    - sonar-scanner -Dsonar.login=$SONAR_TOKEN -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.branch.name=$BRANCH_NAME -X
  allow_failure: true
    
before_script:
  - curl -fL https://getcli.jfrog.io | sh  

build_flask_app:
  stage: build
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pip install setuptools wheel
    - python setup.py sdist bdist_wheel  
  artifacts:
    paths:
      - dist/ # Directory containing the generated artifacts
    name: "app_pr_V-${CI_COMMIT_SHA}"

deploy:
  image: python:latest
  stage: deploy
  before_script:
    - export JFROG_CLI_OFFER_CONFIG=false
  script:
    #deploy tar.gz
    - curl -u "$USERNAME:$PASSWORD" -X PUT "https://repos.tech.orange:443/artifactory/communaute-des-refer-local-pypi-stable/app_pr_version-${CI_COMMIT_SHA}.tar.gz/" -T dist/*.tar.gz
    #deploy whl
    - curl -u "$USERNAME:$PASSWORD" -X PUT "https://repos.tech.orange:443/artifactory/communaute-des-refer-local-pypi-stable/app_pr_version-${CI_COMMIT_SHA}.whl/" -T dist/*.whl
  only:
    - developer



--  sonar-project.properties	

sonar.projectKey=crt-devops-gr_python_ex1_AYlzYMU9FhmrILXu8XVW
sonar.qualitygate.wait=true



--  scrap data crypto

import requests
import time

def scrape_crypto_prices():
    # Replace 'YOUR_API_KEY' with your actual Cryptocompare API key
    api_key = 'befcc3e92a381c3512ec6186850db4e076be653e909abebc624d40b6d42e6fca'

    # Cryptocurrency symbols you want to track (e.g., BTC, ETH, XRP)
    symbols = ['BTC', 'LTC', 'ETH', 'DOGE', 'ADA', 'DOT', 'BCH', 'XRP']

    try:
        for symbol in symbols:
            url = f'https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD&api_key={api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                price = data['USD']
                print(f'{symbol}: ${price}')
            else:
                print(f'Error: Unable to fetch data for {symbol}. Status code: {response.status_code}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')

while True:
    scrape_crypto_prices()
    # Sleep for a specific interval (e.g., 1 minute)
    time.sleep(60)
    print()
    print('-'*15)
    print()



"""