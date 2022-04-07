class ReadError(Exception):
    pass

class Cursor(object):
    def __init__(self, items, index=0):
        self.items = items
        self.index = index

    def current(self):
        return self.items[self.index]

    def next(self):
        self.index += 1

    def rewind(self, index=0):
        self.index = index

    def at_end(self):
        return self.index == len(self.items)

class Base(object):
    pass

class Unit(Base):
    def __init__(self, children=[]):
        self.children = children

    def read(self, input):
        unit_name = self.__class__.__name__
        cur = input.current()
        if cur['node_type'] != unit_name:
            raise ReadError(
                f"expected {unit_name} but got {cur['node_type']}"
            )
        input.next()

        if self.children:
            cursor = Cursor(cur['children'])
            for child in self.children:
                if cursor.at_end():
                    raise ReadError("ran out of input")
                child.read(cursor)
            if not cursor.at_end():
                raise ReadError("did not consume all input")

class Construct(Unit):
    pass

class TranscriptionUnit(Unit):
    pass

class Promoter(Unit):
    pass

class UTR(Unit):
    pass

class CDS(Unit):
    pass

class StopCodon(Unit):
    pass

class Terminator(Unit):
    pass

class AnyOf(Base):
    def __init__(self, children):
        self.children = children

    def read(self, input):
        index = input.index
        for child in self.children:
            try:
                input.rewind(index)
                child.read(input)
                return
            except ReadError as err:
                pass
        names = [c.__class__.__name__ for c in self.children]
        raise ReadError(f"could not match input against ({names})")

class AtLeast(Base):
    def __init__(self, minimum, child):
        self.minimum = minimum
        self.child = child

    def read(self, input):
        count = 0
        while not input.at_end():
            try:
                self.child.read(input)
                count += 1
            except ReadError as err:
                break
        if count < self.minimum:
            raise ReadError(
                f"only matched {count} input(s) but needed {self.minimum}"
            )

graph = Construct([
    AtLeast(1, TranscriptionUnit([
        Promoter(),
        AtLeast(3, AnyOf([UTR(), CDS()])),
        StopCodon(),
        Terminator(),
    ])),
])

def validate(input):
    graph.read(Cursor([input]))
