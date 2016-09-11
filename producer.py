#!/usr/bin/env python
import requests
import logging
import time
from configparser import ConfigParser

logging.basicConfig()
logger = logging.getLogger('producer')
logger.setLevel(logging.DEBUG)

class JsonProducer(object):
    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def produce(self, topic, messages, key=None):
        headers = {
        "Content-Type": "application/vnd.kafka.json.v1+json",
        "Accept": "application/vnd.kafka.v1+json, application/vnd.kafka+json, application/json"
        }
        formatted_messages = []
        for m in messages:
            formatted_messages.append({"key": key, "value": m})

        data = {
            "records": formatted_messages
        }

        url = "http://%s:%s/topics/%s" % (self.host, self.port, topic)
        r = requests.post(url, headers=headers, json=data)
        if r.ok:
            return r.json()
        else:
            logger.error(r.text)
            return null


def main():
    message_number = 0
    batch = 25
    sleep = 1
    producer = JsonProducer("localhost")
    while(True):
        messages = []
        for number in range(0, batch):
            messages.append("message number %d" % message_number)
            message_number += 1
        response = producer.produce("testtopic", messages)
        logger.debug(response)
        time.sleep(sleep)

if __name__ == '__main__':
    main()
