import socket
import time


class ClientError(Exception):
    pass


class Client:

    def __init__(self, adr, port, timeout=None):
        super().__init__()
        self.adr = adr
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.adr, self.port), self.timeout)

    def put(self, name, value, timestamp=None):
        value = str(value)
        if timestamp is None:
            timestamp = int(time.time())
        timestamp = str(timestamp)
        message = b'put ' + name.encode('utf-8') + b' ' + value.encode('utf-8') + b' ' + str(timestamp).encode('utf-8') + b'\n'
        try:
            self.sock.sendall(message)
        except Exception:
            raise ClientError
        answer = self.sock.recv(1024)
        answer = answer.decode('utf-8')
        if answer != 'ok\n\n':
            raise ClientError
        print('conec')

    @staticmethod
    def _time_sort(data):
        for key_dict in data:
            data[key_dict] = sorted(data[key_dict], key=lambda metric: metric[0])
        return data

    @staticmethod
    def _dict_crt(data):
        out = {}

        if len(data) < 3:
            raise ClientError

        for i in range(1, len(data)-2):
            split_data = data[i].split(' ')

            if len(split_data) != 3:
                raise ClientError
            key = split_data[0]

            try:
                value = float(split_data[1])
            except Exception:
                raise ClientError

            try:
                timestamp = int(split_data[2])
            except Exception:
                raise ClientError

            if key not in out:
                out[key] = [(timestamp, value)]
            else:
                out[key].append((timestamp, value))
        return out

    def get(self, name):
        ask = name.encode('utf-8')
        ask = b'get ' + ask + b'\n'
        self.sock.sendall(ask)
        answer = self.sock.recv(1024)
        answer = answer.decode('utf-8')

        if answer == 'ok\n\n':
            return {}
        if not answer.startswith('ok\n'):
            raise ClientError

        data = answer.split('\n')

        dict_metr = self._dict_crt(data)
        dict_metr = self._time_sort(dict_metr)
        return dict_metr

    def close_serv(self):
        self.sock.close()


#8 cl = Client('127.0.0.1', 8888)

# cl.put('palm.cpu', 0.5, 1150864247)
# print(cl.get('cpu'))
#f = Client('127.0.0.1', 8181)
#f.put('Nitro', 89)
#f.close_serv()

p_pp = (y[j] - x[j] + 1) * (u[j] - v[j] + 1)/ (37 * 37)
	p_mp = (x[j] - 0) * (u[j] - v[j] + 1) / (37 * 37) + (36 - y[j]) * (u[j] - v[j] + 1) / (37 * 37)
	p_pm = (y[j] - x[j] + 1) * (v[j] - 0) / (37 * 37) + (y[j] - x[j] + 1) * (36 - u[j]) / (37 * 37)
	p_mm = 1 - p_pp - p_mp - p_pm
	print(p_pp)