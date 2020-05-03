Docker commands from source folder

docker build -f ./Dockerfile -t platintel-back .
docker run -p 8000:8000 --env-file ./.env platintel-back:latest

OR

docker run -d -p 8000:8000 --env-file ./.env platintel-back:latest

Heroku Docker

heroku login
docker ps
heroku container:login
heroku container:push web -a platintel-back
heroku container:release web -a platintel-back
