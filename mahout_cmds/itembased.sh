#!/bin/sh
#will make input params later
#remove files
hadoop fs -rmr /user/movie_lens_rec_item_based
hadoop fs -rmr /app/hadoop/tmp/recommenditembased

#run hadoop
/usr/local/hadoop/mahout/bin/mahout recommenditembased \
  --input /user/movie_lens_data \
  --output /user/movie_lens_rec_item_based \
  --tempDir /app/hadoop/tmp/recommenditembased \
  --usersFile /user/movie_lens_user/part-m-00000 \
  --similarityClassname SIMILARITY_COSINE \
  --numRecommendations 50



