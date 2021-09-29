import numpy as np
from NetworkManager import NetworkManager
from EnvironmentState import State
from collections import deque
import math
import time
import heapq
from itertools import count

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
        # self.border =[]
        # for i in range(0, 400):
        #     if i <301:
        #         self.border.append(str([0, i]))
        #         self.border.append(str([399, i]))
        #     self.border.append(str([i, 0]))
        #     self.border.append(str([i, 299]))
    # define your variables here
    def myInit(self):
        self.opMap = {LEFT: [-1, 0], RIGHT: [1, 0], UP: [0, -1], DOWN: [0, 1]}
        self.ops = list(self.opMap.keys())

    def addSnakeLocation(self):
        snakeLocation = []
        for part in self.state.body:
            snakeLocation.append(str([part.x1, part.y1]))
            snakeLocation.append(str([part.x2, part.y2]))
            if part.x1 == part.x2:
                for i in range(part.y1, part.y2):
                    snakeLocation.append(str([part.x1, i]))
            else:
                for i in range(part.x1, part.x2):
                    snakeLocation.append(str([i, part.y1]))
        return snakeLocation

    def aStar(self, head, food):

        # Don't move into any snakeLocation
        # snakeLocation = self.addSnakeLocation()

        # Move to the closest food
        position = [head.x1, head.y1]
        openList = []
        visted = {str(position):True}
        closeList = []
        gScore = {}
        hScore = {}
        fScore = {}
        tiebreaker = count()
        dirArray = []

        heapq.heappush(openList, (0, -1, next(tiebreaker), position))
        # minDistance = math.inf
        # currentBestAction = None

        # for i, action in enumerate(getStates(position, self.opMap)):
        #     currentDistance = distance(action, food)
        #     print(minDistance)
        #     if not collisionDetection(action, self.state.body) and currentDistance < minDistance:
        #         print(currentDistance)
        #         minDistance = currentDistance
        #         currentBestAction = i

        # return self.ops[currentBestAction]

        #finds the next best path to the food base on current location
        while(True):
            temp = heapq.heappop(openList)
            #del visted[str(temp[3])]
            closeList.append(str(temp[3]))
            dirArray.append(temp[1])
            if len(dirArray)>1:
                break
            if np.array_equal(temp[3], food):
                break
            for i, neighbor in enumerate(getStates(temp[3], self.opMap)):
                if str(neighbor) not in closeList and not collisionDetection(neighbor, self.state.body):
                    print(neighbor)
                    if str(neighbor) not in gScore:
                        tempg = 1
                    else:
                        tempg = gScore[str(neighbor)] + 1
                    if str(neighbor) in visted:
                        if tempg < gScore[str(neighbor)]:
                            gScore[str(neighbor)] = tempg
                    else:
                        gScore[str(neighbor)] = tempg
                    hScore[str(neighbor)] = distance(neighbor,food)
                    fScore[str(neighbor)] = gScore[str(neighbor)] + hScore[str(neighbor)]
                    heapq.heappush(openList, (fScore[str(neighbor)], i, next(tiebreaker), neighbor))
                    visted[str(neighbor)] = True
        return self.ops[dirArray.pop(1)]
    def control(self):
        # Do not modify the order of operations.
        # Get current state, check exit condition and send next command.
        while(True):
            # 1. Get current state information from the server
            self.state.setState(self.networkMgr.getStateInfo())
            # 2. Check Exit condition
            if self.state.food == None:
                break
            #run astar to find the path 
            # if len(self.dirArray) == 0 or np.array_equal([self.state.body[0].x1,self.state.body[0].y1] , [self.state.food[0],self.state.food[1]] ):
            #     self.aStar(self.state.body[0], self.state.food)
            # 3. Send next command
            t1_start = time.perf_counter()
            self.networkMgr.sendCommand(self.aStar(
                self.state.body[0], self.state.food))
            t1_stop = time.perf_counter()
            # print("Elapsed time during the whole program in seconds:",
            #                             t1_stop-t1_start)
            # self.networkMgr.sendCommand(self.ops[self.dirArray.pop(0)])


cntrl = Controller()
cntrl.control()
