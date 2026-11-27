import json
import socket
import threading
from dataclasses import dataclass
from typing import Callable, Optional


MESSAGE_TYPE = "lan-file-sharing-discovery"
PROTOCOL_VERSION = 1
MAX_MESSAGE_SIZE = 1024
RECEIVE_TIMEOUT = 0.2


@dataclass(frozen=True)
class Peer:
    device_id: str
    name: str
    address: str


def parse_announcement(data: bytes, address: str) -> Optional[Peer]:
    try:
        message = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None

    if not isinstance(message, dict):
        return None

    if message.get("type") != MESSAGE_TYPE:
        return None

    if message.get("version") != PROTOCOL_VERSION:
        return None

    device_id = message.get("device_id")
    device_name = message.get("device_name")

    if not isinstance(device_id, str) or not device_id.strip():
        return None

    if not isinstance(device_name, str) or not device_name.strip():
        return None

    return Peer(device_id, device_name, address)


class UDPReceiver:

    def __init__(
        self,
        on_peer_discovered: Callable[[Peer], None],
        port: int = 37020,
    ):
        self.port = port
        self.on_peer_discovered = on_peer_discovered
        self._stop_event = threading.Event()
        self._socket = None
        self._thread = None

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.bind(("", self.port))
            udp_socket.settimeout(RECEIVE_TIMEOUT)
        except OSError:
            udp_socket.close()
            raise

        self._socket = udp_socket
        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._receive,
            daemon=True
        )
        self._thread.start()

    def _receive(self):
        while not self._stop_event.is_set():
            try:
                data, sender = self._socket.recvfrom(MAX_MESSAGE_SIZE)
            except socket.timeout:
                continue

            peer = parse_announcement(data, sender[0])

            if peer is not None:
                self.on_peer_discovered(peer)

    def stop(self):
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join()

        if self._socket is not None:
            self._socket.close()

        self._socket = None
        self._thread = None
