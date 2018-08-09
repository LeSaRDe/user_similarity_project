import itertools

USER_LIST_FILE = '/home/fcmeng/gh_data/top100users'
USER_SIM_CONFIG = '/home/fcmeng/user_similarity_project/user_sim_config'
MONTH_LIST_FILE = '/home/fcmeng/user_similarity_project/month_list'

def main():
    l_user= []
    with open(USER_LIST_FILE, 'r') as ulf:
        l_user = ulf.readlines()
        l_user = [x.strip() for x in l_user]
    #print l_user

    user_comb_gen = itertools.combinations(l_user, 2)
    l_user_comb = list(user_comb_gen)
    print len(l_user_comb)
     
    l_mon = []
    with open(MONTH_LIST_FILE, 'r') as mlf:
        l_mon = mlf.readlines()
        l_mon = [x.strip() for x in l_mon]
    l_mon_comb = zip(*(l_mon[i:] for i in xrange(2)))
    print len(l_mon_comb)

    l_config = []
    for uu in l_user_comb:
        for mm in l_mon_comb:
            l_config.append((uu[0], uu[1], mm[0], mm[1]))
    print len(l_config)


    with open(USER_SIM_CONFIG, 'w') as usc:
        for one_config in l_config:
            config_str = '|'.join(one_config)
            config_str += '\n'
            usc.write(config_str)

main()
