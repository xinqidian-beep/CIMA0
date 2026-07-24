import random
from collections import deque


class EventQueue:


    def __init__(self,n):

        self.queue=deque()

        for i in range(n):

            self.queue.append(i)



    def pop(self):

        if not self.queue:
            return None

        return self.queue.popleft()



    def push_neighbors(
        self,
        ids
    ):

        for i in ids:

            self.queue.append(i)