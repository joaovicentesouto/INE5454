# INE5454
Special Topics in Data Management: Reverse Engineering and Polyglot Persistence

# Data

The following sections present the data used in this project.

## Sources

We will work over the following three datasets to create the polyglot persistence application:
- [Google Play Store Apps](https://www.kaggle.com/lava18/google-play-store-apps)
- [Mobile App Store](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps)
- [Shopify app store](https://www.kaggle.com/usernam3/shopify-app-store)

## Raw

Attribute   | Google                                                       | Apple                                                                 | Shopify
---         | ---                                                          | ---                                                                   | ---
Identifier  | App                                                          | id <br>track_name</br>                                                | id <br>title</br> app_id
Description | ...                                                          | app_desc                                                              | tagline <br>description</br> description_raw <br>description(benefits)</br>
Category    | Category <br>Genres</br>                                     | prime_genre                                                           | category_id <br>title(category)</br> title(benefits)
Rating      | Rating <br>Content Rating</br>                               | user_rating <br>user_rating_ver</br> cont_rating                      | rating <br>rating(reviews)</br>
Reviews     | Reviews <br>Translated Review</br>                           | rating_count_tot <br>rating_count_ver</br> <br>Translated Review</br> | reviews_count <br>author</br> body <br>helpful_count</br> posted_at <br>developer_reply</br> developer_reply_posted_at
Language    | ...                                                          | lang.num                                                              | ...
Size        | Size                                                         | size_bytes                                                            | ...
Download    | Installs                                                     | ...                                                                   | ...
Price       | TypePaid <br>Price</br>                                      | currency <br>price</br>                                               | pricing_hint <br>pricing_plan_id</br> feature(pricing_plan) <br>price</br> title(pricing_plan)
Version     | Last Updated <br>Current Ver</br> Android Ver               | ver                                                                   | ...
Developer   | ...                                                          | ...                                                                   | developer <br>developer_link</br>
Sentiment   | Sentiment <br>Sentiment_Polarity</br> Sentiment_Subjectivity | ...                                                                   | ...
Others      | ...                                                          | sup_devices.num <br>ipadSc_urls.num</br> vpp_lic                      | icon <br>url</br>