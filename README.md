# The Price Evaluator App
## Description 
An app hosted on a streamlit website that, given sufficient retailer data, is able to take a product and price given to it by a user and determine whether or not that is a good price to buy at. If not, the app will give a list of similair products at different retailers with better times and prices to buy.
## Reason to Use
There’s always a lot of ‘head knowledge’ of the best times to buy a certain item (ie always Black Friday) or from where to buy it (according to my dad Best Buy is always the best) but there’s a lack of actual hard evidence for this. We wanted to get rid of the prophesizing and create a model to predict whether you’re getting a good deal on something, or whether you should wait a couple more weeks for a sale.
## How to Use
<insert image of the selection table>
The application itself is incredibly simple to use. A user simply needs to begin typing the product they are interested in purchasing into the search box and select it from the dropdown menu. After that, enter the price you found the item at into the adjacent 'price' box and select whether or not you would like a new or used item. A text field will then appear either telling you to 'Buy' in green letters for a good deal, or in red letters tell you to think before you buy as there may be better options. To give you an idea of these options, the table below the search fields will automatically generate with the same product from different retailers and the price those retailers are selling it for. This way you can know you are getting your new iPhone at a competitive price, and not simply what Apple.com is telling you they believe it should be!
  <insert generated table>
Finally the website also includes several tables that are generated below the interactive table and in the 'data visualization' tab. Below the interactive table, these graphs are designed to show you who the biggest retailers are for your product as well as the products price over time. This is to allow you to pick both the most reputable retailers with highest supply and to tailor your shopping decisions for when the item is cheapest. The 'data visualization' section has several graphics generated within Tableau that are static, but again feature the biggest brands, retailers, and average price per retailer. This is again to help inform users the most reputable and cheapest purchase options as well as the representation of certain brands within the dataset.
    
For the dataset, it is currently populated with over 12k entries from an Electronics Product dataset found on Kaggle (more details below). You are free to use the code provided here and substitute your own dataset, but it will need to be cleaned and columns matched to our naming schema or the code edited to reflect your desires.

## Communication Methods
- We will meet every Tuesday/Thursday starting at 6:00 to review changes and to go over large problems.
- Team members will update each other daily on Slack
- If assistance is needed, impropmtu meetings will be scheduled using Slack. If not all members can be present in these meetings that is acceptable.
- All team members have each others email and phone number for contact purposes as well in case of issues
- Individual member updates will be stored in their corresponding Git branch (named for each member). Review by two memebers is needed to push an update to main.

## Data - Extract, Transform & Load
Extract: 
- We obtained [Electronic Products and Pricing Data](https://www.kaggle.com/datasets/datafiniti/electronic-products-prices?resource=download) from [kaggle.com](kaggle.com) which includes minimum selling prices (`prices_amountmin`) observed from various online merchants (`prices_merchant`) as well as the dates that those prices were observed (`prices_dateseen`), and whether the prices observed were "sale" prices (`prices_issale`) for each individual product id (`id`). 

In order to clean the data, we had to perform several steps
- Transform the data:
    1. Replace all periods in titles with underscores to follow best SQL practices
    2. Updating all date columns to be in the correct datetime format
    3. Deciding which date columns to use; it was determined that the most recent datetime in the "date seen" column was the most relevant data given what our website's overall goal is. To extract these dates, we split this comma-separated column into individual columns and dropped all but the most recent column. 
    4. Using only USD for our pricing data; all other currencies were dropped
    5. Updating the prices_condition column to read as just one of two values, and cleaned the data so that all values were either New or Used. We assumed that all blank cells were New.
    6. Recombine the prices_merchant column so that we have five categories: walmart, bestbuy, amazon, bhpvideo, and "other". This column initially was a mess, and included mispellings, odd naming conventions, and a host of other issues, which resulted in over 1,500 unique names. We used regex strings to sort the data into the five categories mentioned, with no dramatic loss of data. Data that contained less than 300 data points was lumped together into an "other" category. 

    Load:
    - We decided to use Amazon AWS linked through PGAdmin for our database. PGAdmin allows us to run administrative actions on the database, while AWS hosts the database live. For our schema, we had PGAdmin assign a unique number to each row of data to act as our primay key, since there were no native unique values in the data set. In order to ensure that everyone always had an updated version of hte database (data cleaning was an ongoing process!), we connected the database to our Jupyter notebook files directly by creating an engine using sqalqchemy; this way, whenever a change was made we could all pull the same database into our systems as needed. The password to the database was entered in a separate line of code for security. 



## Machine Learning
### Feature Selection & Target:
The following Features were selected for our Machine Learning model:
1. `id` - The identifier for each unique product.
2. `prices_amountmin` - The lowest price observed for a product on the date specified.
3. `prices_condition` - The 'condition' of a product (i.e. 'New' or 'Used').
4. `prices_merchant` - The merchant selling the product (i.e. 'Walmart.com', 'Bestbuy.com', etc).

Our Target variable is the `prices_issale` field, which indicates whether each data point represents a 'discounted' or 'on-sale' price point.

Note: We initially included the `prices_dateseen` (the date on which the `prices_amountmin` was observed) as a feature in our machine learning model (also experimenting with only keeping the `quarter` or `month` as the feature). However, we eventually realized that this created some over-fitting as our dataset is broken out to thousands of products, while each unique product `id` is only observed, on average, approximately 10-15 times. Once we removed the date features from our model, our accuracy increased by ~5%.

### Data Preprocessing:
We used the `sklearn` library's `LabelEncoder` and `StandardScaler` to preprocess our selected feature and target variables. Additionally, because of the class imbalance observed in our pricing data (discounted prices were far less common than standard prices), we utilized `imblearn.over_sampling.RandomOverSampling` to create an equal distribution in our training data set. We also used the `joblib` library to save our encoders and scalers for future use in our Price Evaluator App.

### Model Selection:
Using our preprocessed dataset, we used a `for` loop to test a number of machine learning models from the `sklearn` library:

!['ML_Models'](Resources/ml_models_tested.jpg)

Based on these results, we found that the `RandomForestClassifier` provided the highest model accuracy score (`model.score()`). We then used the `joblib` library again to save the trained model for future use in our Price Evaluator App.

## Price Evaluator App
We used Streamlit.io to create our web application, which prompts users for a product name, price, merchant, and condition ('New' or 'Used'). Our app then feeds the user's input into our saved Machine Learning Model, and predicts whether the sale conditions are discounted.
We have 3 pages in our web application:
- Graph page which represents our Tableau Dashboard.
- Prediction page which allows the user to select the product to be predicted, and contains our input and selec boxes.
- Predicted page which appears after submitting the submit button and contains our interactive graphs and predicted results.<br>

our web application is connected with our AWS database using sqlalchemy create_engine feature, using option_menu feature in streamlit we created multiple pages, lottie is used for animated graphic.<br>
st.spinner is used to add a spinner, after submitting the submit button the spinner is going to load for a second and then our predicted page will show up, if predicted price is lower then user input price, a green success messages (Seems like a Good Deal!) and balloons will pop up on our screen, which is created using st.success and st.balloons.

We have two interactive charts:
1) Pie chart which shows Retailer Distribution.
2) Altair chart which shows Price History.
> <img width="1440" alt="interactive charts" src="https://user-images.githubusercontent.com/97934695/177893946-2a6fd88c-48c1-4993-9c44-f9bad3709794.png">


## Visualizations Dashboard
Using Tableau, we also built static visualizations capturing the full dataset. 
- A stacked bar chart shows the distribution of sales over time; we can see that BestBuy has the most frequent sales in May, but almost none in January or Febrary.  
- Bubble chart shows the distribution of brands in our data set, using a count of the unique values int he ID column. Sony and Apple are pretty big players!
- Box and Whiskers: We used this to look at how skewed the pricing data is. In order to evaluate this we chose the top 10 items with the most pricing data associated with them. We can see that Walmart and Bestbuy's average price is quite a bit lower than the other merchants'. BestBuy and Walmart also have the largest spread of pricing within their own data sets, while Amazon remains fairly tight around its average cost line. For this plot, outliers were thrown out; we are only interested in the skew and shape of normally distributed data. This has a pronounced affect on the look and usability of our graphs, demonstrated below with outliers (right) and without (left)

![Here it is without outliers:](Resources/boxplot.jpg)
![Here it is with outliers:](Resources/boxplot_outliers.jpg)



## Technology
•	Data Cleaning: Pandas, Numpy, and re
•	Database: PostgreSQL RDS hosted on AWS
•	Machine Learning: Sklearn library
•	Code Editors: Jupyter Notebook / Google Colab / VScode
•	Dashboard: Streamlit, Lottie, Matplotlib, Tableau, HTML
