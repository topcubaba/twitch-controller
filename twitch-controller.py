import socket
from emoji import demojize
import keyboard
import time
from apscheduler.schedulers.background import BackgroundScheduler


class Twitch:
    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.token = 'oauth:youroauthtoken'
        self.channel = '#yourchannel'
        self.nickname = 'yournickname'

        self.sched = BackgroundScheduler()

        self.sock = socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))

        self.voteDict = {"null": 0, "fwd": 0, "rev": 0, "left": 0, "right": 0}

        self.sched.add_job(self.voteCount, 'interval', seconds=2) # vote interval
        self.sched.start()

    def loop(self):

        while True:
            resp = self.sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                rCln = demojize(resp)
                print(rCln)
                msgComponents = rCln.split(" ", 3)

                msgUser = msgComponents[0]  # get username
                msgUser = msgUser[msgUser.find(':') + 1: msgUser.find('!')]
                msgContent = msgComponents[3]  # print message
                
                # vote
                if msgContent.find("forward") >= 0:
                    self.voteDict["FWD"] = self.voteDict["FWD"] + 1
                if msgContent.find("reverse") >= 0:
                    self.voteDict["REV"] = self.voteDict["REV"] + 1
                if msgContent.find("left") >= 0:
                    self.voteDict["LEFT"] = self.voteDict["LEFT"] + 1
                if msgContent.find("right") >= 0:
                    self.voteDict["RIGHT"] = self.voteDict["RIGHT"] + 1

    def voteCount(self):
        print('Counting votes and executing command')
        voteWinner = max(self.voteDict, key=self.voteDict.get)
        print("biggest vote:" + voteWinner)
        nullCheck = all(x == 0 for x in self.voteDict.values())

        if nullCheck:
            print('doing nothing')

            # COMMANDS
        elif voteWinner == "FWD":
            print('FORWARD!')
            keyboard.press('w')
            time.sleep(2) # command interval
            keyboard.release('w')
        elif voteWinner == "REV":
            print('REVERSE!')
            keyboard.press('s')
            time.sleep(2) # command interval
            keyboard.release('s')
        elif voteWinner == "LEFT":
            print('LEFT!')
            keyboard.press('a')
            time.sleep(2) # command interval
            keyboard.release('a')
        elif voteWinner == "RIGHT":
            print('RIGHT!')
            keyboard.press('d')
            time.sleep(2) # command interval
            keyboard.release('d')
        self.voteDict = {"null": 0, "FWD": 0, "REV": 0, "LEFT": 0, "RIGHT": 0}  # reset votes

    def close(self):
        self.sched.shutdown()

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        self.close()


def main(argv=None):
    Twitch().loop()


main()
