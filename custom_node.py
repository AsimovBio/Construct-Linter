from anytree import NodeMixin

class PromoterNode(NodeMixin):
    """Class that represents promoters in an Abstract Syntax Tree."""

    def __init__(self, name, label, parent=None, children=None):
        self.name = name
        self.label = label
        self.parent = parent
        self.node_type = "promoter"
        if children:
            self.children = children


class UTRNode(NodeMixin):
    """Class that represents UTRs in an Abstract Syntax Tree."""

    def __init__(self, name, label, parent=None, children=None):
        self.name = name
        self.label = label
        self.parent = parent
        self.node_type = "utr"
        if children:
            self.children = children


class CDSNode(NodeMixin):
    """Class that represents CDS in an Abstract Syntax Tree."""

    def __init__(self, name, label, parent=None, children=None):
        self.name = name
        self.label = label
        self.parent = parent
        self.node_type = "cds"
        if children:
            self.children = children


class StopCodonNode(NodeMixin):
    """Class that represents stop codons in an Abstract Syntax Tree."""

    def __init__(self, name, label, parent=None, children=None):
        self.name = name
        self.label = label
        self.parent = parent
        self.node_type = "stop_codon"
        if children:
            self.children = children


class TerminatorNode(NodeMixin):
    """Class that represents terminators in an Abstract Syntax Tree."""

    def __init__(self, name, label, parent=None, children=None):
        self.name = name
        self.label = label
        self.parent = parent
        self.node_type = "terminator"
        if children:
            self.children = children


class TUNode(NodeMixin):
    """Class that represents a transcription unit in an Abstract Syntax Tree."""

    def __init__(self, name, label, parent=None, children=None):
        self.name = name
        self.label = label
        self.parent = parent
        self.num_children = 0
        self.node_type = "transcription_unit"
        if children:
            self.children = children
            self.num_children = len(children)
