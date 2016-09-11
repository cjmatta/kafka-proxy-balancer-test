import unittest
from producer import JsonProducer
from consumer import JsonConsumer
from configparser import ConfigParser
from multiprocessing import Process

def produce(producer, batch, sleep):
    while(True):
        messages = []
        for number in range(0, batch):
            messages.append("message number %d" % message_number)
            message_number += 1
        response = producer.produce("testtopic", messages)
        logger.debug(response)
        time.sleep(sleep)


class TestConsumer(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser.read('balancer-test.cfg')
        self.producer = JsonProducer(
            self.confg.get('producer', 'restproxy'),
            self.config.get('producer', 'restproxy.port')
        )
        self.consumer = JsonConsumer(
            self.config.get('cosnumer', 'restproxy'),
            self.config.get('consumer', 'restproxy.port')
        )
        self.producerBatch = self.config.get('producer', 'batch.size')
        self.producerSleep = self.config.get('prodcuer', 'sleep.time')
        self.prodcuerProcess = Process(produce, args=(
            self.producer, self.producerBatch, self.producerSleep)
        )

        # Start the producer
        self.prodcuerProcess.start()
