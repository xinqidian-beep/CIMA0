class ComputeSystem:

    def __init__(
        self,
        capacity=100
    ):
        self.capacity = capacity


    def allocate(
        self,
        requests
    ):

        total = self._sum_activity(
            requests
        )

        if total <= 0:
            return {}

        return self._allocate_tree(
            requests,
            self.capacity,
            total
        )


    def _sum_activity(
        self,
        value
    ):

        if isinstance(
            value,
            dict
        ):

            total = 0.0

            for v in value.values():

                total += self._sum_activity(
                    v
                )

            return total


        if isinstance(
            value,
            (int, float)
        ):

            return float(value)


        return 0.0



    def _allocate_tree(
        self,
        node,
        capacity,
        total
    ):

        if isinstance(
            node,
            dict
        ):

            result = {}

            for key, value in node.items():

                result[key] = self._allocate_tree(
                    value,
                    capacity,
                    total
                )

            return result


        if isinstance(
            node,
            (int, float)
        ):

            return (
                capacity *
                float(node) /
                total
            )


        return 0.0