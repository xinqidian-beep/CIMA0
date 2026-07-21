import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components



class ClusterObserver:


    def __init__(
        self,
        threshold=0.8
    ):

        self.threshold=threshold



    def observe(self, network):


        x=np.array(
            [
                n.x
                for n in network.nodes
            ]
        )


        v=np.array(
            [
                n.v
                for n in network.nodes
            ]
        )


        phase=np.arctan2(
            v,
            x
        )


        rows=[]
        cols=[]


        for a,b in network.edges:


            diff=abs(
                phase[a]-phase[b]
            )


            if diff < self.threshold:

                rows.append(a)
                cols.append(b)



        if len(rows)==0:

            return {

                "phase_std":
                    float(np.std(phase)),

                "clusters":
                    network.n,

                "max_cluster":
                    1
            }



        data=np.ones(
            len(rows)
        )


        adj=csr_matrix(
            (
                data,
                (rows,cols)
            ),
            shape=(
                network.n,
                network.n
            )
        )


        adj=adj+adj.T



        count,labels=connected_components(
            adj,
            directed=False,
            return_labels=True
        )


        sizes=np.bincount(
            labels
        )


        return {

            "phase_std":
                float(np.std(phase)),

            "clusters":
                int(count),

            "max_cluster":
                int(np.max(sizes))
        }