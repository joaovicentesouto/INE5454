from cassandra.cluster import Cluster

cluster = Cluster(['localhost'], port=9042)

session = cluster.connect()

session.execute(
    "CREATE KEYSPACE IF NOT EXISTS test WITH replication = { 'class':'SimpleStrategy', 'replication_factor':1 }"
)

session.execute(
    "USE test"
)

session.execute(
    "CREATE TABLE IF NOT EXISTS test.reviews (review_id uuid, app_id bigint, sentiment_type text, sentiment_polarity float, sentiment_subjectivity float, author text, content text, rating float, helpful_count decimal, post_date text, developer_reply text, developer_reply_post_date text, PRIMARY KEY(review_id, app_id))"
)


session.execute(
    "CREATE INDEX IF NOT EXISTS apps_index ON test.reviews (app_id)"
)

session.execute(
    "CREATE INDEX IF NOT EXISTS sentiment_index ON test.reviews (sentiment_polarity)"
)

session.execute(
    "CREATE INDEX IF NOT EXISTS rating_index ON test.reviews (rating)"
)

session.execute(
        "INSERT INTO test.reviews (review_id, app_id, sentiment_type, sentiment_polarity, sentiment_subjectivity, author, content, rating, helpful_count, post_date, developer_reply, developer_reply_post_date) VALUES (6ba2870d-c0d6-4234-949f-9ccbf073afa8, 123, 'Positive', -1, -1, 'dummy', 'dummy', 4.5, 0, '2019-01-01', 'dummy', '2019-01-01')"
)

session.execute(
        "INSERT INTO test.reviews (review_id, app_id, sentiment_type, sentiment_polarity, sentiment_subjectivity, author, content, rating, helpful_count, post_date, developer_reply, developer_reply_post_date) VALUES (6ba2870d-c0d6-4234-949f-9ccbf078afa7, 123, 'Positive', 1, 1, 'dummy', 'dummy', 3.5, 0, '2019-01-01', 'dummy', '2019-01-01')"
)

session.execute(
        "INSERT INTO test.reviews (review_id, app_id, sentiment_type, sentiment_polarity, sentiment_subjectivity, author, content, rating, helpful_count, post_date, developer_reply, developer_reply_post_date) VALUES (6ba2870d-c0d6-4234-949f-9ccbf077afa8, 456, 'Positive', -1, -1, 'dummy', 'dummy', 4.5, 0, '2019-01-01', 'dummy', '2019-01-01')"
)

session.execute(
        "INSERT INTO test.reviews (review_id, app_id, sentiment_type, sentiment_polarity, sentiment_subjectivity, author, content, rating, helpful_count, post_date, developer_reply, developer_reply_post_date) VALUES (6ba2870d-c0d6-4234-949f-9ccbf077afa7, 456, 'Positive', 1, 1, 'dummy', 'dummy', 3.5, 0, '2019-01-01', 'dummy', '2019-01-01')"
)

# rows = session.execute(
#     "SELECT * FROM test.reviews WHERE app_id = 123 ALLOW FILTERING"
# )

rows = session.execute(
    "SELECT * FROM test.reviews WHERE app_id IN (123, 456) ALLOW FILTERING"
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