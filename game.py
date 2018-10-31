import time
import random
from osbrain import run_agent
from osbrain import run_nameserver


def initGame(self):
    self.sticks = 20


def removeSticks(self, toTake):
    if self.sticks >= toTake:
        self.sticks = self.sticks - toTake
        return True
    else:
        return False


def get_sticks(self):
    return self.sticks


def replyToref(agent, message):
    r = random.choice(list(range(1, min(3, message) + 1)))
    agent.log_info(r)
    return r


if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    referee = run_agent('Referee')
    player1 = run_agent('Player1')
    player2 = run_agent('Player2')

    # System configuration
    referee.set_method(initGame, removeSticks, get_sticks)

    player1_role = player1.bind('REP', alias='p1r', handler=replyToref)
    player2_role = player2.bind('REP', alias='p2r', handler=replyToref)
    referee.connect(player1_role, alias='p1r')
    referee.connect(player2_role, alias='p2r')
    referee.initGame()
    referee.log_info('Game started!')
    p1turn = True

    while referee.get_sticks() > 0:

        print(referee.get_sticks())
        time.sleep(1)

        if p1turn:
            referee.send('p1r', referee.get_sticks())
            referee.removeSticks(referee.recv('p1r'))
        else:
            referee.send('p2r', referee.get_sticks())
            referee.removeSticks(referee.recv('p2r'))

        p1turn = not p1turn

    if p1turn:
        referee.log_info('player 1 WINS!')
    else:
        referee.log_info('player 2 WINS!')

    ns.shutdown()
