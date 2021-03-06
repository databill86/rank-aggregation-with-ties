from mediane.algorithms.median_ranking import MedianRanking, DistanceNotHandledException
from mediane.distances.enumeration import GENERALIZED_KENDALL_TAU_DISTANCE, GENERALIZED_INDUCED_KENDALL_TAU_DISTANCE, \
    PSEUDO_METRIC_BASED_ON_GENERALIZED_INDUCED_KENDALL_TAU_DISTANCE
from mediane.algorithms.lri.BioConsert import BioConsert

from typing import List, Dict, Tuple
from itertools import combinations
from numpy import vdot, ndarray, count_nonzero, shape, array, zeros, asarray
from igraph import Graph


class CondorcetPartitioning(MedianRanking):
    def __init__(self, algorithm_to_complete=None):
        if isinstance(algorithm_to_complete, MedianRanking):
            self.alg = algorithm_to_complete
        else:
            self.alg = BioConsert(starting_algorithms=None)

    def compute_median_rankings(
            self,
            rankings: List[List[List[int]]],
            distance,
            return_at_most_one_ranking: bool = False)-> List[List[List[int]]]:
        """
        :param rankings: A set of rankings
        :type rankings: list
        :param distance: The distance to use/consider
        :type distance: Distance
        :param return_at_most_one_ranking: the algorithm should not return more than one ranking
        :type return_at_most_one_ranking: bool
        :return one or more consensus if the underlying algorithm can find multiple solution as good as each other.
        If the algorithm is not able to provide multiple consensus, or if return_at_most_one_ranking is True then, it
        should return a list made of the only / the first consensus found
        :raise DistanceNotHandledException when the algorithm cannot compute the consensus following the distance given
        as parameter
        """
        scoring_scheme = asarray(distance.scoring_scheme)
        if scoring_scheme[1][0] != scoring_scheme[1][1] or scoring_scheme[1][3] != scoring_scheme[1][4]:
            raise DistanceNotHandledException
        res = []
        elem_id = {}
        id_elements = {}
        id_elem = 0
        for ranking in rankings:
            for bucket in ranking:
                for element in bucket:
                    if element not in elem_id:
                        elem_id[element] = id_elem
                        id_elements[id_elem] = element
                        id_elem += 1
        # nb_elements = len(elem_id)

        positions = CondorcetPartitioning.__positions(rankings, elem_id)

        # TYPE igraph.Graph
        gr1, mat_score = self.__graph_of_elements(positions, scoring_scheme)

        # TYPE igraph.clustering.VertexClustering
        scc = gr1.components()
        for scc_i in scc:
            if len(scc_i) == 1:
                res.append([id_elements.get(scc_i[0])])
            else:
                all_tied = True
                for e1, e2 in combinations(scc_i, 2):
                    if mat_score[e1][e2][2] > mat_score[e1][e2][0] or mat_score[e1][e2][2] > mat_score[e1][e2][1]:
                        all_tied = False
                        break
                if all_tied:
                    buck = []
                    for el in scc_i:
                        buck.append(id_elements.get(el))
                    res.append(buck)
                else:
                    set_scc = set(scc_i)
                    project_rankings = []
                    for ranking in rankings:
                        project_ranking = []
                        for bucket in ranking:
                            project_bucket = []
                            for elem in bucket:
                                if elem_id.get(elem) in set_scc:
                                    project_bucket.append(elem)
                            if len(project_bucket) > 0:
                                project_ranking.append(project_bucket)
                        project_rankings.append(project_ranking)
                    res.extend(self.alg.compute_median_rankings(project_rankings, distance, False)[0])

        return [res]

    @staticmethod
    def __graph_of_elements(positions: ndarray, matrix_scoring_scheme: ndarray) -> Tuple[Graph, ndarray]:
        graph_of_elements = Graph(directed=True)
        cost_before = matrix_scoring_scheme[0]
        cost_tied = matrix_scoring_scheme[1]
        cost_after = array([cost_before[1], cost_before[0], cost_before[2], cost_before[4], cost_before[3],
                            cost_before[5]])
        n = shape(positions)[0]
        m = shape(positions)[1]

        for i in range(n):
            graph_of_elements.add_vertex(name=str(i))
        matrix = zeros((n, n, 3))

        for e1 in range(n):
            mem = positions[e1]
            d = count_nonzero(mem == -1)
            for e2 in range(e1 + 1, n):
                a = count_nonzero(mem + positions[e2] == -2)
                b = count_nonzero(mem == positions[e2])
                c = count_nonzero(positions[e2] == -1)
                e = count_nonzero(mem < positions[e2])
                relative_positions = array([e - d + a, m - e - b - c + a, b - a, c - a, d - a, a])
                put_before = vdot(relative_positions, cost_before)
                put_after = vdot(relative_positions, cost_after)
                put_tied = vdot(relative_positions, cost_tied)
                if put_before > put_after or put_before > put_tied:
                    graph_of_elements.add_edge(e2, e1)
                if put_after > put_before or put_after > put_tied:
                    graph_of_elements.add_edge(e1, e2)
                matrix[e1][e2] = [put_before, put_after, put_tied]
                matrix[e2][e1] = [put_after, put_before, put_tied]
        return graph_of_elements, matrix

    @staticmethod
    def __positions(rankings: List[List[List[int]]], elements_id: Dict) -> ndarray:
        positions = zeros((len(elements_id), len(rankings)), dtype=int) - 1
        id_ranking = 0
        for ranking in rankings:
            id_bucket = 0
            for bucket in ranking:
                for element in bucket:
                    positions[elements_id.get(element)][id_ranking] = id_bucket
                id_bucket += 1
            id_ranking += 1
        return positions

    def is_breaking_ties_arbitrarily(self):
        return False

    def is_using_random_value(self):
        return False

    def get_full_name(self):
        return "CondorcetPartitioning"

    def get_handled_distances(self):
        """

        :return: a list of distances from distance_enumeration
        """
        return [GENERALIZED_KENDALL_TAU_DISTANCE, GENERALIZED_INDUCED_KENDALL_TAU_DISTANCE,
                PSEUDO_METRIC_BASED_ON_GENERALIZED_INDUCED_KENDALL_TAU_DISTANCE]
