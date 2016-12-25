import socketserver
import threading
import json

__author__ = 'Bartosz Kościow'


class MessageHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        event = None
        try:
            message = json.loads(data.decode())
            if 'protocol' in message \
                    and message['protocol'] == "iot:1" \
                    and 'node' in message \
                    and message['node'] == self.server.node_name:
                event = message['event']
        except ValueError:
            pass

        if event:
            print(event)
            self.server.emit_signal(event)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, address, handler, node_name, communication):
        super().__init__(address, handler)
        self.node_name = node_name
        self.communication = communication
        self.communication['close'].close.connect(self.close_socket)

    def emit_signal(self, event):
        self.communication['state'].state.emit(event)

    def close_socket(self):
        self.socket.shutdown()


def run_server(host, port, node_name, communication):
    udp_server = ThreadedUDPServer((host, port), MessageHandler, node_name, communication)
    udp_thread = threading.Thread(target=udp_server.serve_forever)
    udp_thread.start()