# shorte

Shorte is a url shortener service for making long urls... short.

# Setup

- Install docker for your platform
- git clone the project
- cd to root directory
- run docker-compose up

```bash
docker-compose up
```

- then go to localhost/index in your browser
- ???
- profit

# Tests

- Run docker-compose up if you haven't done it already
- Open new terminal window
- run this command

```bash
docker exec -it backend_1 /bin/bash -c "pytest --cov=./"
```

- This command will also show the test coverage
