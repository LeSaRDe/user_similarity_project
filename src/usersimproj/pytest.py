import nltk
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize
from nltk.parse import corenlp
import gensim
import socket

#(ROOT (S (NP (NP (NNP Align#[00464321v]) (, ,) (NNP Disambiguate#[00957178v]) (, ,) ) (CC and) (NP (NP (VB Walk#[01904930v])) (PRN (-LRB- -LRB-) (NP (NN ADW)) (-RRB- -RRB-)))) (VP (VBZ is) (NP (NP (DT a) (JJ WordNet-based) (NN approach#[00941140n])) (PP (IN for) (S (VP (VBG measuring#[00647094v]) (NP (NP (JJ semantic#[02842042a]) (NN similarity#[04743605n])) (PP (IN of) (NP (NP (JJ arbitrary#[00718924a]) (NNS pairs#[13743605n])) (PP (IN of) (NP (JJ lexical#[02886629a]) (NNS items#[03588414n]))) (, ,) (PP (IN from) (NP (NN word#[06286395n]) (NNS senses#[03990834n])))))) (PP (TO to) (NP (JJ full#[01083157a]) (NNS texts#[06387980n, 06388579n])))))))) (. .)))

con_sent_tree_str = '(ROOT (S (NP (NP L:Align#00464321v L:Disambiguate#00957178v) L:Walk#01904930v) (NP L:approach#00941140n (S (VP L:measuring#00647094v (NP (NP L:semantic#02842042a L:similarity#04743605n) (NP (NP L:arbitrary#00718924a L:pairs#13743605n) (NP L:lexical#02886629a L:items#03588414n) (NP L:word#06286395n L:senses#03990834n))) (NP L:full#01083157a L:texts#06387980n+06388579n))))))'

sent = 'Align, Disambiguate, and Walk (ADW) is a WordNet-based approach for measuring semantic similarity of arbitrary pairs of lexical items, from word senses to full texts.'

#con_parser = corenlp.CoreNLPParser(url='http://localhost:9000')

# this function takes a tree string and returns the graph of this tree
# the format of the input tree string needs follow the CoreNLP Tree def.
# this format is compatible with NLTK Tree.
# the graph is introduced from NetworkX.
def treestr_to_graph(treestr):
    ret_graph = nx.Graph()
    tree = Tree.fromstring(treestr)
    tree_prod = tree.productions()
    for i, p in enumerate(tree_prod):
        p = str(p).split('->')
        p[1] = p[1].split()
        start = p[0]
        ret_graph.add_node(start, type='node')
        for edge_e in p[1]:
            edge_e = edge_e.replace("'", "")
            if edge_e[:2] == "L:":
                word_n_tags = edge_e[:2].split('#')
                end = word_n_tag[0]
                offset_tags = word_n_tag[1].split('+')
                ret_graph.add_node(end, type='leaf', tags = offset_tags)
                ret_graph.add_edge(start, end, weight = 1, type = 'inter')
            else:
                ret_graph.add_node(end, type='node')
                ret_graph.add_edge(start, edge_e, weight = 1, type = 'inter')
            
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
    #treestr_to_graph(con_sent_tree)
    
    send_wordsim_request('oo', ['06387980n', '06388579n'], ['03588414n']) 
    
    
    
    #mytree = Tree('A', [Tree('B', ['C', 'D']), Tree('E', ['F'])])
    #mytree2 = Tree('A', ['B', 'C'])
    #print mytree2

    #t_sent = sent_tokenize(sent)
    #p_sent = con_parser.raw_parse(sent)
    #print t_sent
    #w2v_model = gensim.models.KeyedVectors.load_word2vec_format('/home/fcmeng/nasari/NASARIembed+UMBC_w2v.bin', binary=True)
    #w2v_model.save('NASARIembed+UMBC_w2v+model')
    #w2v_model = gensim.models.KeyedVectors.load("NASARIembed+UMBC_w2v+model")
    #print w2v_model.similarity('woman', 'man')

main()
