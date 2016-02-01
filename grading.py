import snap, json, random
total_tweets = {}
retweeted_by = {}
fav_count = {}
# grades1 = {}
grades2 = {}
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
    load_grades()
    global err_count, grades2
    json_files = [f for f in listdir('../StreamingAPITrackData') if f.endswith('.json')]

    # train_files = random.sample(json_files, 2)
    train_files = random.sample(json_files, 246)
    test_files = [f for f in json_files if f not in train_files]
    total_tweets = {}
    retweeted_by = {}
    fav_count = {}
    c = 0
    for f_name in train_files:
        f = open('../StreamingAPITrackData/' + f_name)
        print 'analysing file:(%d/): %s' %(c, f_name)
        c +=1
        for l in f:
            try:
                obj = json.loads(l)
            except Exception as e:
                continue
            if 'user' not in obj:
                continue
            usr_id = obj['user']['id']
            if usr_id not in grades2:
                continue
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
    err_count = 0
    for f_name in test_files:
        f = open('../StreamingAPITrackData/' + f_name, 'r')
        print 'analysing file:(%d/): %s' %(c, f_name)
        c +=1
        for l in f:
            try:
                obj = json.loads(l)
            except Exception as e:
                continue
            if 'user' not in obj:
                continue

            user = obj['user']['id']
            if user not in grades2:
                continue
            pred = 0
            if user in total_tweets and user in retweeted_by:
                pred = retweeted_by[user]*1.0/total_tweets[user]
            else:
                pred = average
            real_rt_count = obj['retweet_count']
            err = pow(pred - real_rt_count, 2)
            # print err
            err_sum += err
            # print 'err: ', err
            err_count += 1
    final_err = err_sum*1.0/err_count
    print 'final_err: ', final_err
    # err = 1568465.62994

total_favs = {}

def load_grades():
    global grades2, total_favs
    grades2_file = open('grades2.txt', 'r')
    grades2 = eval(grades2_file.read())
    fav_file = open('fav.txt', 'r')
    total_favs = eval(fav_file.read())

def create_data_frames():
    print 'loading dict'
    load_dicts()
    print 'loading grades2'
    load_grades()
    data_file = open('data.csv', 'w')
    data_file.write('hashtags, mentions, link, rt_count\n')
    global total_tweets, retweeted_by, grades2, total_favs

    # train_files = random.sample(json_files, 2)
    json_files = [f for f in listdir('../StreamingAPITrackData') if f.endswith('.json')]
    # json_files = json_files[:2]

    err_count = 0
    total_cnt = 0

    idx = 0

    for f_name in json_files:
        f = open('../StreamingAPITrackData/' + f_name, 'r')
        print 'analysing file (%d/308):%s' %(idx+1, f_name)
        idx += 1
        for l in f:
            try:
                obj = json.loads(l)
            except Exception as e:
                continue
            if 'user' not in obj:
                continue
            user_id = obj['user']['id']
            if user_id not in grades2:
                err_count += 1
                continue
            total_cnt += 1
            hashtags = str(len(obj['entities']['hashtags'])) if 'hashtags' in obj['entities'] else '0'
            mentions = str(len(obj['entities']['user_mentions'])) if 'user_mentions' in obj['entities'] else '0'
            link = '1' if 'urls' in obj['entities'] and len(obj['entities']['urls']) > 0 else '0'
            grade = str(grades2[user_id])
            rt_count = str(obj['retweet_count'])
            rt_user_grade = '0'
            if 'retweeted_status' in obj:
                if 'user' in obj['retweeted_status']:
                    rt_usr = obj['retweeted_status']['user']['id']
                    rt_user_grade = str(grades2[rt_usr]) if rt_usr in grades2 else '0'
            
            data = hashtags + ', ' + mentions + ', ' + link + ', ' + grade +\
                 ', ' + rt_user_grade + ', ' + str(total_favs[user_id]) + ',' + rt_count + "\n"
            data_file.write(data)
    data_file.close()
    print 'err_count: ', err_count, 'total_tweets: ', total_cnt



#err_count:  8443637 total_tweets:  2299595
# final error without rt_grade: 633667.1274



def create_graph():
    f = open('edge_list.csv', 'r')
    fout = open('good_graph.csv', 'w')
    for l in f:
        p = l.split(',')
        # if p[0] == '-1' or p[1] == '-1':
        #     continue
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
    g = snap.LoadEdgeList(snap.PUNGraph, "good_graph.csv", 0, 1)
    # g = snap.PNGraph_New()
    # g = snap.ConvertGraph_PNGraph_PUNGraph(g_u, g)

    
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



