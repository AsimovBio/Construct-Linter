from collections import defaultdict

from anytree import findall
from anytree import PreOrderIter, LevelOrderIter
from anytree import Walker

from tree_helper import flatten

class BaseChecker(object):
    def __init__(self):
        self.violations = []
        self.message = ""

    def report_all(self):
        if self.violations:
            for warning in self.violations:
                for logged in warning:
                    print(logged)
        else:
            print("No warnings.")


class IncompleteTranscriptionUnit(BaseChecker):
    def __init__(self):
        super().__init__()
        self.required_parts = ["promoter", "utr", "cds", "stop_codon", "terminator"]
        self.required_checklist = defaultdict(int)
        self.log = []

    def extract(self, tree):
        self.transcript_units = findall(
            tree, filter_=lambda node: node.node_type == "transcription_unit"
        )
        transcript_unit_names = [node.name for node in self.transcript_units]
        required_checklist = defaultdict(int, {k: 0 for k in self.required_parts})
        self.transcript_checklist = {
            unit: required_checklist.copy() for unit in transcript_unit_names
        }

    def check(self):
        for unit in self.transcript_units:
            name = unit.name
            current_checklist = self.transcript_checklist[name]
            child_nodes = [node.node_type for node in LevelOrderIter(unit, maxlevel=2)][
                1:
            ]
            for part in child_nodes:
                current_checklist[part] += 1
            self.transcript_checklist[name] = current_checklist

    def log_warning(self):
        for unit in self.transcript_units:
            name = unit.name
            current_checklist = self.transcript_checklist[name]
            missing_parts = []
            for required in self.required_parts:
                if current_checklist[required] == 0:
                    missing_parts.append(required)

            if missing_parts:
                message = f"\tWarning: {name} is missing {str(missing_parts)[1:-1]}"
                self.log.append(message)

    def report(self, tree):
        self.extract(tree)
        self.check()
        self.log_warning()
        if self.log:
            self.violations.append(self.log)


class TranscriptionUnitOrderCheck(BaseChecker):
    def __init__(self):
        super().__init__()
        self.required_parts = ["promoter", "utr", "cds", "stop_codon", "terminator"]
        self.required_checklist = defaultdict(int)
        self.log = []

    def extract(self, tree):
        self.transcript_units = findall(
            tree, filter_=lambda node: node.node_type == "transcription_unit"
        )
        transcript_unit_names = [node.name for node in self.transcript_units]
        required_checklist = defaultdict(int, {k: -1 for k in self.required_parts})
        self.transcript_checklist = {
            unit: required_checklist.copy() for unit in transcript_unit_names
        }

    def check(self):
        for unit in self.transcript_units:
            name = unit.name
            current_checklist = self.transcript_checklist[name]
            child_nodes = [node.node_type for node in LevelOrderIter(unit, maxlevel=2)][
                1:
            ]
            for idx, part in enumerate(child_nodes):
                current_checklist[part] = idx
            self.transcript_checklist[name] = current_checklist

    def log_warning(self):
        for unit in self.transcript_units:
            name = unit.name
            current_checklist = self.transcript_checklist[name]
            out_of_order = []
            unit_req_parts = [
                index_part[0]
                for index_part in sorted(current_checklist.items(), key=lambda x: x[1])
            ]
            for i, part in enumerate(self.required_parts):
                if part != unit_req_parts[i]:
                    out_of_order.append(unit_req_parts[i])

            if out_of_order:
                message = f"\tWarning: {name} has the following parts out of order: {str(out_of_order)[1:-1]}"
                self.log.append(message)

    def report(self, tree):
        self.extract(tree)
        self.check()
        self.log_warning()
        if self.log:
            self.violations.append(self.log)


class NestedCheck(BaseChecker):
    def __init__(self):
        super().__init__()
        # self.required_parts = ["promoter", "utr", "cds", "stop_codon", "terminator"]
        self.required_checklist = defaultdict(int)
        self.log = []

    def extract(self, tree):
        self.transcript_units = findall(
            tree, filter_=lambda node: node.node_type == "transcription_unit"
        )
        self.transcript_unit_names = [node.name for node in self.transcript_units]

    def check(self):
        pass

    def log_warning(self):
        for unit in self.transcript_units:
            name = unit.name
            nested = []
            all_child_nodes = [(node, node.node_type) for node in LevelOrderIter(unit)][
                1:
            ]
            child_types = [node[1] for node in all_child_nodes]
            children = [node[0] for node in all_child_nodes]

            for i, part in enumerate(child_types):
                if part == "transcription_unit":
                    nested.append(name)
                    w = Walker()
                    path = w.walk(unit, children[i])
                    paths = []
                    for item in path:
                        direction = []
                        try:
                            if len(item.label):
                                direction.append([item.label])
                        except:
                            direction.append([n.label for n in item])
                        paths.append(direction[0])
            if nested:
                message = (
                    f"\tWarning: {name} contains a nested transcription unit.\n"
                    f"\t\tCheck the path: {flatten(paths)}"
                )
                self.log.append(message)

    def report(self, tree):
        self.extract(tree)
        self.check()
        self.log_warning()
        if self.log:
            self.violations.append(self.log)
