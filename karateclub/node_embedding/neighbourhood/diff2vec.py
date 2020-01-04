import numpy as np
import networkx as nx
from gensim.models.word2vec import Word2Vec
from karateclub.utils.diffusion import DiffusionTree
from karateclub.estimator import Estimator

class Diff2Vec(Estimator):
    r"""An implementation of `"Diff2Vec" <https://arxiv.org/abs/1403.6652>`_
    from the CompleNet '18 paper "Diff2Vec: Online Learning of Social Representations".


    Args:
        diffusion_number (int): Number of diffusions. Default is 10.
        diffusion_cover (int): Number of nodes in diffusion. Default is 40.
        dimensions (int): Dimensionality of embedding. Default is 128.
        workers (int): Number of cores. Default is 4.
        window_size (int): Matrix power order. Default is 5.
        epochs (int): Number of epochs.
        learning_rate (float): HogWild! learning rate.
        min_count (int): Minimal count of node occurences.
    """
    def __init__(self, walk_number=10, walk_length=80, dimensions=128, workers=4,
                 window_size=5, epochs=1, learning_rate=0.05, min_count=1):

        self.walk_number = walk_number
        self.walk_length = walk_length
        self.dimensions = dimensions
        self.workers = workers
        self.window_size = window_size
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.min_count = min_count

    def fit(self, graph):
        """
        Fitting a DeepWalk model.

        Arg types:
            * **graph** *(NetworkX graph)* - The graph to be embedded.
        """
        walker = RandomWalker(self.walk_number, self.walk_length)
        walker.do_walks(graph)

        model = Word2Vec(walker.walks,
                         hs=1,
                         alpha=self.learning_rate,
                         iter=self.epochs,
                         size=self.dimensions,
                         window=self.window_size,
                         min_count=self.min_count,
                         workers=self.workers)

        num_of_nodes = graph.number_of_nodes()
        self._embedding = [model[str(n)] for n in range(num_of_nodes)]


    def get_embedding(self):
        r"""Getting the node embedding.

        Return types:
            * **embedding** *(Numpy array)* - The embedding of nodes.
        """
        return np.array(self._embedding)
