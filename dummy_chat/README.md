## What?

A simple chat in flask. It handles a single chat window with message history. 

## Requirements

* Single chat window
* Several users
* Message History




## How to use it? 

### №1
Build the docker image:
```bash
docker build -t dummy_chat .
```
Run the docker image:
```bash
docker run -d -p 5000:5000 dummy_chat
```

And then, open your browser to http://localhost:5000/

### №2 
Build the docker image:
```bash
docker-compose up --build dummy_chat
```
Run the docker image
```bash
docker-compose run --service-ports dummy_chat
```
And then, open your browser to http://localhost:5000/

## Resources
* [The Flask Website](http://flask.pocoo.org/)
* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Docker container for Flask](http://containertutorials.com/docker-compose/flask-simple-app.html)
