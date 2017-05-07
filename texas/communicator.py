
class Communicator():
    ''' check, correct, send and receive msg/response between 
    player_socket and acpc server'''

    # return msg without \r\n in str type 
    # maybe handle gui or comment msg in future
    @classmethod
    def receive(cls, conn):
        s = conn
        msg = ''

        while True:
            part_msg = s.recv(1)
            msg += part_msg.decode()

            # check if full message received
            count = msg.count("\n")

            if count < 1:
                continue
            elif count == 1 and msg.endswith("\n"):
                # ignore comment message, gui message
                if msg.startswith("#") or msg.startswith(";"):
                    pass # todo
                msg = msg.strip("\r\n")
                return msg
            else:
                raise Exception


    #try to receive msg in given time, return msg or None
    @classmethod
    def try_receive(cls, conn, time):
        pass


    # support both str type and binary type msg
    @classmethod
    def send_msg(cls, conn, msg):
        if type(msg) == bytes:
            cls.send_binary_msg(msg)
        elif type(msg) == str:
            cls.send_binary_msg(conn, msg.encode())
        else:
            raise TypeError

    # only support binary msg
    # should be invoked by function send_msg()
    @classmethod
    def send_binary_msg(cls, conn, binary_msg):
        conn.send(binary_msg)


    # check and correct str type msg
    # return corrected msg
    @classmethod
    def check_format(cls, msg):
        if '\n' in msg:
            return msg.strip('\r\n')
        return msg

    # check and correct before sending msg
    @classmethod
    def check_and_send_msg(cls, conn, msg):
        cls.send_msg(conn, cls.check_format(msg))




