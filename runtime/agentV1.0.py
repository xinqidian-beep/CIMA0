from core.cloud import Cloud

from interface.byte_stream import ByteStream
from interface.mapper import ByteFieldMapper

from observer.observer import Observer

import numpy as np
from interface.output_mapper import OutputMapper
from organs.oscillator_organ import OscillatorOrgan


class Agent:
    

    def __init__(self):

        self.cloud = Cloud(
            cells=64,
            dim=512
        )


        self.interface = ByteStream()


        self.mapper = ByteFieldMapper(
            dim=512
        )

        self.output_mapper = OutputMapper()


        self.organs = [

            OscillatorOrgan(
                "organ_A"
            ),

            OscillatorOrgan(
                "organ_B"
            )

        ]

        self.observer = Observer()



    def run(
        self,
        steps=100000
    ):


        for i in range(steps):


            # 持续环境扰动

            if i % 500 == 0:

                data = bytes(
                    np.random.randint(
                        0,
                        256,
                        32
                    )
                )

                self.interface.push(
                    data
                )


            # IO -> field

            raw = self.interface.read(
                64
            )


            if raw:

                field = self.mapper.map(
                    raw
                )


                self.cloud.receive(
                    field
                )


            # 内部动力

            self.cloud.step()

            # 场 -> 器官
            field = self.cloud.get_field()
            for organ in self.organs:
                organ.receive(
                    field
                )

                organ.step()


            # 输出观察

            if i % 1000 == 0:
                field = self.cloud.get_field()
                print(
                    [
                        organ.snapshot()
                        for organ in self.organs
                    ]
                )

                

                out = self.output_mapper.map(
                    field
                )

                print(
                    {
                        "step": i,
                        "output_bytes": len(out),
                        "organs": len(self.organs)
                    }
                )

            # Observer

            if i % 1000 == 0:


                result = self.observer.measure(
                    self.cloud
                )

                result.update(
                    self.observer.cluster(
                        self.cloud
                    )
                )

                result["step"]=i


                print(
                    result
                )