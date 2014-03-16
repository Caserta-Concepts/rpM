#simple script for importing u_iem

import redis
import sys

from config import Config


#config
cfg = Config()

#redis connect (pipeline)
rC = redis.Redis(cfg.g('redis','host'))
pL     = rC.pipeline(cfg.g('redis','port'))


#read file
print sys.argv[1]

itemfile = sys.argv[1]
items = open (itemfile)

#read the lines
records = items.readlines()

#loop split and write to redis
for line in records:
    #print line
    parsed_line = line.split('|')
    #print parsed_line[0]+ ' name ' + parsed_line[1]
    pL.hset ('I'+str(parsed_line[0]),'name', parsed_line[1])
    pL.hset ('I'+str(parsed_line[0]),'imdb', parsed_line[4])


pL.execute()

items.close()
