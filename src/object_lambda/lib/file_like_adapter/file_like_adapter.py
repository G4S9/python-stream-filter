class FileLikeAdapter:
    def __init__(self, it):
        self.it = iter(it)
        self.next_chunk = ""

    def grow_chunk(self):
        self.next_chunk = self.next_chunk + next(self.it)

    def read(self, n):
        if n < 0:
            raise ValueError
        if self.next_chunk is None:
            return None
        try:
            while len(self.next_chunk) < n:
                self.grow_chunk()
            rv = self.next_chunk[:n]
            # remove sent bytes from memory
            self.next_chunk = self.next_chunk[n:]
            return rv
        except StopIteration:
            rv = self.next_chunk
            self.next_chunk = None
            return None if rv == "" else rv
