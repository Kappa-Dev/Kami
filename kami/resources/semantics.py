"""Semantic AG."""
import networkx as nx

from regraph.primitives import (add_nodes_from,
                                add_edges_from)


action_graph = nx.DiGraph()
add_nodes_from(action_graph, [
    "protein_kinase",
    ("activity", {"name": {"activity"}, "test": {True}}),
    ("phospho", {"value": {True}}),
    ("phospho_state", {"name": {"phosphorylation"}, "test": {True, False}}),
    ("phospho_target_residue", {"aa": {"S", "T", "Y"}, "test": {True}}),
    "phosphatase",
    ("dephospho", {"value": {False}}),
    "pY_site",
    ("sh2_domain_pY_bnd", {"type": "do", "test": True}),
    "sh2_domain",
])

add_edges_from(action_graph, [
    ("activity", "protein_kinase"),
    ("protein_kinase", "phospho"),
    ("phospho", "phospho_state"),
    ("phospho_state", "phospho_target_residue"),
    ("activity", "phosphatase"),
    ("phosphatase", "dephospho"),
    ("dephospho", "phospho_state"),
    ("phospho_target_residue", "pY_site"),
    ("pY_site", "sh2_domain_pY_bnd"),
    ("sh2_domain", "sh2_domain_pY_bnd"),
])

sag_kami_typing = {
    "protein_kinase": "region",
    "activity": "state",
    "phospho": "mod",
    "phospho_state": "state",
    "phospho_target_residue": "residue",
    "phosphatase": "region",
    "dephospho": "mod",
    "pY_site": "site",
    "sh2_domain_pY_bnd": "bnd",
    "sh2_domain": "region",
}

# Phosphorylation semantic nugget
phosphorylation = nx.DiGraph()
add_nodes_from(
    phosphorylation,
    ["protein_kinase",
     ("protein_kinase_activity", {"name": {"activity"}, "test": {True}}),
     ("phospho", {"value": {True}}),
     ("target_state", {"name": {"phosphorylation"}, "test": {False}}),
     ("target_residue", {"aa": {"S", "T", "Y"}, "test": {True}})]
)

add_edges_from(
    phosphorylation,
    [("protein_kinase_activity", "protein_kinase"),
     ("protein_kinase", "phospho"),
     ("phospho", "target_state"),
     ("target_state", "target_residue")]
)

phosphorylation_kami_typing = {
    "protein_kinase": "region",
    "protein_kinase_activity": "state",
    "phospho": "mod",
    "target_state": "state",
    "target_residue": "residue"
}

phosphorylation_semantic_AG = {
    "protein_kinase": "protein_kinase",
    "protein_kinase_activity": "activity",
    "phospho": "phospho",
    "target_state": "phospho_state",
    "target_residue": "phospho_target_residue"
}

# Dephosphorylation semantic nugget
dephosphorylation = nx.DiGraph()
add_nodes_from(
    dephosphorylation,
    [
        "phosphatase",
        ("phosphatase_activity", {"name": {"activity"}, "test": {True}}),
        ("dephospho", {"value": False}),
        ("target_state", {"name": {"phosphorylation"}, "test": {True}}),
        ("target_residue", {"aa": {"S", "T", "Y"}, "test": {True}})
    ]
)

add_edges_from(
    dephosphorylation,
    [
        ("phosphatase_activity", "phosphatase"),
        ("phosphatase", "dephospho"),
        ("dephospho", "target_state"),
        ("target_state", "target_residue")
    ]
)

dephosphorylation_kami_typing = {
    "phosphatase": "region",
    "phosphatase_activity": "state",
    "dephospho": "mod",
    "target_state": "state",
    "target_residue": "residue"
}

dephosphorylation_semantic_AG = {
    "phosphatase": "phosphatase",
    "phosphatase_activity": "activity",
    "dephospho": "dephospho",
    "target_state": "phospho_state",
    "target_residue": "phospho_target_residue"
}

# SH2 - pY binding semantic nugget
sh2_pY_binding = nx.DiGraph()
add_nodes_from(
    sh2_pY_binding,
    [
        "sh2_domain",
        ("sh2_domain_pY_bnd", {"type": "do", "test": True}),
        "pY_site",
        ("pY_residue", {"aa": "Y", "test": True}),
        ("phosphorylation", {"name": "phosphorylation", "test": True})
    ]
)

add_edges_from(
    sh2_pY_binding,
    [("sh2_domain", "sh2_domain_pY_bnd"),
     ("pY_site", "sh2_domain_pY_bnd"),
     ("pY_residue", "pY_site"),
     ("phosphorylation", "pY_residue")]
)

sh2_pY_kami_typing = {
    "sh2_domain": "region",
    "sh2_domain_pY_bnd": "bnd",
    "pY_site": "site",
    "pY_residue": "residue",
    "phosphorylation": "state",
}

sh2_pY_semantic_AG = {
    "sh2_domain": "sh2_domain",
    "sh2_domain_pY_bnd": "sh2_domain_pY_bnd",
    "pY_site": "pY_site",
    "pY_residue": "phospho_target_residue",
    "phosphorylation": "phospho_state"
}
