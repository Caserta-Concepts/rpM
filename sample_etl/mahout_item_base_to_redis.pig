 
--item base
REGISTER '/home/hduser/libs/pig-redis.jar' ;                                      
 
raw = LOAD '/user/movie_lens_rec_item_based'
  USING PigStorage('\t') as (user:chararray, results:chararray);
 
exp_1 = FOREACH raw
  GENERATE user, FLATTEN(TOKENIZE(results,',')) as results;
 
exp_2 = FOREACH exp_1
  GENERATE CONCAT('U-',user) as user, 
    STRSPLIT(REPLACE(REPLACE(results,'\\]',''),'\\[',''),':') as results;
 
STORE exp_2 INTO 'dummy' USING com.hackdiary.pig.RedisStorer('zset','192.168.56.1');
