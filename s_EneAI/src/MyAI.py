
#3.7 sat. V3

# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import deque
from collections import defaultdict

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.max_row = 7
        self.max_col = 7
        self.current_position = [0,0]
        self.mydirection = [1,0] # position: direction
        #[1,0] right x + 1. 
        #[0,1] up y + 1 
        #[0,-1] left 
        #[-1, 0] down
        self.visited = [] #list list
        self.unvisited = [] #unvisited but safe
        self.danger = [] #store pit position
        self.ghost = []
        self.move = []
        self.no_pit = []
        # self.pit_chance = defaultdict(int)
        self.get_gold = False
        self.ammo = True
        self.mystench = False
        


        


        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        if self.move != []:
            return self.make_move()

        path_dic = {}
        # print("here is all unvisited1:    ", self.unvisited)
        if glitter:
            re_value1, re_value2 = self.next_position([0,0])
            self.move_to_next_position(re_value2)
            self.get_gold = True
            return Agent.Action.GRAB

        if scream:
            # print("here is scream and unvisited", self.unvisited)

            for i in self.ghost:
                # print("here is ghost i: ",i)
                if (i not in self.danger):
                    self.unvisited.append(i)
            self.ghost = []
            self.mystench = True

        if bump:
            self.handle_bump()

        if breeze:
            self.handle_breeze()
            # print("here is all danger:   ", self.danger)

        # print("here is all unvisited2:    ", self.unvisited)
        

        if stench:
            self.handle_ghost()
            if len(self.ghost) == 1:
                self.mystench = True
            # print("here is all ghost: ",self.ghost)

        # print("here is all unvisited3:    ", self.unvisited)
        if stench and not breeze:
            # print("in here alllllllllll ")
            self.handle_no_pit()

        if not breeze and not stench:
            self.handle_safe()

        # print("here is all unvisited4:    ", self.unvisited)

        if (self.unvisited == [] and self.current_position == [0,0] and not (self.ammo and self.ghost != [])) or self.get_gold:
            return Agent.Action.CLIMB
        
        elif self.unvisited != []:
            for i in self.unvisited:
                re_value1, re_value2 = self.next_position(i)
                path_dic[re_value1] = re_value2

            choose = sorted(path_dic)[0]
            self.move_to_next_position(path_dic[choose])


        else:
            if self.ghost != [] and self.ammo:
                self.ammo = False
                if [self.ghost[0][0] + 1,self.ghost[0][1]] in self.visited:
                    re_value1, re_value2 = self.next_position([self.ghost[0][0] + 1,self.ghost[0][1]])
                    path_dic[re_value1] = re_value2
                    choose = sorted(path_dic)[0]
                    self.move_to_next_position(path_dic[choose])
                    if self.mydirection == [0,1]:
                        self.move.append("L")
                    elif self.mydirection == [0,-1]:
                        self.move.append("R")
                    self.mydirection = [-1,0]


                elif [self.ghost[0][0] - 1,self.ghost[0][1]] in self.visited:
                    re_value1, re_value2 = self.next_position([self.ghost[0][0] - 1,self.ghost[0][1]])
                    path_dic[re_value1] = re_value2
                    choose = sorted(path_dic)[0]
                    self.move_to_next_position(path_dic[choose])
                    if self.mydirection == [0,1]:
                        self.move.append("R")
                    elif self.mydirection == [0,-1]:
                        self.move.append("L")
                    self.mydirection = [1,0]

                elif [self.ghost[0][0] , self.ghost[0][1] + 1] in self.visited:
                    re_value1, re_value2 = self.next_position([self.ghost[0][0] , self.ghost[0][1] + 1])
                    path_dic[re_value1] = re_value2
                    choose = sorted(path_dic)[0]
                    self.move_to_next_position(path_dic[choose])
                    if self.mydirection == [1,0]:
                        self.move.append("R")
                    elif self.mydirection == [-1,0]:
                        self.move.append("L")
                    self.mydirection = [0,-1]

                elif [self.ghost[0][0] , self.ghost[0][1] - 1] in self.visited:
                    re_value1, re_value2 = self.next_position([self.ghost[0][0] , self.ghost[0][1] - 1])
                    path_dic[re_value1] = re_value2
                    choose = sorted(path_dic)[0]
                    self.move_to_next_position(path_dic[choose])
                    if self.mydirection == [1,0]:
                        self.move.append("L")
                    elif self.mydirection == [-1,0]:
                        self.move.append("R")
                    self.mydirection = [0,1]

                
                # print("here is ghost0:" ,self.ghost[0])
                if (self.ghost[0] not in self.danger):
                    self.unvisited.append(self.ghost[0])
                # print("here append ghost0    ",self.unvisited)
                self.ghost.remove(self.ghost[0])
                self.move.append("S")


            else:
                # total = 0
                # for m in self.pit_chance.values():
                #     total += m

                # pit = sorted(self.pit_chance)[0]
                # # print("here is print", self.pit_chance[pit]/total, "    ", pit)

                # if  self.pit_chance[pit] == 1 and self.pit_chance[pit]/total < 0.5 and len(self.pit_chance)/total != 1:
                #     if [pit[0] + 1,pit[1]] in self.visited:
                #         re_value1, re_value2 = self.next_position([pit[0] + 1,pit[1]])
                #         path_dic[re_value1] = re_value2
                #         choose = sorted(path_dic)[0]
                #         self.move_to_next_position(path_dic[choose])
                #         if self.mydirection == [0,1]:
                #             self.move.append("L")
                #         elif self.mydirection == [0,-1]:
                #             self.move.append("R")
                #         self.mydirection = [-1,0]


                #     elif [pit[0] - 1,pit[1]] in self.visited:
                #         re_value1, re_value2 = self.next_position([pit[0] - 1,pit[1]])
                #         path_dic[re_value1] = re_value2
                #         choose = sorted(path_dic)[0]
                #         self.move_to_next_position(path_dic[choose])
                #         if self.mydirection == [0,1]:
                #             self.move.append("R")
                #         elif self.mydirection == [0,-1]:
                #             self.move.append("L")
                #         self.mydirection = [1,0]

                #     elif [pit[0] , pit[1] + 1] in self.visited:
                #         re_value1, re_value2 = self.next_position([pit[0] , pit[1] + 1])
                #         path_dic[re_value1] = re_value2
                #         choose = sorted(path_dic)[0]
                #         self.move_to_next_position(path_dic[choose])
                #         if self.mydirection == [1,0]:
                #             self.move.append("R")
                #         elif self.mydirection == [-1,0]:
                #             self.move.append("L")
                #         self.mydirection = [0,-1]

                #     elif [pit[0] , pit[1] - 1] in self.visited:
                #         re_value1, re_value2 = self.next_position([pit[0] , pit[1] - 1])
                #         path_dic[re_value1] = re_value2
                #         choose = sorted(path_dic)[0]
                #         self.move_to_next_position(path_dic[choose])
                #         if self.mydirection == [1,0]:
                #             self.move.append("L")
                #         elif self.mydirection == [-1,0]:
                #             self.move.append("R")
                #         self.mydirection = [0,1]
                    
                #     self.current_position = [pit[0] , pit[1]]
                #     self.move.append("F")


                # else:
                re_value1, re_value2 = self.next_position([0,0])
                self.move_to_next_position(re_value2)

        if self.move != []:
            return self.make_move()

        
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================


    def handle_bump(self):
        self.unvisited.remove(self.current_position)

        if self.mydirection == [1,0]:
            self.max_row = self.current_position[0]
            self.current_position[0] -= 1

        elif self.mydirection == [0,1]:
            self.max_col = self.current_position[1]
            self.current_position[1] -= 1

        for i in self.visited:
            if i[0] >= self.max_row or i[1] >= self.max_col:
                self.visited.remove(i)

        for i in self.unvisited:
            if i[0] >= self.max_row or i[1] >= self.max_col:
                self.unvisited.remove(i)

        for i in self.danger:
            if i[0] >= self.max_row or i[1] >= self.max_col:
                self.danger.remove(i)

        for i in self.ghost:
            if i[0] >= self.max_row or i[1] >= self.max_col:
                self.ghost.remove(i)

        # for i in self.pit_chance.keys():
        #     if i[0] >= self.max_row or i[1] >= self.max_col:
        #         self.pit_chance.pop(i)




    def cost(self,pre,now,next):
        direc = [abs(now[0] - pre[0]) + abs(next[0] - now[0]), abs(now[1] - pre[1]) + abs(next[1] - now[1])]
        if direc == [1,1]:
            return 1
        else:
            if now[0] - pre[0] == next[0] - now[0] and now[1] - pre[1] == next[1] - now[1]:
                return 0
            else:
                return 2


    def next_position(self,end):
        if self.current_position == end:
            return 0,[]

        x = [1, 0, -1, 0]
        y = [0, 1, 0, -1]
        dist = [[500 for _ in range(self.max_col+1)] for _ in range(self.max_row+1)]
        pre = [[None for _ in range(self.max_col+1)] for _ in range(self.max_row+1)]
        begin = self.current_position

        dist[begin[0]][begin[1]] = 0
        queue = deque()
        queue.append(begin)
        while queue:
            curr = queue.popleft()
            find = False
            for i in range(4):
                next = [curr[0] + x[i], curr[1] + y[i]]
                if (next in self.unvisited or next in self.visited) and dist[next[0]][next[1]] == 500:
                    if curr == begin:
                        direc = [self.mydirection[0] + abs(next[0] - curr[0]), self.mydirection[1] + abs(next[1] - curr[1])]

                        if direc == [1, 1]:
                            dist[next[0]][next[1]] = 2

                        else:
                            if self.mydirection[0] == next[0] - curr[0] and self.mydirection[1] == next[1] - curr[1]:
                                dist[next[0]][next[1]] = 1

                            else:
                                dist[next[0]][next[1]] = 3

                    else:
                        dist[next[0]][next[1]] = dist[curr[0]][curr[1]] + 1 + self.cost(pre[curr[0]][curr[1]], curr, next )

                    pre[next[0]][next[1]] = curr
                    queue.append(next)
                    if next == end:
                        find = True
                        break
            if find:
                break
        
        stack = []
        curr = end
        while True:
            if curr[0] == begin[0] and curr[1] == begin[1]:
                break

            stack.append(curr)
            prev = pre[curr[0]][curr[1]]
            curr = prev
        

        return dist[end[0]][end[1]] , stack


    def make_move(self):
        next_move = self.move.pop(0)
        if next_move == "L":
            return Agent.Action.TURN_LEFT
        elif next_move == "R":
            return Agent.Action.TURN_RIGHT
        elif next_move == "F":
            return Agent.Action.FORWARD
        elif next_move == "S":
            return Agent.Action.SHOOT


        

    def move_to_next_position(self, path):
        while path:
            i = path.pop()
            direc = [i[0] - self.current_position[0], i[1] - self.current_position[1]]
            if direc == self.mydirection:
                self.move.append("F")

            elif direc[0] == -self.mydirection[0] and direc[1] == -self.mydirection[1]:
                self.move.append("L")
                self.move.append("L")
                self.move.append("F")
                
            else:
                if (self.mydirection == [1,0] and direc == [0,1]) or (self.mydirection == [0,1] and direc == [-1,0]) or (self.mydirection == [-1,0] and direc == [0,-1]) or (self.mydirection == [0,-1] and direc == [1,0]):
                    self.move.append("L")
                    self.move.append("F")

                else:
                    self.move.append("R")
                    self.move.append("F")
            self.current_position = i
            self.mydirection = direc

            
    

    def handle_safe(self):
        if self.current_position not in self.no_pit:
            self.no_pit.append(self.current_position)

        if self.current_position not in self.visited:
            self.visited.append(self.current_position)

        if self.current_position in self.unvisited:
            self.unvisited.remove(self.current_position)

        if self.current_position[0] + 1 < self.max_row:
            if [self.current_position[0] + 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] + 1, self.current_position[1]] not in self.visited:
                self.unvisited.append([self.current_position[0] + 1, self.current_position[1]])

            if [self.current_position[0] + 1, self.current_position[1]] in self.danger:
                self.danger.remove([self.current_position[0] + 1, self.current_position[1]])
                # self.pit_chance.pop((self.current_position[0] + 1, self.current_position[1]))


            if [self.current_position[0] + 1, self.current_position[1]] in self.ghost:
                self.ghost.remove([self.current_position[0] + 1, self.current_position[1]])

            if [self.current_position[0] + 1, self.current_position[1]] not in self.no_pit:
                self.no_pit.append([self.current_position[0] + 1, self.current_position[1]])
        
        
        if self.current_position[1] + 1 < self.max_col:
            if [self.current_position[0], self.current_position[1] + 1] not in self.unvisited and [self.current_position[0], self.current_position[1] + 1] not in self.visited:
                self.unvisited.append([self.current_position[0], self.current_position[1] + 1])

            if [self.current_position[0], self.current_position[1] + 1] in self.danger:
                self.danger.remove([self.current_position[0], self.current_position[1] + 1])
                # self.pit_chance.pop((self.current_position[0], self.current_position[1] + 1))

            if [self.current_position[0], self.current_position[1] + 1] in self.ghost:
                self.ghost.remove([self.current_position[0], self.current_position[1] + 1])

            if [self.current_position[0], self.current_position[1] + 1] not in self.no_pit:
                self.no_pit.append([self.current_position[0], self.current_position[1] + 1])
        

        if self.current_position[0] - 1 >= 0:
            if [self.current_position[0] - 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] - 1, self.current_position[1]] not in self.visited:
                self.unvisited.append([self.current_position[0] - 1, self.current_position[1]])

            if [self.current_position[0] - 1, self.current_position[1]] in self.danger:
                self.danger.remove([self.current_position[0] - 1, self.current_position[1]])
                # self.pit_chance.pop((self.current_position[0] - 1, self.current_position[1]))

            if [self.current_position[0] - 1, self.current_position[1]] in self.ghost:
                self.ghost.remove([self.current_position[0] - 1, self.current_position[1]])

            if [self.current_position[0] - 1, self.current_position[1]] not in self.no_pit:
                self.no_pit.append([self.current_position[0] - 1, self.current_position[1]])
        

        if self.current_position[1] - 1 >= 0:
            if [self.current_position[0], self.current_position[1] - 1] not in self.unvisited and [self.current_position[0], self.current_position[1] - 1] not in self.visited:
                self.unvisited.append([self.current_position[0], self.current_position[1] - 1])

            if [self.current_position[0], self.current_position[1] - 1] in self.danger:
                self.danger.remove([self.current_position[0], self.current_position[1] - 1])
                # self.pit_chance.pop((self.current_position[0], self.current_position[1] - 1))

            if [self.current_position[0], self.current_position[1] - 1] in self.ghost:
                self.ghost.remove([self.current_position[0], self.current_position[1] - 1])

            if [self.current_position[0], self.current_position[1] - 1] not in self.no_pit:
                self.no_pit.append([self.current_position[0], self.current_position[1] - 1])


    def handle_breeze(self):
        if self.current_position not in self.visited:
            self.visited.append(self.current_position)

        if self.current_position in self.unvisited:
            self.unvisited.remove(self.current_position)

        if self.current_position[0] + 1 < self.max_row:
            if [self.current_position[0] + 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] + 1, self.current_position[1]] not in self.visited:
                if [self.current_position[0] + 1, self.current_position[1]] not in self.no_pit:
                    # self.pit_chance[(self.current_position[0] + 1, self.current_position[1])] += 1
                    if [self.current_position[0] + 1, self.current_position[1]] not in self.danger:
                        self.danger.append([self.current_position[0] + 1, self.current_position[1]])
                    
        
        if self.current_position[1] + 1 < self.max_col:
            if [self.current_position[0], self.current_position[1] + 1] not in self.unvisited and [self.current_position[0], self.current_position[1] + 1] not in self.visited:
                if [self.current_position[0], self.current_position[1] + 1] not in self.no_pit:
                    # self.pit_chance[(self.current_position[0], self.current_position[1] + 1)] += 1
                    if [self.current_position[0], self.current_position[1] + 1] not in self.danger:
                        self.danger.append([self.current_position[0], self.current_position[1] + 1])
                    
        
        if self.current_position[0] - 1 >= 0:
            if [self.current_position[0] - 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] - 1, self.current_position[1]] not in self.visited:
                if [self.current_position[0] - 1, self.current_position[1]] not in self.no_pit:
                    # self.pit_chance[(self.current_position[0] - 1, self.current_position[1])] += 1
                    if [self.current_position[0] - 1, self.current_position[1]] not in self.danger:
                        self.danger.append([self.current_position[0] - 1, self.current_position[1]])
                    
        
        if self.current_position[1] - 1 >= 0:
            if [self.current_position[0], self.current_position[1] - 1] not in self.unvisited and [self.current_position[0], self.current_position[1] - 1] not in self.visited:
                if [self.current_position[0], self.current_position[1] - 1] not in self.no_pit:
                    # self.pit_chance[(self.current_position[0], self.current_position[1] - 1)] += 1
                    if [self.current_position[0], self.current_position[1] - 1] not in self.danger:
                        self.danger.append([self.current_position[0], self.current_position[1] - 1])
                        

    
    def handle_no_pit(self):
        if self.current_position[0] + 1 < self.max_row:
            if [self.current_position[0] + 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] + 1, self.current_position[1]] not in self.visited:
                if [self.current_position[0] + 1, self.current_position[1]] in self.danger:
                    self.danger.remove([self.current_position[0] + 1, self.current_position[1]])
                    # self.pit_chance.pop((self.current_position[0] + 1, self.current_position[1]))
                if [self.current_position[0] + 1, self.current_position[1]] not in self.no_pit:
                    self.no_pit.append([self.current_position[0] + 1, self.current_position[1]])
        
        if self.current_position[1] + 1 < self.max_col:
            if [self.current_position[0], self.current_position[1] + 1] not in self.unvisited and [self.current_position[0], self.current_position[1] + 1] not in self.visited:
                if [self.current_position[0], self.current_position[1] + 1] in self.danger:
                    self.danger.remove([self.current_position[0], self.current_position[1] + 1])
                    # self.pit_chance.pop((self.current_position[0], self.current_position[1] + 1))
                if [self.current_position[0], self.current_position[1] + 1] not in self.no_pit:
                    self.no_pit.append([self.current_position[0], self.current_position[1] + 1])
        
        if self.current_position[0] - 1 >= 0:
            if [self.current_position[0] - 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] - 1, self.current_position[1]] not in self.visited:
                if [self.current_position[0] - 1, self.current_position[1]] in self.danger:
                    self.danger.remove([self.current_position[0] - 1, self.current_position[1]])
                    # self.pit_chance.pop((self.current_position[0] - 1, self.current_position[1]))
                if [self.current_position[0] - 1, self.current_position[1]] not in self.no_pit:
                    self.no_pit.append([self.current_position[0] - 1, self.current_position[1]])
        
        if self.current_position[1] - 1 >= 0:
            if [self.current_position[0], self.current_position[1] - 1] not in self.unvisited and [self.current_position[0], self.current_position[1] - 1] not in self.visited:
                if [self.current_position[0], self.current_position[1] - 1] in self.danger:
                    self.danger.remove([self.current_position[0], self.current_position[1] - 1])
                    # self.pit_chance.pop((self.current_position[0], self.current_position[1] - 1))
                if [self.current_position[0], self.current_position[1] - 1] not in self.no_pit:
                    self.no_pit.append([self.current_position[0], self.current_position[1] - 1])


    def handle_ghost(self):
        if self.current_position not in self.visited:
            self.visited.append(self.current_position)

        if self.current_position in self.unvisited:
            self.unvisited.remove(self.current_position)
        

        if self.current_position[0] + 1 < self.max_row:
            if [self.current_position[0] + 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] + 1, self.current_position[1]] not in self.visited:
                if self.mystench:
                    if [self.current_position[0] + 1, self.current_position[1]] not in self.danger and [self.current_position[0] + 1, self.current_position[1]] not in self.ghost and [self.current_position[0] + 1, self.current_position[1]] not in self.visited:
                        self.unvisited.append([self.current_position[0] + 1, self.current_position[1]])

                elif [self.current_position[0] + 1, self.current_position[1]] not in self.ghost:
                    self.ghost.append([self.current_position[0] + 1, self.current_position[1]])

                else:
                    for i in self.ghost:
                        if i != [self.current_position[0] + 1, self.current_position[1]] and i not in self.danger:
                            self.unvisited.append(i)

                    self.ghost = []
                    self.ghost.append([self.current_position[0] + 1, self.current_position[1]])
                    return

        if self.current_position[1] + 1 < self.max_col:
            if [self.current_position[0], self.current_position[1] + 1] not in self.unvisited and [self.current_position[0], self.current_position[1] + 1] not in self.visited:
                if self.mystench:
                    if [self.current_position[0], self.current_position[1] + 1] not in self.danger and [self.current_position[0], self.current_position[1] + 1] not in self.ghost and [self.current_position[0], self.current_position[1] + 1] not in self.visited:
                        self.unvisited.append([self.current_position[0], self.current_position[1] + 1])

                elif [self.current_position[0], self.current_position[1] + 1] not in self.ghost:
                    self.ghost.append([self.current_position[0], self.current_position[1] + 1])
                    
                else:
                    for i in self.ghost:
                        if i != [self.current_position[0], self.current_position[1] + 1] and i not in self.danger:
                            self.unvisited.append(i)

                    self.ghost = []
                    self.ghost.append([self.current_position[0], self.current_position[1] + 1])
                    return

        if self.current_position[0] - 1 >= 0:
            if [self.current_position[0] - 1, self.current_position[1]] not in self.unvisited and [self.current_position[0] - 1, self.current_position[1]] not in self.visited:
                if self.mystench:
                    if [self.current_position[0] - 1, self.current_position[1]] not in self.danger and [self.current_position[0] - 1, self.current_position[1]] not in self.ghost and [self.current_position[0] - 1, self.current_position[1]] not in self.visited:
                        self.unvisited.append([self.current_position[0] - 1, self.current_position[1]])

                elif [self.current_position[0] - 1, self.current_position[1]] not in self.ghost:
                    self.ghost.append([self.current_position[0] - 1, self.current_position[1]])
                else:
                    for i in self.ghost:
                        if i != [self.current_position[0] - 1, self.current_position[1]] and i not in self.danger:
                            self.unvisited.append(i)

                    self.ghost = []
                    self.ghost.append([self.current_position[0] - 1, self.current_position[1]])
                    return

        if self.current_position[1] - 1 >= 0: 
            if [self.current_position[0], self.current_position[1] - 1] not in self.unvisited and [self.current_position[0], self.current_position[1] - 1] not in self.visited:     
                if self.mystench:
                    if [self.current_position[0], self.current_position[1] - 1] not in self.danger and [self.current_position[0], self.current_position[1] - 1] not in self.ghost and [self.current_position[0], self.current_position[1] - 1] not in self.visited:
                        self.unvisited.append([self.current_position[0], self.current_position[1] - 1])

                elif [self.current_position[0], self.current_position[1] - 1] not in self.ghost:
                    self.ghost.append([self.current_position[0], self.current_position[1] - 1])
                else:
                    for i in self.ghost:
                        if i != [self.current_position[0], self.current_position[1] - 1] and i not in self.danger:
                            self.unvisited.append(i)

                    self.ghost = []
                    self.ghost.append([self.current_position[0], self.current_position[1] - 1])
                    return


    

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================