---
data = LOAD '/user/movie_lens/u.data' AS (id:int, item:int, rating:int);    
STORE data INTO '/user/movie_lens_data' USING PigStorage(',')    
 
