### Simple proxy test env with Docker

This is a small enviroment used to learn/test the Confluent REST proxy with Python and an Nginx loadbalancer

#### Starting the environment
```
docker-compose up
```

#### Set up python env
Run `setup.sh` after bringing the environment up to creat the topic and create the python virtualenv.

Run `source pythontest_env/bin/activate` to activate the environment before running the consumer/producer python.

#### Consumer/Producer
These are very simple python scripts, one produces batches of messages with sequential numbers, the other consumes and prints the messages. 
