import heapq
import random


class Scheduler:


    def __init__(self):

        self.queue=[]


    def add(self,cell,time):

        heapq.heappush(
            self.queue,
            (
                time,
                random.random(),
                cell
            )
        )


    def run(self,steps):


        for _ in range(steps):

            if not self.queue:
                break


            t,_,cell=heapq.heappop(
                self.queue
            )


            cell.update()


            # 根据自己的状态决定下一次时间

            activity=cell.oscillator.activity


            dt=1.0/(1+activity)


            self.add(
                cell,
                t+dt
            )