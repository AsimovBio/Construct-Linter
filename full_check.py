from anytree import AnyNode, Node, NodeMixin
from anytree import RenderTree
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
root = Node("design_1", node_type="construct", label="design_1")
TU1 = TUNode("TU1", "TU_1", parent=root)
p1 = PromoterNode("promoter1", "p1", parent=TU1)
utr1 = UTRNode("5'UTR1", "utr1", parent=TU1)
cds1 = CDSNode("CDS1", "cds1", parent=TU1)
stop1 = StopCodonNode("stop_codon1", "stop1", parent=TU1)
term1 = TerminatorNode("terminator1", "term1", parent=TU1)

TU2 = TUNode("TU2", "TU_2", parent=root)
p2 = PromoterNode("promoter2", "p2", parent=TU2)
utr2 = UTRNode("5'UTR2", "utr2", parent=TU2)
cds2 = CDSNode("CDS2", "cds2", parent=TU2)
stop2 = StopCodonNode("stop_codon2", "stop2", parent=TU2)
term2 = TerminatorNode("terminator2", "term2", parent=TU2)

TU3 = TUNode("TU3", "TU_3", parent=cds2)
# p3 = PromoterNode("promoter1", "p3", parent=TU3)
# utr3 = UTRNode("5'UTR1", "utr3", parent=TU3)
# cds3 = CDSNode("CDS1", "cds3", parent=TU3)
stop3 = StopCodonNode("stop_codon1", "stop3", parent=TU3)
term3 = TerminatorNode("terminator1", "term3", parent=TU3)

# TU4 = TUNode("TU4", "TU_4", parent=root)
# p4 = PromoterNode("promoter4", "p4", parent=TU4)
# utr4 = UTRNode("5'UTR4", "utr4", parent=TU4)
# cds4 = CDSNode("CDS4", "cds4", parent=TU4)
# stop4 = StopCodonNode("stop_codon4", "stop4", parent=TU4)
# term4 = TerminatorNode("terminator4", "term4", parent=TU4)

TU4 = TUNode("TU4", "TU_4", parent=root)
p4 = PromoterNode("promoter4", "p4", parent=TU4)
# utr4 = UTRNode("5'UTR4", "utr4", parent=TU4)
# cds4 = CDSNode("CDS4", "cds4", parent=TU4)
# stop4 = StopCodonNode("stop_codon4", "stop4", parent=TU4)
# term4 = TerminatorNode("terminator4", "term4", parent=TU4)

TU5 = TUNode("TU5", "TU_5", parent=root)
term5 = TerminatorNode("terminator5", "term5", parent=TU5)
utr5 = UTRNode("5'UTR5", "utr5", parent=TU5)
cds5 = CDSNode("CDS5", "cds5", parent=TU5)
stop5 = StopCodonNode("stop_codon5", "stop5", parent=TU5)
p5 = PromoterNode("promoter5", "p5", parent=TU5)

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
