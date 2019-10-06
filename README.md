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
    Apps_Reviews (*#App_Id, *#Review_Id)

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
    Apps_Reviews (*#App_Id, *#Review_Id)

  2. With Contained Key = With the same Primary Key

  3. Third Normal Form = With the same Primary Key

  4. Final Result:

    Apps (*Id, Name, Size, Version, Description, #Genre_Id, #Age_Id, Rating, Rating_Curr_Version, N_of_Rating, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)
    Genres (*Id, Genre)
    Currencies (*Id, Currency)
    Prices (*#App_Id, *#Currency_Id, Price)
    Age_Ratings (*Id, Age_Rating)
    Reviews (*Review_Id, Review)
    Apps_Reviews (*#App_Id, *#Review_Id)

### Shopify Store

#### apps.csv file:

  1. Not Normalized:

    (*Id, Url, Title, Tagline, Developer, Developer link, Icon, Rating, Reviews_count, Description, Description_Raw, Price_Hint)

  1.5. Mapping Names:

    Title -> Name
    Developer link -> Developer_Link
    Price_Hint -> Free_Trial_Days

  2. First Normal Form:

    Apps (*Id, Url, Name, Tagline, Developer, Developer_Link, Icon, Rating, Reviews_count, Description, Description_Raw, Free_Trial_Days)

  3. Second Normal Form == First Normal Form

  4. Third Normal Form:

    Apps (*Id, Url, Name, Tagline, #Developer_Id, Icon, Rating, Reviews_count, Description, Description_Raw, Free_Trial_Days)
    Developers (*Id, Name, Link)

  5. Fourth Normal Form = Third Normal Form

#### apps_categories.csv file:

  1. Not Normalized:

    (*App_Id, *Category_Id)

  2. First Normal Form:

    Apps_Categories (*App_Id, *Category_Id)

  3. Second Normal Form == First Normal Form

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### categories.csv file:

  1. Not Normalized:

    (*Id, Title)

  1.5. Mapping Names:

    Title -> Name

  2. First Normal Form:

    Categories (*Id, Name)

  3. Second Normal Form == First Normal Form

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### key_benefits.csv file:

  1. Not Normalized:

    (*App_Id, Title, Description)

  1.5. Mapping Names:

    Title -> Benefit_Name
    Description -> Benefit_Description

  2. First Normal Form:

    Apps (*Id, Benefit_Name, Benefit_Description)

  3. Second Normal Form == First Normal Form

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### pricing_plans.csv file:

  1. Not Normalized:

    (*App_Id, (*Id, Title), price)

  1.5. Mapping Names:

    Title -> Name

  2. First Normal Form:

    Apps (*Id, Price)
    Price_plans (*Id, *#App_Id, Name)

  3. Second Normal Form:

    Apps (*Id, Price)
    Price_plans (*Id, Name)
    Apps_Price_plans (*#App_Id, *#Price_Plans_Id)

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### pricing_plan_features.csv file:

  1. Not Normalized:

    (*App_Id, *Pricing_Plan_Id, Feature)

  2. First Normal Form:

    Apps_Pricing_Plans_Features (*App_Id, *Pricing_Plan_Id, Feature)

  3. Second Normal Form == First Normal Form

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Formm

#### reviews.csv file:

  1. Not Normalized:

    (*Id, App_Id, Author, Body, Rating, Helpful_Count, Posted_At, Developer_Reply, Developer_Reply_Posted_At)

  1.5. Mapping Names:

    Body -> Content
    Posted_At -> Post_Date
    Developer_Reply_Posted_At -> Developer_Reply_Post_Date

  2. First Normal Form:

    Reviews (*Id, App_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date)

  3. Second Normal Form = First Normal Form

  4. Third Normal Form = Second Normal Form

  5. Fourth Normal Form = Third Normal Form

#### Integration (Normalization of Datasets 1 + 2 + 3 + 4 + 5 + 6 + 7):

  1. With the same Primary Key:

    Table A = Apps (*Id, Url, Name, Tagline, #Developer_Id, Icon, Rating, Reviews_count, Description, Description_Raw, Free_Trial_Days)
    Table B = Apps (*Id, Benefit_Name, Benefit_Description)
    Table C = Apps (*Id, Price)

    Table A + B + C = Apps (*Id, Url, Name, Tagline, #Developer_Id, Icon, Rating, Reviews_count, Description, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, Price)
    
    Table D = Apps_Price_plans (*#App_Id, *#Price_Plans_Id)
    Table E = Apps_Pricing_Plans_Features (*App_Id, *Pricing_Plan_Id, Feature)
    
    Table D + E = Apps_Price_plans (*#App_Id, *#Price_Plans_Id, Feature)

    Developers (*Id, Name, Link)
    Categories (*Id, Name)
    Apps_Categories (*#App_Id, *#Category_Id)
    Price_plans (*Id, Name)
    Reviews (*Id, #App_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date)

  2. With Contained Key = With the same Primary Key

  3. Third Normal Form = With the same Primary Key

  4. Final Result:

    Apps (*Id, Url, Name, Tagline, #Developer_Id, Icon, Rating, Reviews_count, Description, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, Price)
    Reviews (*Id, #App_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date)
    Developers (*Id, Name, Link)
    Price_plans (*Id, Name)
    Categories (*Id, Name)
    Apps_Categories (*#App_Id, *#Category_Id)
    Apps_Price_plans (*#App_Id, *#Price_Plans_Id, Feature)

### Final Integration (Union of All Datasets):

  1. With the same Primary Key:

    (Apple)   Table A = Apps (*Id, Name, Size, Version, Description, #Genre_Id, #Age_Id, Rating, Rating_Curr_Version, N_of_Rating, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program)
    (Shopify) Table B = Apps (*Id, Url, Name, Tagline, #Developer_Id, Icon, Rating, Reviews_count, Description, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, Price)
    (Google)  Table C = Apps (*Id, Name, #Category_Id, #Price_Type_Id, #Age_Rating_Id, Rating, N_of_Reviews, Price, Size, N_of_Downloads, Latest_Update_at_Store, Curr_Version_Available, Android_Version_Required)
    
    Equals Attributes:
    
      Reviews_Count = N_of_Rating = N_of_Reviews
      Curr_Version_Available = Version
      Age_Rating_Id = Age_Id
      
    Attributes Manipulations:
    
      At C table the key attribute is the app name but it is possible to create an Id related to each name and make this Id as a Primary Key.
      However, it's necessary to verify if there is an intersection between the apps name of C table and the same in other tables.
      In this case, it's possible to reuse an existing key.
      
    Table A + B + C = Apps (*Id, #Category_Id, #Genre_Id, #Age_Rating_Id, #Developer_Id, #Price_Type_Id, Name, Size, Version, Description, Rating, Rating_Curr_Version, N_of_Reviews, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program, Url, Tagline, Icon, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, Price, N_of_Downloads, Latest_Update_at_Store, Android_Version_Required)
    
    
    (Google)  Table F = Reviews (*Id, #App_Name, #Sentiment_Type_Id, Translated_Review, Sentiment_Polarity, Sentiment_Subjectivity)
    (Apple)   Table G = Reviews (*Review_Id, Review)
    (Shopify) Table H = Reviews (*Id, #App_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date)
    
    Equals Attributes:
    
      Id = Review_Id
      Review = Content = Translated_Review
      
    Table F + G + H = Reviews (*Id, #App_Id, #App_name, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date, #Sentiment_Type_Id, Sentiment_Polarity, Sentiment_Subjectivity)
    
    
    (Google) Table D = Genres (*Id, Name)
    (Apple)  Table E = Genres (*Id, Genre)
    
    Equals Attributes:
    
      Genre = Name
      
    Table D + E = Genres (*Id, Genre)
    
    
    (Apple)  Table I = Age_Ratings (*Id, Age_Rating)
    (Google) Table J = Age_Rating (*Id, Age)
    
    Equals Attributes:
    
      Age_Rating = Age
      
    Table I + J = Age_Ratings (*Id, Age_Rating)
    
    
    (Google)  Table N = Price_Type (*Id, Type)
    (Shopify) Table O = Price_plans (*Id, Name)
    
    Equals Attributes:
    
      Type = Name
      
    Table N + O = Price_plans (*Id, Name)
    
    
    (Shopify) Table L = Categories (*Id, Name)
    (Google)  Table M = Category (*Id, Name)
      
    Table L + M = Categories (*Id, Name))
    
    
    Table K = Apps_Genres (*#App_Name, *#Genre_Id)
    
    Attributes Manipulations:
    
      Uses the app Id, not its name.
      
    Table K = Apps_Genres (*#App_Id, *#Genre_Id)
    
    AppReviews (*#App_Id, *#Review_Id)
    Developers (*Id, Name, Link)
    Sentiment_Type (*Id, Type)
    Currencies (*Id, Currency)
    Prices (*#App_Id, *#Currency_Id, Price)
    Apps_Price_plans (*#App_Id, *#Price_Plans_Id, Feature)
    Apps_Categories (*#App_Id, *#Category_Id)

  1.5. Intermediate Result:
    
    Removed Attributes from Apps for duplicity:
    
      #Category_Id
      #Genre_Id
      #Price_Plan_Id
      Price
    
    Removed Attributes from Reviews for duplicity:

      #App_Id
      #App_Name
    
    Included Attributes in Prices due to removal of Price from Apps:

      #Price_Plan_Id


    Apps (*Id, #Age_Rating_Id, #Developer_Id, Name, Size, Version, Description, Rating, Rating_Curr_Version, N_of_Reviews, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program, Url, Tagline, Icon, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, N_of_Downloads, Latest_Update_at_Store, Android_Version_Required)
    Reviews (*Id, #Sentiment_Type_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date, Sentiment_Polarity, Sentiment_Subjectivity)
    Age_Ratings (*Id, Age_Rating)
    Developers (*Id, Name, Link)
    Sentiment_Type (*Id, Type)
    Currencies (*Id, Currency)
    Price_plans (*Id, Name)
    Categories (*Id, Name)
    Genres (*Id, Genre)
    Apps_Genres (*#App_Id, *#Genre_Id)
    Apps_Reviews (*#App_Id, *#Review_Id)
    Apps_Categories (*#App_Id, *#Category_Id)
    Apps_Price_plans (*#App_Id, *#Price_Plan_Id, Feature)
    Prices (*#App_Id, *#Price_Plan_Id, *#Currency_Id, Price)

  2. With Contained Key
  
    Table A = Apps_Price_plans (*#App_Id, *#Price_Plan_Id, Feature)
    Table B = Prices (*#App_Id, *#Price_Plan_Id, *#Currency_Id, Price)
    
    Table A + B = Apps_Price_Plans_Currencys (*#App_Id, *#Price_Plan_Id, *#Currency_Id, Feature, Price)

    Apps (*Id, #Age_Rating_Id, #Developer_Id, Name, Size, Version, Description, Rating, Rating_Curr_Version, N_of_Reviews, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program, Url, Tagline, Icon, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, N_of_Downloads, Latest_Update_at_Store, Android_Version_Required)
    Reviews (*Id, #Sentiment_Type_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date, Sentiment_Polarity, Sentiment_Subjectivity)
    Age_Ratings (*Id, Age_Rating)
    Developers (*Id, Name, Link)
    Sentiment_Type (*Id, Type)
    Currencies (*Id, Currency)
    Price_plans (*Id, Name)
    Categories (*Id, Name)
    Genres (*Id, Genre)
    Apps_Genres (*#App_Id, *#Genre_Id)
    Apps_Reviews (*#App_Id, *#Review_Id)
    Apps_Categories (*#App_Id, *#Category_Id)

  3. Third Normal Form = With Contained Key

  4. Final Result:

    Apps (*Id, #Age_Rating_Id, #Developer_Id, Name, Size, Version, Description, Rating, Rating_Curr_Version, N_of_Reviews, N_of_Rating_Curr_Version, N_of_Supported_Devices, N_of_ipad_URLs, N_of_Available_Languages, Belongs_To_Volume_Purchase_Program, Url, Tagline, Icon, Description_Raw, Free_Trial_Days, Benefit_Name, Benefit_Description, N_of_Downloads, Latest_Update_at_Store, Android_Version_Required)
    Reviews (*Id, #Sentiment_Type_Id, Author, Content, Rating, Helpful_Count, Post_Date, Developer_Reply, Developer_Reply_Post_Date, Sentiment_Polarity, Sentiment_Subjectivity)
    Age_Ratings (*Id, Age_Rating)
    Developers (*Id, Name, Link)
    Sentiment_Type (*Id, Type)
    Currencies (*Id, Currency)
    Price_plans (*Id, Name)
    Categories (*Id, Name)
    Genres (*Id, Genre)
    Apps_Genres (*#App_Id, *#Genre_Id)
    Apps_Reviews (*#App_Id, *#Review_Id)
    Apps_Categories (*#App_Id, *#Category_Id)
    Apps_Price_Plans_Currencys (*#App_Id, *#Price_Plan_Id, *#Currency_Id, Feature, Price)
