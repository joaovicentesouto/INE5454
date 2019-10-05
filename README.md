# INE5454
Special Topics in Data Management: Reverse Engineering and Polyglot Persistence

# Data

The following sections present the data used in this project.

## Sources

We will work over the following three datasets to create the polyglot persistence application:
- [Google Play Store Apps](https://www.kaggle.com/lava18/google-play-store-apps)
- [Mobile App Store (Apple)](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps)
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
Version     | Last Updated <br>Current Ver</br> Android Ver                | ver                                                                   | ...
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

    Apps (*Name, #Category_Id, #Price_Type_Id, #Age_Rating_Id, Rating, N_of_Reviews, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Genres (*Id, Name)
    Apps_Genres (*#App_Name, *#Genre_Id)
    Category (*Id, Name)
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

    Table A = Apps (*Name, #Category_Id, #Price_Type_Id, #Age_Rating_Id, Rating, N_of_Reviews, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Table B = Apps (*Name)

    Table A + B = Apps (*Name, #Category_Id, #Price_Type_Id, #Age_Rating_Id, Rating, N_of_Reviews, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)

    Genres (*Id, Name)
    Apps_Genres (*#App_Name, *#Genre_Id)
    Category (*Id, Name)
    Price_Type (*Id, Type)
    Age_Rating (*Id, Age)
    Reviews (*Id, #App_Name, #Sentiment_Type_Id, Translated_Review, Sentiment_Polarity, Sentiment_Subjectivity)
    Sentiment_Type (*Id, Type)

  2. With Contained Key = With the same Primary Key

  3. Third Normal Form = With the same Primary Key

  4. Final Result:

    Apps (*Name, #Category_Id, #Price_Type_Id, #Age_Rating_Id, Rating, N_of_Reviews, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    Reviews (*Id, #App_Name, #Sentiment_Type_Id, Translated_Review, Sentiment_Polarity, Sentiment_Subjectivity)
    Apps_Genres (*#App_Name, *#Genre_Id)
    Sentiment_Type (*Id, Type)
    Price_Type (*Id, Type)
    Age_Rating (*Id, Age)
    Category (*Id, Name)
    Genres (*Id, Name)

### Apple Store

#### AppleStore.csv file:

  1. Not Normalized:

    (*Id, Name, Size, (Currency), Price, N_of_Rating, N_of_Rating_Curr_Version, Rating, Rating_Curr_Version, Version, (Age_Rating), (Genre), N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)

  1.5. Mapping Names:

    Id -> id
    Name -> track_name
    Size -> size_bytes
    Currency -> currency
    Price -> price
    N_of_Rating -> rating_count_tot
    N_of_Rating_Curr_Version -> rating_count_ver
    Rating -> user_rating
    Rating_Curr_Version -> user_rating_ver
    Version -> ver
    Age_Rating -> cont_rating
    Genre -> prime_genre
    N_of_Supported_Devices -> sup_devices.num
    N_of_ipad_URLs -> ipadSc_urls.num
    N_of_Available_Languages -> lang.num
    Belongs_To_Volume_Purchase_Program -> vpp_lic

  2. First Normal Form:

    Apps (*Id, Name, Size, #Currency_Id, Price, N_of_Rating, N_of_Rating_Curr_Version, Rating, Rating_Curr_Version, Version, #Age_Id, #Genre_Id, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)
    Genres (*Id, Genre)
    Currencies (*Id, Currency)
    Age_Ratings (*Id, Age_Rating)

  3. Second Normal Form = First Normal Form

  4. Third Normal Form:
  
    (*Id, #Currency_Id) -> Price
    
    Apps (*Id, Name, Size, N_of_Rating, N_of_Rating_Curr_Version, Rating, Rating_Curr_Version, Version, #Age_Id, #Genre_Id, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)
    Genres (*Id, Genre)
    Currencies (*Id, Currency)
    Age_Ratings (*Id, Age_Rating)
    Prices (*#App_Id, *#Currency_Id, Price)

  5. Fourth Normal Form = Third Normal Form

#### appleStore_description.csv file:

  1. Not Normalized:

    (*Id, Name, Size, Description)

  1.5. Mapping Names:

    Id -> id
    Name -> track_name
    Size -> size_bytes
    Description -> app_desc

  2. First Normal Form:

    Apps (*Id, Name, Size, Description)

  3. Second Normal Form = First Normal Form

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### AppleStore_Reviews.csv file:

  1. Not Normalized:

    (*Id, (*Review_Id, Review))

  1.5. Mapping Names:

    Id -> id
    Review_Id -> codigo_review
    Review -> review

  2. First Normal Form:

    Apps (*Id)
    Reviews (*#App_Id, *Review_Id, Review)

  3. Second Normal Form:
  
    (*Review_Id) -> Review
    
    Apps (*Id)
    Reviews (*Review_Id, Review)
    AppReviews (*#App_Id, *#Review_Id)

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### Integration (Normalization of Datasets 1 + 2 + 3):

  1. With the same Primary Key:

    Table A = Apps (*Id, Name, Size, N_of_Rating, N_of_Rating_Curr_Version, Rating, Rating_Curr_Version, Version, #Age_Id, #Genre_Id, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)
    Table B = Apps (*Id, Name, Size, Description)
    Table C = Apps (*Id)

    Table A + B + C = Apps (*Id, Name, Size, N_of_Rating, N_of_Rating_Curr_Version, Rating, Rating_Curr_Version, Version, #Age_Id, #Genre_Id, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program, Description)

    Genres (*Id, Genre)
    Currencies (*Id, Currency)
    Prices (*#App_Id, *#Currency_Id, Price)
    Age_Ratings (*Id, Age_Rating)
    Reviews (*Review_Id, Review)
    AppReviews (*#App_Id, *#Review_Id)

  2. With Contained Key = With the same Primary Key

  3. Third Normal Form = With the same Primary Key

  4. Final Result:

    Apps (*Id, Name, Size, Version, Description, #Genre_Id, #Age_Id, Rating, Rating_Curr_Version, N_of_Rating, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)
    Genres (*Id, Genre)
    Currencies (*Id, Currency)
    Prices (*#App_Id, *#Currency_Id, Price)
    Age_Ratings (*Id, Age_Rating)
    Reviews (*Review_Id, Review)
    AppReviews (*#App_Id, *#Review_Id)

### Shopify Store
