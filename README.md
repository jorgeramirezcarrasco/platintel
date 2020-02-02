Docker commands

docker build -f ./Dockerfile -t platintel .
docker run -p 3000:3000 --env-file ./server/.env platintel:latest


Heroku Docker

heroku login
docker ps
heroku container:login
heroku container:push web -a platintel
heroku container:release web