# Dependencies
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import time
from ML_Evaluator import evaluate_price

# Function to generate predictions page
def show_prediction_page(df):
    st.title("Price Evaluator")

    # Dropdown menu options
    product_names = list(df['name'].unique())
    merchants = list(df['prices_merchant'].unique())
    product_conditions = list(df['prices_condition'].unique())
    
    # Generate input form
    with st.form('user_form'):
        # Splits the page width for four input columns
        box1, box2, box3, box4 = st.columns((3,2,2,2))

        # Create Input Boxes & retain user input as variables
        with box1:
            item_name = st.selectbox("Enter Product Name", product_names)
        with box2:
            item_price = st.number_input("Enter your price")
        with box3:
            retailer = st.selectbox("Select a Retailer", merchants)
        with box4:
            condition = st.selectbox("Product Condition", product_conditions)

        # Submit button for Input Form
        submitted = st.form_submit_button('Submit')
    
    return item_name, item_price, retailer, condition, submitted

def show_predicted_page(df, item_name, item_price, retailer, condition, submitted):
    # Runs Machine Learning Model each time input form is 'submitted' by user
    if submitted:     
        # Adds spinner after clicking the button
        with st.spinner("Searching for your product"):
            time.sleep(1)

        # Filter df for item_name in order to find corresponding product_id
        product_id = df['id'].loc[df['name'] == item_name].iloc[0]
        
        # Use ML_Evaluator to make a prediction based on user input
        eval = evaluate_price(product_id, item_price, condition, retailer)
        if eval == True:
            st.success("Seems like a Good Deal!")
            st.balloons()
        if eval == False:
            st.warning("May Not be Discounted.")

        # Print output df showing all product details matching selected product name
        output_df = df.loc[df["name"] == item_name]
        display_df = pd.DataFrame({'Product Name': output_df['name'], 
                                    'Price': output_df['prices_amountmin'], 
                                    'Merchant': output_df['prices_merchant'], 
                                    'Condition': output_df['prices_condition'],
                                    'On Sale': output_df['prices_issale']})
        st.write(display_df.style.format({"Price": "{:.2f}"}))
    
        # Generate columns of equal width for interactive visualizations
        g1, g2 = st.columns((3.5,6.5))

        # Graph 1 - Retailer Distribution
        with g1:
            st.write("### Retailer Distribution")
            output_df = df.loc[df["name"] == item_name]
            labels = list(output_df['prices_merchant'].unique())
            data = list(output_df.groupby(['prices_merchant']).count()['id'])
            fig, ax = plt.subplots(figsize=(4,4))
            wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.0f%%', shadow=True, startangle=180, 
                    textprops={'color':'lightgrey', 'fontsize': 14, 'weight': 'bold'})
            ax.set_position([0,3,1,1])
            fig.patch.set_facecolor('none')
            st.pyplot(fig)

        # Graph 2 - Price History
        with g2:
            st.write("### Price History")
            output_df = df.loc[df["name"] == item_name]
            chart_data = pd.DataFrame({'Date': output_df['prices_dateseen'], 
                                        'Price': output_df['prices_amountmin'],
                                        'Condition': output_df['prices_condition']})
            st.altair_chart(alt.Chart(chart_data).mark_line().encode(x='Date',
                                                            y='Price',
                                                            color='Condition'),
                            use_container_width=True)


