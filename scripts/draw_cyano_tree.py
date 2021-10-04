#!/usr/bin/env python
__author__ = "Jimmy Saw"

"""
usage example:

"""

import argparse
import pandas as pd
import ete3
from ete3 import Tree, TreeStyle, NodeStyle, faces

def treeLayout(node):    
    if node.is_leaf():
        if node.name in m:
            N = ete3.faces.TextFace(m[node.name][1] + " (" + m[node.name][0] + ")", fsize=10, fstyle='italic')
            faces.add_face_to_node(N, node, 0)    
            #faces.add_face_to_node(N, node, column=0, position="aligned")
        else:
            print(node.name)

def draw_tree(tree, mapping, outfile, support):
    t = Tree(tree)
    og = ['GCA_903970565.1_BOG_genome_mining.92_sub', 'GCA_001858525.1_ASM185852v1', 'GCA_003864455.1_ASM386445v1']
    lca = t.get_common_ancestor(og)
    t.set_outgroup(lca)
    t.ladderize(direction=1)

    ts = TreeStyle()
    #ts.show_branch_support = True
    ts.branch_vertical_margin = 0
    ts.show_leaf_name = False
    ns = NodeStyle()
    if args.support:
        ts.show_branch_support = True
    ns['shape'] = "square"
    ns['size'] = 0
    ns['vt_line_width'] = 1
    ns['hz_line_width'] = 1
    for n in t.traverse():
        n.set_style(ns)

    global m

    m = {}

    with open(mapping, "r") as mf:
        lines = mf.readlines()
        for line in lines:
            x = line.split("\t")
            m[x[0]] = (x[1], x[2].strip())
            #print(x[0], x[1], x[2])

    ts.layout_fn = treeLayout

    #t.render(file_name=outfile, w=8.5, h=11, units="in", tree_style=ts, dpi=400)
    t.render(file_name=outfile, tree_style=ts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script makes colored tubulin phylogenetic tree for final publication")
    parser.add_argument("-t", "--tree", required=True, help="Tree file")
    parser.add_argument("-m", "--mapping", required=True, help="Mapping file (taxon to clade mapping file)")
    parser.add_argument("-o", "--outfile", required=True, help="Outfile name - PDF")
    parser.add_argument("-s", "--support", action="store_true", default=False, help="Choose this option to show support values")
    args = parser.parse_args()
    draw_tree(args.tree, args.mapping, args.outfile, args.support)
