
import random

def generate_ports(number=2):
    ports = []
    while True:
        for i in range(number):
            ports.append(random.randint(1025, 10000))
        if len(set(ports)) == number:
            break
    return ports

