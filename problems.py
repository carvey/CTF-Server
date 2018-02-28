import socketserver
import hashlib
import time
import random
import string


class ProblemBase(socketserver.BaseRequestHandler):

    def setup(self):
        return socketserver.BaseRequestHandler.setup(self)

    # handle hook could go here

    def finish(self):
        return socketserver.BaseRequestHandler.finish(self)

    def get_flag(self, flag):
        return hashlib.sha1(flag.encode()).hexdigest()

    def send(self, text):
        self.request.sendall(text.encode());

    def send_flag(self, flag):
        self.send("Congratulations!\nYour flag is: " + self.get_flag(flag) + '\n')

        # this can hook into other logic to handle a user completing a challenge
        print("%s just completed %s!" % (self.client_address[0], self.__class__.__name__))

    def receive(self, bytes=1024):
        return self.request.recv(1024).strip()

    def random_string(self, char_count):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(char_count))

    def start_timer(self):
        """
        Just making a method for this to simplify the timing process along with a stop_timer method
        """
        return time.time()

    def stop_timer(self, start):
        end = time.time()
        return end-start


class GiveFlag(ProblemBase):

    def handle(self):
        flag = "kitten"
        self.send_flag(flag)

class AskForFlag(ProblemBase):

    def handle(self):
        flag = "toasteroven"

        self.send("Send back the following text to receive a flag: 'Give me flag.'\n")
        response = self.receive() 

        if response == b"Give me flag.":
            self.send_flag(flag)
        else:
            self.send("Incorrect.\n")

class RepeatAfterMe(ProblemBase):

    def handle(self):
        flag = "toasterairplanescooter"

        rand_string = self.random_string(17)
        self.send("Send back the following random string within .1 seconds: %s\n" % rand_string)

        start = self.start_timer()
        response = self.receive()
        end = self.stop_timer(start)

        print(end)
        if end < 0.1:
            if response == rand_string.encode():
                self.send_flag(flag)
            else:
                self.send("Incorrect.\n")
        else:
            self.send("Took too long!\n")


        
tcp_problems = {9000: GiveFlag, 9010: AskForFlag, 9020: RepeatAfterMe}
udp_problems = {}

