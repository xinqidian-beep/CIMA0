import json
import os



class Memory:


    def __init__(
        self,
        path="data/memory.jsonl"
    ):


        self.path=path


        os.makedirs(
            "data",
            exist_ok=True
        )



    def record(
        self,
        state
    ):


        with open(
            self.path,
            "a",
            encoding="utf8"
        ) as f:


            f.write(
                json.dumps(
                    state
                )
                +
                "\n"
            )