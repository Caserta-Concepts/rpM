#py imports
from collections import OrderedDict
from flask import Flask, Response
from flask import request
import redis
import json

#project imports
from config import Config
from recommendation_item import recommendation_item

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
def get_multi_items(itemids):
    results = []
    for itemid in itemids:
        ascii_itemid = itemid.encode('ascii', 'ignore')
        item_results = rP.hgetall(ascii_itemid)
        item_results['itemid'] = ascii_itemid

        results.append(item_results)

    return results

def get_item(itemid):
    return rP.hgetall('I'+itemid)



##################################
## ROUTES
##################################
#index
@app.route('/')
def index():
    return 'rpM Recommender v0.1'


##################################
#get item details
#sample URL:  http://localhost:5000/getItem?item_id=1,2,3,5,6,99&callback=mycallback
#simpler URL: http://localhost:5000/getItem?item_id=1,2,3,5,6,99

@app.route('/getItems')
def get_items():

    #pull the string of ids from the querystring and turn it into an array
    itemid_string = request.args.get('item_id')
    itemArray = itemid_string.split(',')

    items = get_multi_items(itemArray) ## replace this with your code to look up the descriptions

    ## do callback stuff to make javascript clients happy fun time
    results = WrapCallbackString(items)

    resp = Response(response=results,
                    status=200,
                    mimetype="application/json")

    return resp

    #return itemArray

##################################
#recommendation getters
@app.route('/recommenderitems/<string:userid>/<int:itemid>/<int:numitems>/<string:mode>')
@app.route('/recommenderitems/<string:userid>/<int:itemid>/<int:numitems>',defaults={'mode': 'simple'})

def recommenderitems (userid, itemid, numitems,mode):

    retArray = []

    #we will retrieve twice the requested recommendations from each set
    numperset = numitems*2

    #get from redis, no pipeline, it's just two calls (for now)
    itemsim = get_item_sim(itemid, numperset)
    itembase = get_item_base(userid, numperset)

    #get top scores so we can level the two datasets (item base is 1 to 5, item sim 0 to 1)

    if itemsim and itembase:
        topitemsim = itemsim[0][1]
        topitembase = itembase[0][1]
        factor = topitembase/topitemsim
    else:
        factor = 1

    for i in itembase:
        item = recommendation_item();
        item.item_id = i[0]
        item.score = i[1]
        retArray.append(item.__dict__)

    for i in itemsim:
        this_itemid = i[0]
        found_item = [x for x in retArray if x['item_id'] == this_itemid]
        if len(found_item) > 0:
            found_item[0]['score'] = found_item[0]['score'] + i[1]*factor
        else:
            item = recommendation_item();
            item.item_id = i[0]
            item.score = i[1] * factor
            retArray.append(item.__dict__)

    if mode == 'detail':
        for recommendation in retArray:
            item_details = get_item(recommendation['item_id'])
            recommendation.update(item_details)

    newlist = sorted(retArray, key=lambda x: x['score'], reverse=True)[:numitems]

    results = WrapCallbackString(newlist)

    resp = Response(response=results,
                    status=200,
                    mimetype="application/json")

    return resp

if __name__ == '__main__':
    app.run()
