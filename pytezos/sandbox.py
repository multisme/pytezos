import atexit
from functools import wraps
from operator import contains
from time import sleep
from pytezos.client import PyTezosClient
import unittest
from abc import abstractmethod
from typing import Optional
from requests.exceptions import ConnectionError

from testcontainers.core.generic import DockerContainer  # type: ignore


# NOTE: Container object is a singleton which will be used in all tests inherited from class _SandboxedNodeTestCase and stopped after
# NOTE: all tests are completed.
node_container: Optional[DockerContainer] = None
node_container_client: PyTezosClient = PyTezosClient()


class _SandboxedNodeTestCase(unittest.TestCase):
    IMAGE = 'bakingbad/sandboxed-node:v8.2-2'

    @classmethod
    def get_node_url(cls) -> str:
        container = cls.get_node_container()
        container_id = container.get_wrapped_container().id
        host = container.get_docker_client().bridge_ip(container_id)
        return f'http://{host}:8732'

    @classmethod
    def get_node_container(cls) -> DockerContainer:
        if node_container is None:
            raise RuntimeError('Sandboxed node container is not running')
        return node_container

    @classmethod
    def get_client(cls):
        return node_container_client.using(
            shell=cls.get_node_url(),
        )

    @classmethod
    def _create_node_container(cls) -> DockerContainer:
        return DockerContainer(
            cls.IMAGE,
        )

    @classmethod
    def setUpClass(cls) -> None:
        global node_container
        if not node_container:
            node_container = cls._create_node_container()
            node_container.start()
            cls._wait_for_connection()
            atexit.register(node_container.stop)

    @classmethod
    def _wait_for_connection(cls) -> None:
        client = cls.get_client()
        while True:
            try:
                client.shell.node.get("/version/")
                break
            except ConnectionError:
                sleep(0.1)
