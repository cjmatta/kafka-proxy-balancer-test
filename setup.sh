TOPIC_NAME=testtopic
# Create Topic if required
topic_exists() {
  docker exec kafkaproxybalancertest_kafka-1_1 kafka-topics --zookeeper zookeeper-1:2181 --list | grep -q $1
}
if ! topic_exists $TOPIC_NAME;then
  echo "Creating topic ${TOPIC_NAME}"
  docker exec kafkaproxybalancertest_kafka-1_1 kafka-topics \
    --zookeeper zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181 \
    --replication-factor 3 --create --partitions 6 --topic $TOPIC_NAME
fi

#Python environment
PYTHON_VENV_DIR=pythontest_env
if ! [[ -d $PYTHON_VENV_DIR ]]; then
  virtualenv -p $(which python) $PYTHON_VENV_DIR
  source $PYTHON_VENV_DIR/bin/activate
  pip install -r python_requirements.txt
fi

echo "Now run the following to run python env:"
echo "    source ${PYTHON_VENV_DIR}/bin/activate"
