#py imports
from collections import OrderedDict
from flask import Flask, Response
from flask import request
import redis
import json

#project imports
from config import Config

##################################
## APP SETUP
##################################

#declare application
app = Flask(__name__)
app.debug = True

#config
cfg = Config()

#redis connection
rP = redis.StrictRedis(host = cfg.g('redis','host'), port = cfg.g('redis','port'), db = 0)


##################################
## helper functions
##################################
def WrapCallbackString(result_data):
    callback_string = request.args.get('callback')
    if callback_string:
        results = callback_string
        results += "(" + json.dumps(result_data, indent=4) + ")"
    else:
        results = json.dumps(result_data, indent=4)

    return results


##################################
## REDIS INTERACTION
##################################
def get_item_sim(itemid, numperset):
    return rP.zrevrange(itemid, 0, numperset ,'withscores')
    

def get_item_base(userid, numperset):
    return rP.zrevrange('U-'+userid,0,  numperset, 'withscores')

#will replace this with a lua script in future
def get_multi_items (itemids):
    for i in itemids:
        items = rP.hgetall(i)
        items['itemid']=i #put itemid back into results
        yield items




##################################
## ROUTES
##################################
#index
@app.route('/')
def index():
    return 'rpM Recommender :)'


#get item details
#sample URL:  http://localhost:5000/getItem?item_id=1,2,3,5,6,99&callback=mycallback
#simpler URL: http://localhost:5000/getItem?item_id=1,2,3,5,6,99
@app.route('/getItem')
def get_item():
    #pull the string of ids from the querystring and turn it into an array
    itemid_string = request.args.get('item_id')
    itemArray = itemid_string.split(',')

    items = get_multi_items(itemArray) ## replace this with your code to look up the descriptions

    ## do callback stuff to make javascript clients happy fun time
    #results = WrapCallbackString(resultsArray)
    results = []
    for i in items:
        print i

    return 'grumpy cat'

    #resp = Response(response=results,
    #                status=200,
    #                mimetype="application/json")

    #return resp

    #return itemArray


#recommendation getter
@app.route('/recommender/<string:userid>/<int:itemid>/<int:numitems>',defaults={'mode': 'simple'})
def recommender (userid, itemid, numitems,mode):

    print mode
    #we will retrieve twice the requested recommendations from each set
    numperset = numitems*2

    #get from redis, no pipeline, it's just two calls (for now)
    itemsim = get_item_sim(itemid, numperset)
    itembase = get_item_base(userid, numperset)

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

    #find item attributes
    if mode:  #== 'full':  #can't get optional param to work
        for key in dictRes.keys():
            print rP.hget('I'+key,'name')


    #then we'll sort the dict and take the top results based on numitems
    dictResS = OrderedDict(sorted(dictRes.items(), key=lambda t: t[1], reverse=True)[:numitems])


    #return results
    # great use case: http://127.0.0.1:5000/recommender/572/7/25
    if cfg.g('debug','terminal') == '1':
        print '----\norig item_base:' + str(itembase)
        print '----\norig item_sim:' + str(itemsim)
        print '----\ncombined result:' + str(dictResS)

    results = WrapCallbackString(dictResS)

    resp = Response(response=results,
                    status=200,
                    mimetype="application/json")

    return resp

if __name__ == '__main__':
    app.run()
