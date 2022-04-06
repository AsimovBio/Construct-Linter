from rules2 import validate

validate({
    "node_type": "Construct",
    "name": "design1",
    "children": [{
        "node_type": "TranscriptionUnit",
        "name": "TU1",
        "children": [{
            "node_type": "Promoter",
            "name": "p1",
        }, {
            "node_type": "UTR",
            "name": "utr1",
        }, {
            "node_type": "CDS",
            "name": "cds1",
        }, {
            "node_type": "UTR",
            "name": "utr2",
        }, {
            "node_type": "StopCodon",
            "name": "stop1",
        }, {
            "node_type": "Terminator",
            "name": "term1",
        }]
    }]
})