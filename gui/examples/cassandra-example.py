# import cassandra requires pip3 install cassandra-driver

from cassandra.cluster import Cluster

cluster = Cluster(['localhost'], port=9042)

session = cluster.connect()

session.execute(
    "CREATE KEYSPACE IF NOT EXISTS test WITH replication = { 'class':'SimpleStrategy', 'replication_factor':1 }"
)

session.execute(
    "USE test"
)

### THIS NEED BE DO IN THE CQLSH (attach)
# COPY test.reviews (review_id, app_id, sentiment_type, sentiment_polarity, sentiment_subjectivity, author, content, rating, helpful_count, post_date, developer_reply, developer_reply_post_date) FROM '/bulk_load/cassandra.csv' WITH DELIMITER=';' AND HEADER=TRUE;

# session.execute(
#     "CREATE TABLE IF NOT EXISTS test.reviews (review_id uuid, app_id bigint, sentiment_type text, sentiment_polarity float, sentiment_subjectivity float, author text, content text, rating float, helpful_count decimal, post_date text, developer_reply text, developer_reply_post_date text, PRIMARY KEY(review_id, app_id))"
# )

# session.execute(
#     "CREATE INDEX IF NOT EXISTS apps_index ON test.reviews (app_id)"
# )

# session.execute(
#     "CREATE INDEX IF NOT EXISTS sentiment_index ON test.reviews (sentiment_polarity)"
# )

# session.execute(
#     "CREATE INDEX IF NOT EXISTS rating_index ON test.reviews (rating)"
# )

rows = session.execute(
    "SELECT * FROM test.reviews WHERE app_id IN (1188432952, 1188375927) ALLOW FILTERING"
)

# NOT SUPPORTED (second indexes)
# rows = session.execute(
#     "SELECT * FROM test.reviews WHERE app_id IN (123) ORDER BY sentiment_polarity DESC ALLOW FILTERING"
# )

# NOT SUPPORTED (second indexes)
# rows = session.execute(
#     "SELECT * FROM test.reviews WHERE app_id IN (123) ORDER BY rating ASC ALLOW FILTERING"
# )

print(rows)

for user_row in rows:
    print("Print ID:", user_row.app_id)