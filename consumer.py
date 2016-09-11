#!/usr/bin/env python
import requests
import logging
import time

logging.basicConfig()
logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)

class JsonConsumer(object):
    def __init__(self, restproxy, port, consumergroup, messageformat, autooffset="smallest", autocommit="true"):
        self.restproxy = restproxy
        self.port = port
        self.consumergroup = consumergroup
        self.format = messageformat
        self.autooffset = autooffset
        self.autocommit = autocommit
        self.base_uri = None
        self.instance_id = None
        headers = {"Content-Type": "application/vnd.kafka.v1+json"}
        url = "http://%s:%s/consumers/%s" % (self.restproxy, self.port, self.consumergroup)

        data = {
            "format": self.format,
            "auto.offset.reset": self.autooffset,
            "auto.commit.enable": self.autocommit
        }

        r = requests.post(url, headers=headers, json=data)
        if not r.ok:
            r.raise_for_status
        else:
            logger.debug(r.json())
            self.base_uri = r.json()["base_uri"]
            self.instance_id = r.json()["instance_id"]

    def consume(self, topic):
        headers = {"Accept": "application/vnd.kafka.json.v1+json"}
        logger.debug("Getting messages from %s" % self.base_uri)
        r = requests.get(self.base_uri + "/topics/%s" % topic, headers=headers)
        logger.debug("Response Status: %s" % r.status_code)
        if not r.ok:
            r.raise_for_status
        else:
            return r.json()

    def offsets(self):
        url = "http://%s:%s/consumers/%s/instances/%s/offsets" % (
        self.restproxy, self.port, self.consumergroup, self.instance_id)
        headers = {"Accept": "application/vnd.kafka.json.v1+json"}
        r = requests.post(url, headers=headers)

        if not r.ok:
            r.raise_for_status
        else:
            return r.json()

    def remove_consumer_group(self):
        pass


def main():
    myConsumer = JsonConsumer("localhost", 80, "default_consumer", "json")
    while(True):
        data = myConsumer.consume("testtopic")
        for message in data:
            print message["value"]
        time.sleep(5)

if __name__ == '__main__':
    main()
