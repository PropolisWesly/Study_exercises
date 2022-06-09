import asyncio


class ClientServerProtocol(asyncio.Protocol):
    storage = {'palm.cpu': [(2.0, 1150864247), (0.5, 1150864248)], 'eardrum.cpu': [(3.0, 1150864250)]}
    storage = {}

    @staticmethod
    def put(resp):
        if not resp.endswith('\n'):
            return 'error\nwrong command\n\n'
        resp = resp.replace('\n', '')
        resp = resp.split(' ')
        if len(resp) != 4:
            return 'error\nwrong command\n\n'
        key = resp[1]
        try:
            value = float(resp[2])
            time = int(resp[3])
        except ValueError:
            return 'error\nwrong command\n\n'
        storage = ClientServerProtocol.storage
        if not key in storage:
            storage[key] = []
        else:
            for i in range(len(storage[key])):
                if time == storage[key][i][1]:
                    storage[key].remove((storage[key][i][0], storage[key][i][1]))
                    storage[key].append((value, time))
                    return 'ok\n\n'
        if (value, time) not in storage[key]:
            storage[key].append((value, time))
        return 'ok\n\n'

    @staticmethod
    def get(resp):
        if not resp.endswith('\n'):
            return 'error\nwrong command\n\n'
        resp = resp.replace('\n', '')
        resp = resp.split(' ')
        if len(resp) != 2:
            return 'error\nwrong command\n\n'
        key = resp[1]
        out = ''
        storage = ClientServerProtocol.storage
        if key == '*':
            out = 'ok\n'
            for key in storage:
                for i in range(len(storage[key])):
                    print(storage[key][i][0], storage[key][i][1])
                    value = str(storage[key][i][0])
                    time = str(storage[key][i][1])
                    out += key + ' ' + value + ' ' + time + '\n'
            out += '\n'
            return out
        if key in storage:
            out = 'ok\n'
            for i in range(len(storage[key])):
                value = str(storage[key][i][0])
                time = str(storage[key][i][1])
                out += key + ' ' + value + ' ' + time + '\n'
            out += '\n'
            return out
        else:
            return 'ok\n\n'

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = data.decode()
        if resp.startswith('put '):
            out = ClientServerProtocol.put(resp)
        elif resp.startswith('get '):
            out = ClientServerProtocol.get(resp)
        else:
            out = 'error\nwrong command\n\n'
        print(out)
        self.transport.write(out.encode())

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    return (loop, server)

loop, server = run_server('127.0.0.1', 8281)

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()