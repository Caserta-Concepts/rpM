---
lens_users= LOAD '/user/movie_lens/u.user' USING PigStorage('|') AS (id:int);
STORE lens_users INTO '/user/movie_lens_user'
