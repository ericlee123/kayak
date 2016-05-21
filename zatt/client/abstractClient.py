import socket
import json


class AbstractClient:
    def _request(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.target)
        sock.send(str(json.dumps(message)).encode())

        buff = bytes()
        while True:
            block = sock.recv(128)
            if not block:
                break
            buff += block
        resp = json.loads(buff.decode('utf-8'))
        sock.close()
        if 'type' in resp and resp['type'] == 'redirect':
            self.target = tuple(resp['leader'])
            print('redirected to', self.target)
            resp = self._request(message)
        return resp

    @property
    def diagnostic(self):
        return self._request({'type': 'diagnostic'})

    def get_state(self):
        """Retrive remote state machine"""
        return self._request({'type': 'get'})

    def append_log(self, payload):
        """Append to remote log"""
        self._request({'type': 'append', 'data': payload})
        self.get_state()

    def config_cluster(self, action, address, port):
        self._request({'type': 'config', 'action': action,
                       'address': address, 'port': port})
