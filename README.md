# LAN file sharing
An application for transferring files between devices connected to the same local network.

## About
This project aims to make file sharing easier by allowing users to send and receive files directly over a local network, without using external services. This makes file transfers faster, more convenient and doesn't require an internet connection.

## Functionalities
- Automatic discovery of devices connected to the same LAN
- Selection of a recipient for file transfers
- Sending files directly between devices
- Option to accept or reject file transfers
- Downloading files

## Architecture
The application uses a Peer-to-Peer (P2P) architecture. Devices communicate directly over the same local network without a central server.
Each device can send and receive files.

- Devices are discovered using UDP broadcast
- Files are transferred using TCP sockets.

The application consists of:
- Frontend: allows users to select devices and files
- Backend: device discovery, network communication and actual file transfers

## Technologies
### Frontend:
- Kivy
- Python
### Backend:
- Python
- Socket Programming
- TCP/IP
- UDP Broadcast

