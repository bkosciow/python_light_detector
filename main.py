import message
import signals
import view
import socket
import json

__author__ = 'Bartosz Kościow'

HOST = ''
PORT = 5053
NODE = "light-wc"


def get_current_state():
    address = ('192.168.1.255', PORT)
    packet = {
        "protocol": "iot:1",
        "node": "computer",
        "event": "state",
        "targets": [
            NODE
        ]
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = json.dumps(packet)
    s.sendto(msg.encode(), address)
    (data, ip) = s.recvfrom(1024)
    state = "unknown"
    try:
        msg = json.loads(data.decode())
        if msg['protocol'] == "iot:1":
            state = msg['response']
    except ValueError:
        pass

    return state


def main():
    communication = {
        'state': signals.StateChange(),
        'close': signals.ExitApplication()
    }
    state = get_current_state()
    message.run_server(HOST, PORT, NODE, communication)
    view.run_gui(state, communication)

if __name__ == '__main__':
    main()