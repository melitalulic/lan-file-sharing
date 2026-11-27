from typing import Callable, Optional

from app.core.udp_discovery.receiver import Peer, UDPReceiver
from app.core.udp_discovery.sender import UDPSender


_sender: Optional[UDPSender] = None
_receiver: Optional[UDPReceiver] = None


def start_transmitting(
    device_name: str,
    port: int = 37020,
    broadcast_address: str = "255.255.255.255",
    interval: float = 2.0,
    device_id: Optional[str] = None,
) -> None:
    global _sender

    if _sender is not None:
        return

    sender = UDPSender(
        device_name=device_name,
        port=port,
        broadcast_address=broadcast_address,
        interval=interval,
        device_id=device_id,
    )
    sender.start()
    _sender = sender


def stop_transmitting() -> None:
    global _sender

    if _sender is None:
        return

    _sender.stop()
    _sender = None


def start_listening(
    on_peer_discovered: Callable[[Peer], None],
    port: int = 37020,
) -> None:
    global _receiver

    if _receiver is not None:
        return

    receiver = UDPReceiver(
        on_peer_discovered=on_peer_discovered,
        port=port,
    )
    receiver.start()
    _receiver = receiver


def stop_listening() -> None:
    global _receiver

    if _receiver is None:
        return

    _receiver.stop()
    _receiver = None
