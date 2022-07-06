# The “When to Buy” App
## Description 
Train a Machine Learning Model to be able to recognize whether a product’s pricing is discounted based on the date, merchant info and product id.
## Reason Selected
There’s always a lot of ‘head knowledge’ of the best times to buy a certain item (ie always Black Friday) or from where to buy it (according to my dad Best Buy is always the best) but there’s a lack of actual hard evidence for this. We wanted to get rid of the prophesizing and create a model to predict whether you’re getting a good deal on something, or whether you should wait a couple more weeks for a sale.
## Questions we Hope to Answer:
- If I buy ‘item X’ today, am I getting a good deal on it?
- What are the pricing trends for item X? Per retailer?
- What retailer should I buy item X from?
- Is one retailer generally better than the others?
- Are the best deals always on holidays?

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
For the machine learning model, we tested a number of Machine Learning Models but found that the RandomForestClassifier resulted in the highest accuracy score. Using the cleaned dataset stored in our RDS, we trained our model to predict whether prices seen online are "discounted / sale" prices or "standard / retail" prices. 

Additionally, we observed that our pricing data had a class imbalance with discounted prices being less common than standard prices (as expected) and therefore we utilized RandomOverSampling in our training population in order to achieve a more balanced training set.

## Price Evaluator App
We used Streamlit.io to create our web application, which prompts users for a product name, price, merchant, and condition ('New' or 'Used'). Our app then feeds the user's input into our saved Machine Learning Model, and predicts whether the sale conditions are discounted.

## Visualizations Dashboard
Using Tableau, we also built static visualizations capturing the full dataset. 
- A stacked bar chart shows the distribution of sales over time; we can see that BestBuy has the most frequent sales in May, but almost none in January or Febrary.  
- Bubble chart shows the distribution of brands in our data set, using a count of the unique values int he ID column. Sony and Apple are pretty big players!
- Box and Whiskers: We used this to look at how skewed the pricing data is. In order to evaluate this we chose the top 10 items with the most pricing data associated with them. We can see that Walmart and Bestbuy's average price is quite a bit lower than the other merchants'. BestBuy and Walmart also have the largest spread of pricing within their own data sets, while Amazon remains fairly tight around its average cost line. For this plot, outliers were thrown out; we are only interested in the skew and shape of normally distributed data. This has a pronounced affect on the look and usability of our graphs, demonstrated below with outliers (right) and without (left)

![Here it is without outliers:](without_outliers.jpg)
![Here it is with outliers:](with_outliers.jpg)



## Technology
•	Data Cleaning: Pandas, Numpy, and re
•	Database: PostgreSQL RDS hosted on AWS
•	Machine Learning: Sklearn library
•	Code Editors: Jupyter Notebook / Google Colab / VScode
•	Dashboard: Streamlit, Lottie, Matplotlib, Tableau, HTML


# Next Steps
