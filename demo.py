import timeit
import sys
import statistics
from sqlalchemy import create_engine
import redis
import random

#Arguments and random seed
entries = int(sys.argv[1])
tries = int(sys.argv[2])
percent = int(sys.argv[3])
random.seed(10)

#SQL setup
db_string = #insert your url here
db = create_engine(db_string)
db.execute("DROP TABLE IF EXISTS pairs")
db.execute("CREATE TABLE IF NOT EXISTS pairs (key int, value text)")
for x in range(entries):
    db.execute("INSERT INTO pairs VALUES(%d, 'test')" % x)

#Redis setup
redis_url = #insert your url here
r.flushdb()


#Just SQL
def no_cache():

    #Decide page
    result = None
    entry = None
    roll = random.randint(1, 100)
    if (roll > percent):
        entry = random.randint(1, entries-1)
    else:
        entry = 0

    #Fetch from postgres
    result = db.execute("SELECT value FROM pairs where key=%d" % entry).first()[0]

#SQL + Redis
def cache():

    #Decide page
    result = None
    roll = random.randint(1, 100)
    if (roll > percent):
        entry = random.randint(1, entries-1)
    else:
        entry = 0


    #Fetch from redis
    result = r.get(entry)

    #If miss, then fetch from postgres and store in redis
    if (result == None):
        result = db.execute("SELECT value FROM pairs where key=%d" % entry).first()[0]
        r.set(entry, result)


# Compare first no cache and then with cache
data_no_cache = timeit.timeit(no_cache, number=tries)/tries
data_with_cache = timeit.timeit(cache, number=tries)/tries
print("No cache avg: %f" % data_no_cache)
print("Cache avg: %f" % data_with_cache)
print("Finished")

