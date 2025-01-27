# pylint: skip-file
from __future__ import absolute_import

import pytest
import io

from kafka3.client_async import KafkaClient
from kafka3.cluster import ClusterMetadata
from kafka3.metrics import Metrics
from kafka3.protocol.produce import ProduceRequest
from kafka3.producer.record_accumulator import RecordAccumulator, ProducerBatch
from kafka3.producer.sender import Sender
from kafka3.record.memory_records import MemoryRecordsBuilder
from kafka3.structs import TopicPartition


@pytest.fixture
def client(mocker):
    _cli = mocker.Mock(spec=KafkaClient(bootstrap_servers=(), api_version=(0, 9)))
    _cli.cluster = mocker.Mock(spec=ClusterMetadata())
    return _cli


@pytest.fixture
def accumulator():
    return RecordAccumulator()


@pytest.fixture
def metrics():
    return Metrics()


@pytest.fixture
def sender(client, accumulator, metrics):
    return Sender(client, client.cluster, accumulator, metrics)


@pytest.mark.parametrize(("api_version", "produce_version"), [
    ((0, 10), 2),
    ((0, 9), 1),
    ((0, 8), 0)
])
def test_produce_request(sender, mocker, api_version, produce_version):
    sender.config['api_version'] = api_version
    tp = TopicPartition('foo', 0)
    buffer = io.BytesIO()
    records = MemoryRecordsBuilder(
        magic=1, compression_type=0, batch_size=100000)
    batch = ProducerBatch(tp, records, buffer)
    records.close()
    produce_request = sender._produce_request(0, 0, 0, [batch])
    assert isinstance(produce_request, ProduceRequest[produce_version])
