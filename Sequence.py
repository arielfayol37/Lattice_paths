# python3 Sequence.py
import random
from datetime import datetime

random.seed(getattr(datetime.now(), "microsecond"))


class Sequence:
    """A sequence is a path. Paths are generated in a lexicographical order by generate_all_paths() in lp_utils.py. So each path is indentified by an index
    and we can either select one of them using its index or randomly pick one path"
    """

    def __init__(self, m, n, paths=None, len_paths=None, index=None, empty=False):
        assert m >= n

        if not empty:
            if index is None:
                self.pi = random.randint(
                    0, len_paths - 1
                )  # randomly choose an index to select a path

            else:
                self.pi = index
            self.terms = paths[self.pi]  # select a specific path from all paths

        else:
            self.terms = []
            # not a valid path but useful later in the code to generate "empty" sequences(sequences with no path yet)
            for i in range(m + n):
                self.terms.append([0, 0, 0])

        self.l = m + n

    def show(self):
        """
        Method to display a path(Sequence) on the screen
        """
        for term in self.terms:
            print(term[0], term[1], term[2], sep=" ", end="   ")

    def compare(self, sequence, k):
        """
        Method to compare if this instance's path is k-equivalent to another. Returns 0 if k-equivalent. Returns 1 if not.
        """
        assert self.l == sequence.l
        equi = 0

        for a, b in zip(self.terms, sequence.terms):
            if a == b:  # can make tis better someow
                equi += 1

                if equi == k:
                    break
        if equi >= k:
            return 0  # k-equivalent
        else:
            return 1  # k-distinct

    def same_paths(self, sequence):
        """
        Method to check if this instance's path is the same as another's path
        """
        assert self.l == sequence.l

        return int(self.pi == sequence.pi)  # returns one if paths are the same
