# PlatIntel Front

Front End Project

### Prerequisites

Docker

## Deployment

Local Development

```

docker build -f ./Dockerfile -t platintel-front .

docker run -p 5000:5000 platintel-front:latest

```

Production

```

docker run -d -p 5000:5000 platintel-front:latest

heroku login

docker ps

heroku container:login

heroku container:push web -a platintel

heroku container:release web -a platintel

```

## Versioning

1.0

## Authors

- **JRC**

## License

Private
