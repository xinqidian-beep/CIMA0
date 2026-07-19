import queue


class ByteStream:

    """
    原始字节输入层

    不解释:
    不分类:
    不编码语义:

    只是传递 byte
    """


    def __init__(self):

        self.buffer = queue.Queue()



    def push(self, data: bytes):

        for b in data:

            self.buffer.put(b)



    def read(self, size=64):

        result=[]

        while (
            not self.buffer.empty()
            and len(result)<size
        ):

            result.append(
                self.buffer.get()
            )

        return bytes(result)