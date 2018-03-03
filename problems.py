import socketserver
import hashlib
import time
import random
import string
import operator
import parser
import codecs

# defined as a global as this string is referenced in two problems
JUST_ASK_PASS = "clock"

class ProblemBase(socketserver.BaseRequestHandler):
    """
    This class implements functionality that all problems can utilize. It should be extended
    for all tcp based problems.
    """

    def setup(self):
        return socketserver.BaseRequestHandler.setup(self)

    # handle hook could go here

    def finish(self):
        return socketserver.BaseRequestHandler.finish(self)

    def get_flag(self, flag):
        """
        Encode the passed in flag as sha1
        """
        return hashlib.sha1(flag.encode()).hexdigest()

    def send(self, text):
        """
        Send text to the user
        """
        self.request.sendall(text.encode());

    def send_flag(self, flag):
        """
        Send the flag to the user

        Optionally, this function can be used as a future hook to execute additional
        actions once a user has completed a challenge. 
        """
        self.send("Congratulations!\nYour flag is: " + self.get_flag(flag) + '\n')

        # this can hook into other logic to handle a user completing a challenge
        print("%s just completed %s!" % (self.client_address[0], self.__class__.__name__))

    def receive(self, num_bytes=1024):
        """
        Receive data from the user
        """
        return self.request.recv(num_bytes).strip().decode()

    def random_string(self, char_count, digits=True):
        """
        Generage a random string of length char_count, optionally including numbers
        """
        choice_str = string.ascii_lowercase + string.ascii_uppercase
        if digits:
            choice_str += string.digits
        return ''.join(random.choice(choice_str) for _ in range(char_count))

    def timed_receive(self, buffer_size=1024):
        """
        Get a response from the user, and additionally return the time it took for the user
        to send back data.
        """
        start = time.time()
        response = self.receive(buffer_size)
        end = time.time() - start

        return response, end


class GiveFlag(ProblemBase):

    def handle(self):
        flag = "kitten"
        self.send_flag(flag)

class JustAsk(ProblemBase):

    def handle(self):
        # only modifiy this flag from the globabl var
        flag = JUST_ASK_PASS

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

        response, time_taken = self.timed_receive()

        if time_taken < 0.1:
            if response == rand_string.encode():
                self.send_flag(flag)
            else:
                self.send("Incorrect.\n")
        else:
            self.send("Took too long!\n")

class SocketTotal(ProblemBase):
    """
    This class does not implement a handle method and should not be used directly
    as a problem. Instead it should be extended so that the generate_expression method
    can be used in the preceeding problems.
    """

    def generate_expression(self, ops, count=None):
        rng = None
        if count:
            rng = range(0, count)
        else:
            rand = random.randint(25, 250)
            rng = range(0, rand)

        rand_list = [random.randint(1, 100) for x in rng]
        rand_str = ""

        for i, num in enumerate(rand_list):
            rand_operator = random.choice(list(ops.keys()))

            if i != len(rand_list)-1:
                rand_str += "%s %s " % (num, rand_operator)
            else:
                rand_str += "%s" % num
                
        expr = parser.expr(rand_str)
        total = eval(expr.compile())

        return rand_str, total

class SocketTotalStatic(SocketTotal):

    def handle(self):
        flag = "mothdesksaucepan"

        operators = {'+': operator.add}
        rand_str, total = self.generate_expression(operators, 5)

        self.send("Evaluate the following expression within .1 seconds:\n%s\n" % rand_str)
        response, time_taken = self.timed_receive()

        if time_taken < .1:
            if int(response) == total:
                self.send_flag(flag)
            else:
                self.send("Incorrect.\n")
        else:
            self.send("Took too long!\n")
                
class SocketTotalRandom(SocketTotal):

    def handle(self):
        flag = "tallunderfrying"

        operators = { '+': operator.add }
        rand_str, total = self.generate_expression(operators)

        self.send("Evaluate the following expression within .1 seconds:\n%s\n" % rand_str)
        response, time_taken = self.timed_receive()

        if time_taken < .1:
            if int(response) == total:
                self.send_flag(flag)
            else:
                self.send("Incorrect.\n")
        else:
            self.send("Took too long!\n")


class SocketTotalRandomOps(SocketTotal):

    def handle(self):
        flag = "tallunderfrying"

        operators = { '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv }
        rand_str, total = self.generate_expression(operators)

        self.send("Evaluate the following expression within .1 seconds:\n%s\n" % rand_str)
        response, time_taken = self.timed_receive()

        if time_taken < .1:
            if int(response) == total:
                self.send_flag(flag)
            else:
                self.send("Incorrect.\n")
        else:
            self.send("Took too long!\n")


class ROT13(ProblemBase):

    def handle(self):
        flag = "noneedforencryptionwithrot13"
                
        rand_string = self.random_string(25, False)
        self.send("Send back the ROT13 encoding of the following string within .1 seconds: %s\n" % rand_string)

        encoded_string = codecs.encode(rand_string, 'rot_13')

        response, time_taken = self.timed_receive()
        if end < 0.1:
            if response == encoded_string:
                self.send_flag(flag)
            else:
                self.send("Incorrect.\n")
        else:
            self.send("Took too long!\n")


class BadPassword(ProblemBase):

    def handle(self):
        flag = "shortpasswordsareeasytoremember"

        self.send("The plaintext password of the 'Just Ask' problem had a password that can be found in /usr/share/dict/words. Send that plaintext password to receive a flag.\n")

        while True:
            response = self.receive()

            # if user disconnects, break the loop to avoid broken pipe
            if len(response) == 0:
                break

            # keep asking for JUST_ASK_PASS until the value is given
            if response == JUST_ASK_PASS:
                self.send_flag(flag)
                break
            else:
                self.send("Wrong password.\n")

# tcp_problems dict:
# key: the tcp port to run the problem on
# value: reference to the class the problem is implemented in
tcp_problems = {
        8000: GiveFlag,
        8010: JustAsk,
        8020: RepeatAfterMe,
        8030: SocketTotalStatic,
        8040: SocketTotalRandom,
        8050: SocketTotalRandomOps,
        8060: ROT13,
        8070: BadPassword
        }

udp_problems = {} # functionality not yet built for the server to start up UDP based problems

