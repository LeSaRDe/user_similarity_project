import nltk
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize
from nltk.parse import corenlp
import gensim
import socket
import networkx as nx
import matplotlib.pyplot as plt
import math
import multiprocessing
from multiprocessing import Process
from multiprocessing import Array
import ctypes
from ctypes import *

#(ROOT (S (NP (NP (NNP Align#[00464321v]) (, ,) (NNP Disambiguate#[00957178v]) (, ,) ) (CC and) (NP (NP (VB Walk#[01904930v])) (PRN (-LRB- -LRB-) (NP (NN ADW)) (-RRB- -RRB-)))) (VP (VBZ is) (NP (NP (DT a) (JJ WordNet-based) (NN approach#[00941140n])) (PP (IN for) (S (VP (VBG measuring#[00647094v]) (NP (NP (JJ semantic#[02842042a]) (NN similarity#[04743605n])) (PP (IN of) (NP (NP (JJ arbitrary#[00718924a]) (NNS pairs#[13743605n])) (PP (IN of) (NP (JJ lexical#[02886629a]) (NNS items#[03588414n]))) (, ,) (PP (IN from) (NP (NN word#[06286395n]) (NNS senses#[03990834n])))))) (PP (TO to) (NP (JJ full#[01083157a]) (NNS texts#[06387980n, 06388579n])))))))) (. .)))

con_sent_tree_str ='(ROOT (S (NP (NP L:Align#00464321v L:Disambiguate#00957178v) L:Walk#01904930v) (NP (NP L:WordNet-based L:approach#04746134n) (S (VP L:measuring#00647094v (NP (NP L:semantic#02842042a L:similarity#06251033n) (NP (NP L:arbitrary#00718924a L:pairs#13743605n) (NP L:lexical#02886869a L:items#03588414n) (NP L:word#06286395n L:senses#03990834n))) (NP L:full#01083157a L:texts#06414372n))))))'

sent = 'Align, Disambiguate, and Walk (ADW) is a WordNet-based approach for measuring semantic similarity of arbitrary pairs of lexical items, from word senses to full texts.'

NODE_ID_COUNTER = 0
WORD_SIM_THRESHOLD = 0.40

#con_parser = corenlp.CoreNLPParser(url='http://localhost:9000')

# this function takes a tree string and returns the graph of this tree
# the format of the input tree string needs follow the CoreNLP Tree def.
# this format is compatible with NLTK Tree.
# the graph is introduced from NetworkX.
def treestr_to_graph(treestr, id):
    ret_graph = nx.Graph()
    tree = Tree.fromstring(treestr)
    #checkTree(tree, '0')
    global NODE_ID_COUNTER
    identifyNodes(tree, id)
    tree.set_label(id + ':' + tree.label() + ':' + str(NODE_ID_COUNTER))
    tree_prod = tree.productions()
    print tree_prod
    for i, p in enumerate(tree_prod):
        p = str(p).split('->')
        p[1] = p[1].split()
        start = p[0]
        start = start.strip()
        ret_graph.add_node(start, type='node')
        for edge_e in p[1]:
            end = edge_e.replace("'", "")
            end = end.strip()
            if end[3:5] == "L:":
                word_n_tags = end[5:].split('#')
                if len(word_n_tags) >= 2:
                    offset_tags = word_n_tags[1].split('+')
                    ret_graph.add_node(end, type='leaf', tags = offset_tags)
                else:
                    ret_graph.add_node(end, type='leaf', tags = [])
            else:
                ret_graph.add_node(end, type='node')
            ret_graph.add_edge(start, end.strip(), weight = 1, type = 'intra')
    return ret_graph

def checkTree(tree, id):
    for index, subtree in enumerate(tree):
        subtree_id = id + ":" + str(index)
        print "subtree:" + subtree_id
        print subtree
        if isinstance(subtree, ParentedTree):
            checkTree(subtree, subtree_id)

def identifyNodes(t, idx):
    global NODE_ID_COUNTER
    for index, subtree in enumerate(t):
        if isinstance(subtree, Tree):
            NODE_ID_COUNTER += 1
            subtree.set_label(idx + ':' + subtree.label() + ':' + str(NODE_ID_COUNTER))
            identifyNodes(subtree, idx)
        elif isinstance(subtree, str):
            newVal = idx + ':' + subtree
            t[index] = newVal
        NODE_ID_COUNTER += 1

def send_wordsim_request(mode, input_1, input_2):
    ret = float(0)
    if mode == 'oo':
        synset_1_str = '+'.join(input_1)
        synset_2_str = '+'.join(input_2)
        send_str = mode + '#' + synset_1_str + '#' + synset_2_str
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_sock.bind((socket.gethostbyaddr("127.0.0.1")[0], 8306))
        c_sock.sendto(send_str, (socket.gethostbyaddr("127.0.0.1")[0], 8607))
        try:
            ret_str, serv_addr = c_sock.recvfrom(4096)
            ret = float(ret_str)
            #print float(ret_str)
            return ret
        except socket.error, msg:
            print "Something wrong happened!"
            print msg
        finally:
            c_sock.close()
    return ret

# this function finds all edges between two parsing trees w.r.t. two sentenses.
# an edge will be created only when its weight is greater than a threshold.
# 'tree_1' and 'tree_2' are two parsing trees.
# what is returned is a collection of edges.
def find_inter_edges(tree_1, tree_2):
    edges = []
    leaves_1 = filter(lambda(f, d): d['type'] == 'leaf', tree_1.nodes(data=True))
    leaves_2 = filter(lambda(f, d): d['type'] == 'leaf', tree_2.nodes(data=True))
    for leaf_1 in leaves_1:
        synset_1 = leaf_1[1]['tags']
        for leaf_2 in leaves_2:
            sim = float(0)
            synset_2 = leaf_2[1]['tags']
            if len(synset_1) > 0 and len(synset_2) > 0:
                sim = send_wordsim_request('oo', synset_1, synset_2)
            if sim == float(0):
                if leaf_1[0].split(':')[2].split('#')[0].strip() \
                    == leaf_2[0].split(':')[2].split('#')[0].strip():
                    sim = 1
            if sim > WORD_SIM_THRESHOLD:
                edges.append((leaf_1[0], leaf_2[0], {'weight': sim, 'type': 'inter'}))
            #print "sim:" + leaf_1[0] + ":" + leaf_2[0] + ":" + str(sim)
    #print edges
    return edges

def treestr_pair_to_graph(treestr_1, treestr_2, id_1, id_2):
    graph_1 = treestr_to_graph(treestr_1, id_1)
    graph_2 = treestr_to_graph(treestr_2, id_2)
    inter_edges = find_inter_edges(graph_1, graph_2)
    ret_graph = nx.compose(graph_1, graph_2)
    ret_graph.add_edges_from(inter_edges)
    return ret_graph, inter_edges, graph_1, graph_2

def get_tags_n_leaves(cycle):
    s1_nodes = {"tags": [], "leaves": []}
    s2_nodes = {"tags": [], "leaves": []}
    for node in cycle:
        if node[:2] == 's1':
            if node[3:4] == 'L':
                s1_nodes["leaves"].append(node)
            else:
                s1_nodes["tags"].append(node)
        elif node[:2] == 's2':
            if node[3:4] == 'L':
                s2_nodes["leaves"].append(node)
            else:
                s2_nodes["tags"].append(node)
    return s1_nodes, s2_nodes

def validate_cycle(cycle):
    ret = True
    s1_nodes, s2_nodes = get_tags_n_leaves(cycle)
    if len(s1_nodes["leaves"]) > 2 or len(s2_nodes["leaves"]) > 2:
        ret = False
    return ret, s1_nodes["leaves"], s2_nodes["leaves"]

def find_shortest_path(g1, g2, sub_nodes1, sub_nodes2):
    p1 = set()
    for m in sub_nodes1:
        for n in sub_nodes1:
            if sub_nodes1.index(m) < sub_nodes1.index(n):
                p1.update(nx.shortest_path(g1, source=m, target=n))
    p1 = list(p1)
    p2 = set()
    for m in sub_nodes2:
        for n in sub_nodes2:
            if sub_nodes2.index(m) < sub_nodes2.index(n):
                p2.update(nx.shortest_path(g2, source=m, target=n))
    p2 = list(p2)
    return p1 + p2

def find_min_cycle_basis(graph, tree_1, tree_2):
    pre_cycle_basis = nx.minimum_cycle_basis(graph)
    min_cycle_basis = []
    while len(pre_cycle_basis):
        b = pre_cycle_basis.pop()
        v, sub_s1, sub_s2 = validate_cycle(b)
        if not v:
            p12 = find_shortest_path(tree_1, tree_2, sub_s1, sub_s2)
            H = graph.subgraph(p12)
            sub_cycle_basis = nx.minimum_cycle_basis(H)
            for cc in sub_cycle_basis:
                if cc not in pre_cycle_basis and cc not in min_cycle_basis and cc != b and set(cc) != set(b):
                    pre_cycle_basis.append(cc)
                else:
                    print "[ERR]: Already has this cycle:"
                    print cc
        else:
            min_cycle_basis.append(b)
    return min_cycle_basis

def cal_cycle_weight(cycle, inter_edges):
    s1_nodes, s2_nodes = get_tags_n_leaves(cycle)
    if len(s1_nodes["leaves"]) > 2 or len(s2_nodes["leaves"]) > 2:
        print "[ERR]: Sentence has more than 2 words in one cycle!"
    w1 = len(s1_nodes["tags"]) + 1
    w2 = len(s2_nodes["tags"]) + 1
    arch_weight = math.exp(math.exp(1)) / (math.pow(w1, 3) + math.pow(w2, 3))

    inter_weight = 1
    for link in inter_edges:
        if link[0] in s1_nodes["leaves"]:
            if link[1] in s2_nodes["leaves"]:
                if link[2]["weight"] < inter_weight:
                    inter_weight = link[2]["weight"]

    ret = arch_weight * inter_weight
    return ret

def sim_from_tree_pair_graph(inter_edges, graph, tree_1, tree_2):
    cycle_weights = []
    if len(inter_edges) < 2:
        return 0
    min_cycle_basis = find_min_cycle_basis(graph, tree_1, tree_2)
    for cycle in min_cycle_basis:
        if len(cycle) < 3:
            print "[ERR]: Invalid cycle in the basis: "
            print cycle
            continue;
        cw = cal_cycle_weight(cycle, inter_edges)
        cycle_weights.append(cw)
    return sum(cycle_weights)

def sent_pair_sim(sent_treestr_1, sent_treestr_2, sim_arr, sim_arr_i):
    tp_graph, inter_edges, tree_1, tree_2 = treestr_pair_to_graph(sent_treestr_1, sent_treestr_2, 's1', 's2')
    sim = sim_from_tree_pair_graph(inter_edges, tp_graph, tree_1, tree_2)
    sim_arr[sim_arr_i] = sim
    return sim

def doc_pair_sim(l_sent_treestr_1, l_sent_treestr_2, num_sent_pairs):
    sim_arr = Array(c_double, num_sent_pairs)
    sim_arr_i = 0
    sim_procs = []
    if l_sent_treestr_1 == None or l_sent_treestr_2 == None \
        or len(l_sent_treestr_1) == 0 or len(l_sent_treestr_2) == 0:
        print "[ERR]: Invalid input doc!"
        return 0
    for sent_treestr_1 in l_sent_treestr_1:
        for sent_treestr_2 in l_sent_treestr_2:
            p = Process(target = sent_pair_sim, args = (sent_treestr_1, sent_treestr_2, sim_arr, sim_arr_i))
            sim_procs.append(t)
            sim_arr_i += 1
            p.start()
    for proc in sim_procs:
        proc.join()
    print "[DBG]: doc_pair_sim is done!"
    print "[DBG]: " + " ".join(map(str, sim_arr))
    ret = sum(sim_arr)
    print "[DBG]: " + "final doc sim = " + str(ret)
    return ret
            
def fetchTreeStrFromDB(db_conn, user_id, time_s, time_e):                
    db_cur = db_conn.execute('SELECT parse_trees FROM tb_user_text_full WHERE (user_id = ?) AND (strftime('%Y-%m-%dT%H:%M:%Sz', time) BETWEEN ? AND ?)', [user_id, time_s, time_e])
    l_tree_str = []
    for row in db_cur:
        l_tree_str.append(row[0])
    return l_tree_str

    


def main():
    #con_sent_tree = Tree.fromstring(con_sent_tree_str)
    #t_production = con_sent_tree.productions()
    #print con_sent_tree
    #print t_production
    #sent_tree = treestr_to_graph(con_sent_tree_str, 's1')
    #print sent_tree
    #find_inter_edges(sent_tree, sent_tree)
    tp_graph, inter_edges, tree_1, tree_2 = treestr_pair_to_graph(con_sent_tree_str, con_sent_tree_str, 's1', 's2')
    sim = sim_from_tree_pair_graph(inter_edges, tp_graph, tree_1, tree_2)
    print "----------------------------------------"
    print tp_graph.nodes
    print "----------------------------------------"
    print tp_graph.edges
    print "----------------------------------------"
    print sim
    print "----------------------------------------"


    #plt.subplot(111)
    #nx.draw(sent_tree, with_labels=True, font_weight='bold')
    #plt.show()

    #send_wordsim_request('oo', ['06387980n', '06388579n'], ['03588414n'])

main()
