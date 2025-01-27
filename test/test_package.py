class TestPackage:
    def test_top_level_namespace(self):
        import kafka3 as kafka1
        assert kafka1.KafkaConsumer.__name__ == "KafkaConsumer"
        assert kafka1.consumer.__name__ == "kafka.consumer"
        assert kafka1.codec.__name__ == "kafka.codec"

    def test_submodule_namespace(self):
        import kafka3.client_async as client1
        assert client1.__name__ == "kafka.client_async"

        from kafka3 import client_async as client2
        assert client2.__name__ == "kafka.client_async"

        from kafka3.client_async import KafkaClient as KafkaClient1
        assert KafkaClient1.__name__ == "KafkaClient"

        from kafka3 import KafkaClient as KafkaClient2
        assert KafkaClient2.__name__ == "KafkaClient"

        from kafka3.codec import gzip_encode as gzip_encode1
        assert gzip_encode1.__name__ == "gzip_encode"

        from kafka3.codec import snappy_encode
        assert snappy_encode.__name__ == "snappy_encode"
