--item sim                                 
 
REGISTER '/home/hduser/libs/pig-redis.jar';
 
raw = LOAD '/user/movie_lens_rec_item_similarity'
  USING PigStorage('\t') as (item1:chararray, item2:chararray, rating:chararray);
 
exp_tuple = FOREACH raw GENERATE item1, TOTUPLE(item2, rating);

exp_tuple2 = FOREACH raw GENERATE item2, TOTUPLE(item1, rating);

result = UNION exp_tuple, exp_tuple2;

STORE result INTO 'dummy' USING com.hackdiary.pig.RedisStorer('zset','192.168.56.1');
 

