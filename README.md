rpM - Redis-Python-Mahout Big Data Recommender
===
This project is meant to be a DIY toolkit for experimenting with a mahout based recommendation engine. Future plans include making a full fledged application.  This is a work in progress but components should work if you follow the instructions carefully!

##Main Components:
* Hadoop / Mahout - any sandbox will do, but you can leverage ours http://www.casertaconcepts.com/resources.  This image includes all necessary components including Redis, Python and a known good snapshot of the project.
* Pig - 0.11 or better (forked pig-redis.jar https://github.com/Simulmedia/pig-redis)
* Redis - 2.8.7
* Python - with redis and flask imports
* Simple UI - client side javascript


##Getting Started:
*Note that this has been tested with Movielens data however any data should work just fine.  Even your real production data

###Python and Redis
The following instructions should help you get the Redis and Python project running on your local env, if you don't plan on doing any development it may be easier to use the Python/Redis environment prebuilt in our VM.

1. Install redis, add the src directory to your path.  Typical path: "/etc/usr/local/redis-2.8.6/src"
2. Start redis ```redis-server```
3. Install Python 2.7
4. Clone the repository
5. Setup Python virtual env
6. Install requirements: pip install -r requirements.txt
7.  At this point you should be able to start RPM (although there is no data in it yet) ```python rpm/rpm.py```
The following message will appear: ```Running on http://127.0.0.1:5000/```

###Hadoop:
In the future we will be making rpM auto-provision EMR and completely automate the workflow, but for now you have two options:

####Option 1  - Use our VM  -->  EASY WAY!
Note: if you are going to use a instance of Redis outside the VM edit the host settings in 7, 8, and 9.

1. Download the VM from  http://www.casertaconcepts.com/resources and follow the Quickstart instructions.
2. Clone the latest version of rpM to the  /home/hduser folder within the VM.
3. Run ```pig ~/rpM/sample_etl/movie_lens_data_to_mahout.pig``` to populate data folders used by itemsimilarity and itembased
4. Run ```pig ~/rpM/sample_etl/movie_lens_user_to_mahout.pig``` to populate user folders used by itembased
5. Run ```./rpM/mahout_cmds/itemsimilarity.sh``` to run itemsimilarity
6. Run ```./rpM/mahout_cmds/itembased.sh``` to run itembased recommender
7. Run ```pig ~/rpM/sample_etl/mahout_item_sim_to_redis.pig```  to populate redis with itemsimilarity zsets
8. Run ```pig ~/rpM/sample_etl/mahout_item_base_to_redis.pig```  to populate redis with itembased zsets
9. If using the sample_ui, run the following to import item info: 
```python rpm/item_import.py ~/rpM/sample_data/movie_lens/u_item.txt```

.. If all went well you should be able to launch sample_ui/index.html
.. or flask app paths directly http://127.0.0.1:5000/recommenderitems/572/7/50/detail OR http://127.0.0.1:5000/recommenderitems/572/7/50

####Option 2 - Build your own or launch on external cluster:
1. Install and configure PIG and Mahout
2. Clone latest RPM
3. Clone and build https://github.com/Simulmedia/pig-redis
4. Go through all scripts and update data directories and hostnames


##Future Plans
The eventual goal of this project is to have a simple easy to deploy tool that will completely automate the calculation and serving of recommendations.
Here is a high level list of to-dos:

* Modularize code
* CI and testing --> Travis
* Document deploying to a real web server
* AWS automation to provision elasticache instance
* AWS automation to provision and execute EMR jobs
* Add features to "recommenderitems": Dithering, algorithm bias
* Integrate more algorithms ALS, Clustering
* Incremental or on-demand itembased recommender in Python
* Comprehensive central config: AWS credentials and provisioning settings, Mahout algorithm params, "recommenderitems" params (dithering, bias, etc)



