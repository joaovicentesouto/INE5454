
CREATE KEYSPACE IF NOT EXISTS "test" WITH replication = { 'class':'SimpleStrategy', 'replication_factor':1 };

use test;

CREATE TABLE "test"."reviews" (review_id uuid, app_id bigint, sentiment_type text, sentiment_polarity float, sentiment_subjectivity float, author text, content text, rating float, helpful_count decimal, post_date text, developer_reply text, developer_reply_post_date text, PRIMARY KEY(review_id));

COPY "test"."reviews" (review_id, app_id, sentiment_type, sentiment_polarity, sentiment_subjectivity, author, content, rating, helpful_count, post_date, developer_reply, developer_reply_post_date) FROM '/mnt/example.csv' WITH DELIMITER=';' AND HEADER=TRUE;

SELECT * FROM "test"."reviews";