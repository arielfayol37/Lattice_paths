class LexOrderer:
    """
    A iterator class that returns lattice paths in lexicographic order.
    ...
    Methods
    -------
    LexOrderer(m: int, n: int)
        Return a LexOrderer iterator that will return the lattice paths with
        m east steps and n north steps in lexicographic order.
    """

    def __init__(self, m, n):
        """
        Parameters
        ----------
        m : int
            number of east steps in the lattice steps
        n : int
            number of north steps in the lattice steps
        """
        self.m = m
        self.n = n
        self.path_length = m + n
        # self.string is the current path in the generator
        # it will look something like: 'EEEENNN'
        self.string = ''
        # self.__first tracks whether we are at the beginning
        # this is important to avoid off-by-one issues
        self.__first = True

    def __iter__(self):
        """
        Start iteration.
        """
        # This method is called before a loop starts getting values from the
        # iterator
        # The following line sets the beginning path (all E's before all N's)
        self.string = 'E'*self.m+'N'*self.n
        self.__first = True
        return self

    def __next__(self):
        """
        Returns the next path in lexicographic order.
        """
        # The following lines check to see if the current string is final
        # (all N's before all E's). If it is, we stop.
        if self.string == 'N'*self.n + 'E'*self.m:
            raise StopIteration
        # If this is the first value, we have already calculated the string, so
        # we can just return it
        if self.__first:
            self.__first = False
            return self.string
        # Otherwise, find where all the e's are
        e_loc = list(self.__find_all_e())
        # then, find how many e's are at the end of the current path
        trail = self.__trailing_e()
        # we will move the last e that has an n after it
        swap = e_loc[-1*trail-1]
        self.string = (self.string[:swap]+self.string[swap+1]+
                          self.string[swap]+self.string[swap+2:])
        # Then, we reverse everything after the move
        self.__reverse(swap+2,self.path_length-1)
        # we have the next string, so we return it
        return self.string

    def __len__(self):
        """
        Number of lattice paths.
        """
        # this function gives the "length" of the iterator, which is the number
        # of possible paths on the given lattice
        return comb(self.m+self.n,self.m)

    def __trailing_e(self):
        """
        Returns the number of trailing e's in the current path string.
        """
        count = 0
        # This loop iterates over the current path string in reverse order
        for x in self.string[-1::-1]:
            # if we encounter an N, we're done
            if x=='N':
                return count
            count+=1
        return count

    def __reverse(self, x, y):
        """
        Reverses the part of the current path string between indices x and y,
        inclusive.
        """
        s = self.string
        while x < y:
            s = s[:x]+s[y]+s[x+1:y]+s[x]+s[y+1:]
            x += 1
            y -= 1
        self.string = s

    def __find_all_e(self):
        """
        Find the locations of all e's in the current path string.
        """
        s = self.string
        idx = s.find('E')
        # The optional second argument of string.find() is the index to start
        # looking at. When there are no E's after the index, find() returns -1
        while idx != -1:
            yield idx
            idx = s.find('E', idx + 1)
