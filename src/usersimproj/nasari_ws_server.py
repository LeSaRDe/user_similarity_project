import socket
import gensim
import os
from multiprocessing.dummy import Pool

SERV_PORT = 8306
WV_MODEL_BIN = "/home/fcmeng/nasari/NASARIembed+UMBC_w2v.bin"
WV_MODEL = "/home/fcmeng/nasari/NASARIembed+UMBC_w2v_model"

g_wv_model = None
g_serv_sock = None

def load_nasari_w2v():
    if not os.path.isfile(WV_MODEL):
        wv_model = gensim.models.KeyedVectors.load_word2vec_format(WV_MODEL_BIN, binary=True) 
        wv_model.save(WV_MODEL)
    wv_model = gensim.models.KeyedVectors.load(WV_MODEL)
    return wv_model

def compute_ws(param):
    global g_wv_model
    global g_serv_sock
    msg = param[0]
    addr = param[1]
    demsg = msg.split("#") 
    ws = g_wv_model.similarity(demsg[0], demsg[1])
    print "sim = " + str(ws)
    print "client = "
    print addr
    g_serv_sock.sendto(str(ws), addr)

def main():
    global g_wv_model
    global g_serv_sock
    g_serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    g_serv_sock.bind(("", SERV_PORT))
    t_pool = Pool(500)
    g_wv_model = load_nasari_w2v()
    while True:
       msg, addr = g_serv_sock.recvfrom(4096)
       param = (msg, addr)
       l_param = list()
       l_param.append(param)
       print l_param
       t_pool.map(compute_ws, l_param)

main()

