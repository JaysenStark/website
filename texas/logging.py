import logging

def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    filename = './texas/log/' + name + '.log'
    ch = logging.FileHandler(filename, mode='a')
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
