from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

from custom_node import (
    PromoterNode,
    UTRNode,
    CDSNode,
    StopCodonNode,
    TerminatorNode,
    TUNode,
)

from rules import IncompleteTranscriptionUnit, TranscriptionUnitOrderCheck, NestedCheck

# Make Tree
root = Node("design_1", node_type="construct", label="design_1", children=[
    TUNode("TU1", "TU_1", children=[
        PromoterNode("promoter1", "p1"),
        UTRNode("5'UTR1", "utr1"),
        CDSNode("CDS1", "cds1"),
        StopCodonNode("stop_codon1", "stop1"),
        TerminatorNode("terminator1", "term1"),
    ]),
    TUNode("TU2", "TU_2", children=[
        PromoterNode("promoter2", "p2"),
        UTRNode("5'UTR2", "utr2"),
        CDSNode("CDS2", "cds2", children=[
            TUNode("TU3", "TU_3", children=[
                # PromoterNode("promoter1", "p3"),
                # UTRNode("5'UTR1", "utr3"),
                # CDSNode("CDS1", "cds3"),
                StopCodonNode("stop_codon1", "stop3"),
                TerminatorNode("terminator1", "term3"),
            ]),
        ]),
        StopCodonNode("stop_codon2", "stop2"),
        TerminatorNode("terminator2", "term2"),
    ]),
    # TUNode("TU4", "TU_4", children=[
        # PromoterNode("promoter4", "p4"),
        # UTRNode("5'UTR4", "utr4"),
        # CDSNode("CDS4", "cds4"),
        # StopCodonNode("stop_codon4", "stop4"),
        # TerminatorNode("terminator4", "term4"),
    # ]),
    TUNode("TU4", "TU_4", children=[
        PromoterNode("promoter4", "p4"),
        # UTRNode("5'UTR4", "utr4"),
        # CDSNode("CDS4", "cds4"),
        # StopCodonNode("stop_codon4", "stop4"),
        # TerminatorNode("terminator4", "term4"),
    ]),
    TUNode("TU5", "TU_5", children=[
        TerminatorNode("terminator5", "term5"),
        UTRNode("5'UTR5", "utr5"),
        CDSNode("CDS5", "cds5"),
        StopCodonNode("stop_codon5", "stop5"),
        PromoterNode("promoter5", "p5"),
    ]),
])

for pre, _, node in RenderTree(root):
    treestr = "%s%s" % (pre, node.name)
    # print(treestr.ljust(8), node.node_type)
    print(treestr.ljust(8))

print("\n\n\n")

# CHECK DESIGN RULES
print("...Checking Transcription Units for missing elements...")
checker = IncompleteTranscriptionUnit()
checker.report(root)
checker.report_all()
print("\n")
print("...Checking Transcription Units for correct order...")
checker = TranscriptionUnitOrderCheck()
checker.report(root)
checker.report_all()
print("\n")
print("...Checking Construct for nested Transcription Units...")
checker = NestedCheck()
checker.report(root)
checker.report_all()
print("\n")
print("All design checks complete.")
