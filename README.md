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
We obtained [Electronic Products and Pricing Data](https://www.kaggle.com/datasets/datafiniti/electronic-products-prices?resource=download) from [kaggle.com](kaggle.com) which includes minimum selling prices (`prices_amountmin`) observed from various online merchants (`prices_merchant`) as well as the dates that those prices were observed (`prices_dateseen`), and whether the prices observed were "sale" prices (`prices_issale`) for each individual product id (`id`). 

In order to clean the data, we ______

Initially, the `pricing_merchant` data contained merchant names with various naming conventions and included over ____ unique names. Using RegEx strings to match different variations of merchant names, we cut the unique names down to ___ and grouped all merchants with fewer than ___ unique data points into an 'Others' category.

Finally, using the `create_engine` function from `sqlalchemy`, we established a connection and saved our clean data to our PostgreSQL RDS (hosted on AWS). 

## Machine Learning
For the machine learning model, we tested a number of Machine Learning Models but found that the RandomForestClassifier resulted in the highest accuracy score. Using the cleaned dataset stored in our RDS, we trained our model to predict whether prices seen online are "discounted / sale" prices or "standard / retail" prices. 

Additionally, we observed that our pricing data had a class imbalance with discounted prices being less common than standard prices (as expected) and therefore we utilized RandomOverSampling in our training population in order to achieve a more balanced training set.

## Price Evaluator App
We used Streamlit.io to create our web application, which prompts users for a product name, price, merchant, and condition ('New' or 'Used'). Our app then feeds the user's input into our saved Machine Learning Model, and predicts whether the sale conditions are discounted.

## Visualizations Dashboard
Using Tableau, we also built static visualizations capturing the full dataset. A stacked bar chart shows____. Bubble chart ____. ____

## Technology usage for our final project
•	Data Cleaning: Pandas, Numpy, and re
•	Database: PostgreSQL RDS hosted on AWS
•	Machine Learning: Sklearn library
•	Code Editors: Jupyter Notebook / Google Colab / VScode
•	Dashboard: Streamlit, Lottie, Matplotlib, Tableau, HTML.


# Next Steps
