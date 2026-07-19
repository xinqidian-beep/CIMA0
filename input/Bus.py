from queue import Queue


class InputBus:


    def __init__(self):

        self.queue=Queue()



    def publish(
        self,
        stimulus
    ):

        self.queue.put(
            stimulus
        )



    def poll(self):

        items=[]


        while not self.queue.empty():

            items.append(
                self.queue.get()
            )


        return items