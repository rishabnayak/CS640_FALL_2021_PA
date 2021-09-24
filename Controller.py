import numpy as np
from NetworkManager import NetworkManager
from EnvironmentState import State
from collections import deque
import math
import time

LEFT = bytes.fromhex('00')
UP = bytes.fromhex('01')
RIGHT = bytes.fromhex('02')
DOWN = bytes.fromhex('03')
NOOP = bytes.fromhex('04')


def distance(p1, p2):
    return math.sqrt(np.sum(np.square(np.subtract(p1, p2))))


def getStates(currentState, opMap):
    head = np.array([currentState[0], currentState[1]])
    return [head+opMap[op] for op in opMap.keys()]


class Controller:

    def __init__(self, ip='localhost', port=4668):
        # Do not Modify
        self.networkMgr = NetworkManager()
        State.col_dim, State.row_dim = self.networkMgr.initiateConnection(
            ip, port)  # Initialize network manager and set environment dimensions
        self.state = State()  # Initialize empty state
        self.myInit()  # Initialize custom variables

    # define your variables here
    def myInit(self):
        self.opMap = {LEFT: [-1, 0], RIGHT: [1, 0], UP: [0, -1], DOWN: [0, 1]}
        self.ops = list(self.opMap.keys())

    def algo(self, head, food):
        openList = deque()
        closedList = []
        for part in self.state.body[1:]:
            closedList.append(tuple([part.x1, part.y1]))
            closedList.append(tuple([part.x2, part.y2]))
            if part.x1 == part.x2:
                for i in range(part.y1, part.y2):
                    closedList.append(tuple([part.x1, i]))
            else:
                for i in range(part.x1, part.x2):
                    closedList.append(tuple([i, part.y1]))
        gScore = {tuple(head): 0}
        fScore = {tuple(head): distance(head, food)}
        openList.append(head)
        current = openList.popleft()
        cost = []
        for next in getStates(current, self.opMap):
            if tuple(next) in closedList:
                cost.append(math.inf)
                continue
            tentativeGScore = gScore[tuple(current)] + 1
            if tuple(next) not in gScore or tentativeGScore < gScore[tuple(next)]:
                gScore[tuple(next)] = tentativeGScore
                fScore[tuple(next)] = tentativeGScore + \
                    distance(next, food)
                cost.append(tentativeGScore + distance(next, food))
                openList.append(next)
            else:
                cost.append(math.inf)
        print(cost)
        self.networkMgr.sendCommand(self.ops[np.argmin(cost)])
        closedList.append(tuple(current))

    def control(self):
        # Do not modify the order of operations.
        # Get current state, check exit condition and send next command.
        while(True):
            # 1. Get current state information from the server
            self.state.setState(self.networkMgr.getStateInfo())
            # 2. Check Exit condition
            if self.state.food == None:
                break
            # 3. Send next command
            self.algo(np.array([self.state.body[0].x1,
                                self.state.body[0].y1]), self.state.food)


cntrl = Controller()
cntrl.control()
