
import json
import socket
import threading
import uuid
from typing import Optional


MESSAGE_TYPE = "lan-file-sharing-discovery"
PROTOCOL_VERSION = 1


class UDPSender:

    def __init__(
        self,
        device_name: str,
        port: int = 37020,
        broadcast_address: str = "255.255.255.255",
        interval: float = 2.0,
        device_id: Optional[str] = None,
    ):
        self.device_name = device_name
        self.device_id = device_id or str(uuid.uuid4())
        self.port = port
        self.broadcast_address = broadcast_address
        self.interval = interval
        self._stop_event = threading.Event()
        self._socket = None
        self._thread = None

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except OSError:
            udp_socket.close()
            raise

        self._socket = udp_socket
        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._send,
            daemon=True
        )
        self._thread.start()

    def _send(self):
        announcement = json.dumps({
            "type": MESSAGE_TYPE,
            "version": PROTOCOL_VERSION,
            "device_id": self.device_id,
            "device_name": self.device_name,
        }).encode("utf-8")

        while not self._stop_event.is_set():
            self._socket.sendto(
                announcement,
                (self.broadcast_address, self.port)
            )

            self._stop_event.wait(self.interval)

    def stop(self):
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join()

        if self._socket is not None:
            self._socket.close()

        self._socket = None
        self._thread = None
