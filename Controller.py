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


def collisionDetection(p1, body):
    for line in body:
        if distance(p1, [line.x1, line.y1]) + distance(p1, [line.x2, line.y2]) == distance([line.x2, line.y2], [line.x1, line.y1]):
            return True
    return False


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

    def greedyAgent(self, head, food):

        # Don't move into any snakeLocation
        # snakeLocation = []
        # for part in self.state.body:
        #     snakeLocation.append(tuple([part.x1, part.y1]))
        #     snakeLocation.append(tuple([part.x2, part.y2]))
        #     if part.x1 == part.x2:
        #         for i in range(part.y1, part.y2):
        #             snakeLocation.append(tuple([part.x1, i]))
        #     else:
        #         for i in range(part.x1, part.x2):
        #             snakeLocation.append(tuple([i, part.y1]))

        # Move to the closest food
        position = [head.x1, head.y1]

        minDistance = math.inf
        currentBestAction = None

        for i, action in enumerate(getStates(position, self.opMap)):
            currentDistance = distance(action, food)
            print(minDistance)
            if not collisionDetection(action, self.state.body) and currentDistance < minDistance:
                print(currentDistance)
                minDistance = currentDistance
                currentBestAction = i

        return self.ops[currentBestAction]

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
            self.networkMgr.sendCommand(self.greedyAgent(
                self.state.body[0], self.state.food))


cntrl = Controller()
cntrl.control()
