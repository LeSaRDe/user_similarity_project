import nltk
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize
from nltk.parse import corenlp
import gensim
import socket
import networkx as nx
import matplotlib.pyplot as plt

#(ROOT (S (NP (NP (NNP Align#[00464321v]) (, ,) (NNP Disambiguate#[00957178v]) (, ,) ) (CC and) (NP (NP (VB Walk#[01904930v])) (PRN (-LRB- -LRB-) (NP (NN ADW)) (-RRB- -RRB-)))) (VP (VBZ is) (NP (NP (DT a) (JJ WordNet-based) (NN approach#[00941140n])) (PP (IN for) (S (VP (VBG measuring#[00647094v]) (NP (NP (JJ semantic#[02842042a]) (NN similarity#[04743605n])) (PP (IN of) (NP (NP (JJ arbitrary#[00718924a]) (NNS pairs#[13743605n])) (PP (IN of) (NP (JJ lexical#[02886629a]) (NNS items#[03588414n]))) (, ,) (PP (IN from) (NP (NN word#[06286395n]) (NNS senses#[03990834n])))))) (PP (TO to) (NP (JJ full#[01083157a]) (NNS texts#[06387980n, 06388579n])))))))) (. .)))

con_sent_tree_str = '(ROOT (S (NP (NP L:Align#00464321v L:Disambiguate#00957178v) L:Walk#01904930v) (NP L:approach#00941140n (S (VP L:measuring#00647094v (NP (NP L:semantic#02842042a L:similarity#04743605n) (NP (NP L:arbitrary#00718924a L:pairs#13743605n) (NP L:lexical#02886629a L:items#03588414n) (NP L:word#06286395n L:senses#03990834n))) (NP L:full#01083157a L:texts#06387980n+06388579n))))))'

sent = 'Align, Disambiguate, and Walk (ADW) is a WordNet-based approach for measuring semantic similarity of arbitrary pairs of lexical items, from word senses to full texts.'

NODE_ID_COUNTER = 0

#con_parser = corenlp.CoreNLPParser(url='http://localhost:9000')

# this function takes a tree string and returns the graph of this tree
# the format of the input tree string needs follow the CoreNLP Tree def.
# this format is compatible with NLTK Tree.
# the graph is introduced from NetworkX.
def treestr_to_graph(treestr):
    ret_graph = nx.Graph()
    tree = Tree.fromstring(treestr)
    #checkTree(tree, '0')
    global NODE_ID_COUNTER
    identifyNodes(tree, 's1:')
    tree.set_label('s1:' + tree.label() + ':' + str(NODE_ID_COUNTER))
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
                offset_tags = word_n_tags[1].split('+')
                ret_graph.add_node(end, type='leaf', tags = offset_tags)
            else:
                ret_graph.add_node(end, type='node')
            ret_graph.add_edge(start, end.strip(), weight = 1, type = 'inter')
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
            subtree.set_label(idx + subtree.label() + ':' + str(NODE_ID_COUNTER))
            identifyNodes(subtree, idx)
        elif isinstance(subtree, str):
            newVal = idx + subtree
            t[index] = newVal
        NODE_ID_COUNTER += 1

def send_wordsim_request(mode, input_1, input_2):
    if mode == 'oo':
        synset_1_str = '+'.join(input_1)
        synset_2_str = '+'.join(input_2)
        send_str = mode + '#' + synset_1_str + '#' + synset_2_str
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_sock.bind((socket.gethostbyaddr("127.0.0.1")[0], 8306))
        c_sock.sendto(send_str, (socket.gethostbyaddr("127.0.0.1")[0], 8607))
        try:
            ret_str, serv_addr = c_sock.recvfrom(4096)
            print float(ret_str)
        except socket.error, msg:
            print "Something wrong happened!"
            print msg
        finally:
            c_sock.close()

def main():
    #con_sent_tree = Tree.fromstring(con_sent_tree_str)
    #t_production = con_sent_tree.productions()
    #print con_sent_tree
    #print t_production
    sent_tree = treestr_to_graph(con_sent_tree_str)
    plt.subplot(111)
    nx.draw(sent_tree, with_labels=True, font_weight='bold')
    plt.show()

    #send_wordsim_request('oo', ['06387980n', '06388579n'], ['03588414n'])

main()
