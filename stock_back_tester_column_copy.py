
# import packages
import streamlit as st
import pandas as pd
from pandas_datareader import data as pdr
import altair as alt
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# App title displayed
st.title("Stock Investment Back Tester")

col1, col2, = st.columns(2)

with col1:
   # Collect input from the user of the company stock they are interested in
    st.write("What company are you thinking to invest in?")
    tick = st.text_input('Type the stocks ticker symbol in the box below')
    tick1 = tick.upper()
    # Get the current date on their computer. (They could change this input date if they desire)
    cur_date = st.date_input("Todays date is")
    # Subtract 10 years from the date for the back check
    back_date = cur_date - relativedelta(years = 10)
    # Use if statement to display the rest after user inputs are collected
    if tick == "":
        pass
    else:
        # Pull in the stock data from yahoo finance
        stock = pdr.get_data_yahoo(f"{tick1}", start= f"{back_date}", end= f"{cur_date}").reset_index()
        stock1 = stock[["Date", "Close"]] # Selects the columns
        # Grab the first and last rows of the dataframe
        both = stock1.iloc[[0, -1]]
        first = both.iloc[[0]]
        last = both.iloc[[1]]
        # Extract the first date for this stock and convert it to a date object from datetime object
        first_date = first.iat[0,0]
        first_date1 = first_date.date()
        # Extract the closing price of the first and last dates
        first1 = first.iat[0,1]
        last1 = last.iat[0,1]
        # Calculate the percent change and average yearly percentage change over the time frame I am showing of the stock
        change = round(last1/first1, 2)
        print(f"{tick1} had a {round((change - 1)*100,2)} % change")
        percent_change = round((change - 1)*100,2)
        avg_yearly_percent_change = percent_change / 10
        if percent_change > 0:
            trend = "growth"
        else:
            trend = "decrease"
        # I am getting the last date and converting it from datetime object to just the date
        last_date = last.iat[0,0]
        last_date1 = last_date.date()
        # Pull out the year alone from both the first and last dates
        first_year = first_date1.year
        last_year = last_date1.year
        # Calculate the difference of the years to state to the user and give them more clear context of the metric below
        year_span = last_year - first_year
        if year_span > 1:
            st.write(f"Over the last {year_span} years there has been an")
        else:
            st.write(f"Over the last {year_span} year there has been an")
        # Show the average yearly percentage growth or decrease in a streamlit metric
        st.metric(label=f"average yearly {trend} of", value= "", delta=f"{avg_yearly_percent_change}%")   
        # Present the current stock price so they know how much a stock would be if they were to purchase it
        last2 = round(last1, 2)
        st.write(f"The current stock price is ${last2}")
if tick == "":
    pass
else:
    with col2:
        # Write to the user the correct starting to current date of the stock
        st.write(f"{tick1} Stock Closing Price From {first_date1} to {cur_date}")
        # Graph of the stocks closing price over time
        chart = alt.Chart(data = stock1).mark_line().encode(x = alt.X("Date"), y = alt.Y("Close"))
        st.altair_chart(chart)


    
    

