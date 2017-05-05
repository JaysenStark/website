import socket
import sys

def start_hkl(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('219.223.252.218', 1300))
    msg = (str(port) + '\n').encode()
    s.send(msg)


def main():
    #start_wpc(2000)
    a =(1,2)
    print(a[0])
if __name__ == '__main__':
    main()
