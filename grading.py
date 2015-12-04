import snap, json, random
total_tweets = {}
retweeted_by = {}
fav_count = {}
# retweets_count = {}
grades = {}
MAX = 19914
MIN = 1
err_count = 0
#1332460298038.json'

def record_error(l):
    global err_count
    er = open('err.txt', 'a')
    er.write(l+'\n')
    er.close()
    err_count += 1

from os import listdir
from os.path import isfile, join
def count():
    global err_count
    json_files = [f for f in listdir('../StreamingAPITrackData') if f.endswith('.json')]

    total_tweets = {}
    retweeted_by = {}
    fav_count = {}
    for f_name in json_files:
        f = open('../StreamingAPITrackData/' + f_name)
        print 'analysing file: ', f_name
        for l in f:
            try:
                obj = json.loads(l)
            except Exception as e:
                record_error(str(e))
                record_error(l)
                print 'error in reading json'
                continue
            if 'user' not in obj:
                record_error(l)
                print 'tweet without user'
                continue
            usr_id = obj['user']['id']
            if usr_id not in total_tweets:
                total_tweets[usr_id] = 0
            if usr_id not in fav_count:
                fav_count[usr_id] = obj['user']['favourites_count']
            total_tweets[usr_id] += 1

            if 'retweeted_status' in obj:
                if 'user' in obj['retweeted_status']:
                    rt_usr = obj['retweeted_status']['user']['id']
                    if rt_usr not in retweeted_by:
                        retweeted_by[rt_usr] = 0
                    retweeted_by[rt_usr] += 1
    total_file = open('total.txt', 'w')
    total_file.write(str(total_tweets))
    retweet_file = open('rt.txt', 'w')
    retweet_file.write(str(retweeted_by))
    fav_file = open('fav.txt', 'w')
    fav_file.write(str(fav_count))

def calc_baseline():
    global err_count
    json_files = [f for f in listdir('../StreamingAPITrackData') if f.endswith('.json')]

    # train_files = random.sample(json_files, 2)
    train_files = random.sample(json_files, 246)
    test_files = [f for f in json_files if f not in train_files]
    total_tweets = {}
    retweeted_by = {}
    fav_count = {}
    for f_name in train_files:
        f = open('../StreamingAPITrackData/' + f_name)
        print 'analysing file: ', f_name
        for l in f:
            try:
                obj = json.loads(l)
            except Exception as e:
                continue
            if 'user' not in obj:
                continue
            usr_id = obj['user']['id']
            if usr_id not in total_tweets:
                total_tweets[usr_id] = 0
            if usr_id not in fav_count:
                fav_count[usr_id] = obj['user']['favourites_count']
            total_tweets[usr_id] += 1

            if 'retweeted_status' in obj:
                if 'user' in obj['retweeted_status']:
                    rt_usr = obj['retweeted_status']['user']['id']
                    if rt_usr not in retweeted_by:
                        retweeted_by[rt_usr] = 0
                    retweeted_by[rt_usr] += 1

    tweets_list = [total_tweets[k] for k in total_tweets.keys()]
    retweets_list = [retweeted_by[k] for k in retweeted_by.keys()]
    average = sum(retweets_list)*1.0/sum(tweets_list)
    ###testing
    print '**** training is finished, going to test ****'
    err_sum = 0
    for f_name in test_files:
        f = open('../StreamingAPITrackData/' + f_name)
        print 'analysing file: ', f_name
        for l in f:
            try:
                obj = json.loads(l)
            except Exception as e:
                continue
            if 'user' not in obj:
                continue
            user = obj['user']['id']
            pred = 0
            if user in total_tweets and user in retweeted_by:
                pred = retweeted_by[user]*1.0/total_tweets[user]
            else:
                pred = average
            real_rt_count = obj['retweet_count']
            err = pow(pred - real_rt_count, 2)
            err_sum += err
    final_err = err_sum/62.0
    print 'final_err: ', final_err
 

def create_data_frames():
    load_dicts()
    global total_tweets, retweeted_by



def create_graph():
    f = open('edge_list.csv', 'r')
    fout = open('good_graph.csv', 'w')
    for l in f:
        p = l.split(',')
        if p[0] == '-1' or p[1] == '-1':
            continue
        fout.write(p[0]+' '+p[1]+'\n')
    fout.close()

def load_dicts():
    global total_tweets, retweeted_by
    total_tweets_file = open('total.txt', 'r')
    total_tweets = eval(total_tweets_file.read())
    # for l in total_tweets_file:
    #     p = l.split(' ')
    #     total_tweets[eval(p[0])] = eval(p[1].strip())
    retweeted_by_file = open('rt.txt', 'r')
    retweeted_by = eval(retweeted_by_file.read())
    # for l in retweeted_by_file:
    #     p = l.split(' ')
    #     retweeted_by[eval(p[0])] = eval(p[1].strip())
    # retweets_count_file = open('retweet_count.txt', 'r')
    # for l in retweets_count_file:
    #     p = l.split(' ')
    #     retweets_count[eval(p[0])] = eval(p[1].strip())

followers_dic = {}
grades_dic = {}
grades_dic2 = {}
g = None

def run():

    load_dicts()
    global followers_dic, grades_dic, grades_dic2, g
    g = snap.LoadEdgeList(snap.PNGraph, "good_graph.csv", 0, 1)
    
    # followers = snap.TIntPrV()
    # snap.GetNodeInDegV(g, followers)
    # print max(followers, key=lambda item: (item[1])), min(followers, key=lambda item: (item[1]))
    # for p in followers:

    # print g.GetEdges()
    nodes = g.Nodes()
    for n in nodes:
        n_id = n.GetId()
        # print n_id
        followers_n = n.GetInDeg()
        followers_dic[n_id] = followers_n
        # we have negative node numbers!
        s = 0
        c = 0
        avg = 0
        for i in xrange(0, followers_n):
            # print i
            neigh_id = n.GetInNId(i)
            if neigh_id not in followers_dic:

                neigh = g.GetNI(neigh_id)
                followers = neigh.GetInDeg()
                s += followers
                c += 1
                followers_dic[neigh_id] = followers
            else:
                s += followers_dic[neigh_id]
                c += 1
        if c is not 0:
            avg = s*1.0/c
        rt_count = retweeted_by[n_id] if n_id in retweeted_by else 0
        rt_rate = rt_count / total_tweets[n_id] if n_id in total_tweets else 0

        grades_dic[n_id] = (followers_n + avg*rt_rate)/MAX
    file_backup = open("grades1.txt", 'w')
    file_backup.write(str(grades_dic))
    nodes = g.Nodes()
    for n in nodes:
        n_id = n.GetId()
        s = 0
        c = 0
        avg = 0
        for i in xrange(0, followers_dic[n_id]):
            neigh_id = n.GetInNId(i)
            s += grades_dic[neigh_id]
            c += 1
        if c is not 0:
            avg = s*1.0/c
        grades_dic2[n_id] = grades_dic[n_id]* 0.7 + avg*0.3
    file_backup = open("grades2.txt", 'w')
    file_backup.write(str(grades_dic2))
    
# run()



