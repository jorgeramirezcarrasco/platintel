# PlatIntel Back

Back End Project

### Prerequisites

Docker

## Deployment

Local Development

```
docker build -f ./Dockerfile -t platintel-back .

docker run -p 8000:8000 --env-file ./.env platintel-back:latest

```

Production

```

docker run -d -p 8000:8000 --env-file ./.env platintel-back:latest

heroku login

docker ps

heroku container:login

heroku container:push web -a platintel-back

heroku container:release web -a platintel-back

```

## Versioning

1.0

## Authors

- **JRC**

## License

Private
