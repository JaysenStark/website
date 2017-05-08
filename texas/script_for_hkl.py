import socket
import sys

def start_hkl(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('219.223.252.218', 1300))
    msg = (str(port) + '\n').encode()
    s.send(msg)


def main():
    pass
    
if __name__ == '__main__':
    main()
