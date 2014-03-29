#!/bin/sh
#will make input params later
#remove files
hadoop fs -rmr /user/movie_lens_rec_item_similarity 
hadoop fs -rmr /app/hadoop/tmp/recommenditemsimilarity

#run hadoop
/usr/local/hadoop/mahout/bin/mahout itemsimilarity \
  --input /user/movie_lens_data \
  --output /user/movie_lens_rec_item_similarity \
  --tempDir /app/hadoop/tmp/recommenditemsimilarity \
  --similarityClassname SIMILARITY_COSINE \

