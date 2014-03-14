#py imports
from collections import OrderedDict
from flask import Flask
import redis

#project imports
from config import Config

#declare application
app = Flask(__name__)

#config
cfg = Config()

#redis connection
rP = redis.StrictRedis(host = cfg.g('redis','host'), port = cfg.g('redis','port'), db = 0)

#index
@app.route('/')
def index():
    return 'rpM Recommender :)'

#recommendation getter
@app.route('/recommender/<string:userid>/<int:itemid>')
def recommender (userid, itemid):

    #get from redis, no pipeline, it's just two calls (for now)
    itemsim = rP.zrevrange(itemid, 0, 25 ,'withscores')
    itembase = rP.zrevrange('U-'+userid,0, 25, 'withscores')

    #get top scores so we can level the two datasets (item base is 1 to 5, item sim 0 to 1)

    if  itemsim and itembase:
        topitemsim = itemsim[0][1]
        topitembase = itembase[0][1]
        factor = topitembase/topitemsim
    else:
        factor = 1

    #next we'll spin these lists into a results dict, toping and adding scores
    dictRes = dict()

    for i in itembase:
        dictRes[i[0]] = i[1]

    for i in itemsim:
        if i[0] in dictRes:
            dictRes[i[0]] = dictRes[i[0]] + i[1]*factor
        else:
            dictRes[i[0]] = i[1]*factor

    #then we'll sort the dict
    dictResS = OrderedDict(sorted(dictRes.items(), key=lambda t: t[1], reverse=True))
    #return results - for now just the raw recommendations, but later from the dict
    #maybe a nice json representation or html page

    # great use case: http://127.0.0.1:5000/recommender/7/572
    if cfg.g('debug','terminal') == '1':
        print '----\norig item_base:' + str(itembase)
        print '----\norig item_sim:' + str(itemsim)
        print '----\ncombined result:' + str(dictResS)

    return  str(dictResS)

if __name__ == '__main__':
    app.run()