#py imports
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
@app.route('/recommender/<int:itemid>/<string:userid>')
def recommender (itemid,userid):

    #get from redis, no pipeline, it's just two calls (for now)
    itemsim = rP.zrevrange(itemid, 0, 9 ,'withscores')
    itembase = rP.zrevrange('U-'+userid,0, 9, 'withscores')

    #get top scores so we can level the two datasets (item base is 1 to 5, item sim 0 to 1)
    topitemsim = itemsim[0][1]
    topitembase = itembase[0][1]

    #next we'll spin these lists into a results dict, toping and adding scores

    #then we'll sort the dict

    #return resutls - for now just the raw recommendations, but later from the dict
    #maybe a nice json representation or html page
    results = '\nitem_base:' + str(itembase) + ' \nitem_sim:' + str(itemsim)

    return results


if __name__ == '__main__':
    app.run()