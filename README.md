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

## Fist Step - Datasets Normalization

### Google Play Store

#### googleplaystore.csv file:

  1. Not Normalized:

    (*App, Category, Rating, Reviews, Size, Installs, Type, Price, Content Rating, (Genres), Last Update, Current Ver, Android Ver)

  1.5. Mapping Names:

    App -> Name
    Reviews -> N_of_Reviews
    Installs -> N_of_Downloads
    Type -> Price_Type
    Content Rating -> Age_Rating
    Last Update -> Latest_Update_at_Store
    Current Ver -> Curr_Version_Available
    Android Ver -> Android_Version_Required

  2. First Normal Form:

    Apps (*Name, Category, Rating, N_of_Reviews, Size, N_of_Downloads, Price_Type, Price, Age_Rating, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Genres (*Id, *#App_Name, Name)

  3. Second Normal Form:

    Apps (*Name, Category, Rating, N_of_Reviews, Size, N_of_Downloads, Price_Type, Price, Age_Rating, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Genres (*Id, Name)
    Apps_Genres (*#App_Name, *#Genre_Id)

  4. Third Normal Form:

    Apps (*Name, #Category_Id, #Rating_Id, #Price_Type_Id, #Age_Rating_Id, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Genres (*Id, Name)
    Apps_Genres (*#App_Name, *#Genre_Id)
    Category (*Id, Name)
    Rating (*Id, Value, N_of_Reviews)
    Price_Type (*Id, Type)
    Age_Rating (*Id, Age)

  5. Fourth Normal Form = Third Normal Form

#### googleplaystore_user_reviews.csv file:

  1. Not Normalized:

    (App, (*Id, Translated_Review, Sentiment, Sentiment_Polarity, Sentiment_Subjectivity))

  1.5. Mapping Names:

    App -> App_Name
    Sentiment -> Sentiment_Type

  2. First Normal Form:

    Apps (*Name)
    Reviews (*Id, #App_Name, Translated_Review, Sentiment_Type, Sentiment_Polarity, Sentiment_Subjectivity)

  3. Second Normal Form = First Normal Form

  4. Third Normal Form:

    Apps (*Name)
    Reviews (*Id, #App_Name, #Sentiment_Type_Id, Translated_Review, Sentiment_Polarity, Sentiment_Subjectivity)
    Sentiment_Type (*Id, Type)

  5. Fourth Normal Form = Third Normal Form

#### Integration (Normalization of Datasets 1 + 2):

  1. With the same Primary Key:

    Table A = Apps (*Name, #Category_Id, #Rating_Id, #Price_Type_Id, #Age_Rating_Id, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Table B = Apps (*Name)

    Table A + B = Apps (*Name, #Category_Id, #Rating_Id, #Price_Type_Id, #Age_Rating_Id, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)

    Genres (*Id, Name)
    Apps_Genres (*#App_Name, *#Genre_Id)
    Category (*Id, Name)
    Rating (*Id, Value, N_of_Reviews)
    Price_Type (*Id, Type)
    Age_Rating (*Id, Age)
    Reviews (*Id, #App_Name, #Sentiment_Type_Id, Translated_Review, Sentiment_Polarity, Sentiment_Subjectivity)
    Sentiment_Type (*Id, Type)

  2. With Contained Key = With the same Primary Key

  3. Third Normal Form = With the same Primary Key

  4. Final Result:

    Apps (*Name, #Category_Id, #Rating_Id, #Price_Type_Id, #Age_Rating_Id, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Reviews (*Id, #App_Name, #Sentiment_Type_Id, Translated_Review, Sentiment_Polarity, Sentiment_Subjectivity)
    Apps_Genres (*#App_Name, *#Genre_Id)
    Rating (*Id, Value, N_of_Reviews)
    Sentiment_Type (*Id, Type)
    Price_Type (*Id, Type)
    Age_Rating (*Id, Age)
    Category (*Id, Name)
    Genres (*Id, Name)
