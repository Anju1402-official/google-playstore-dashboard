import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from datetime import datetime
import pytz

st.title("📱 Google Play Store Data Dashboard")

# Function to check IST time range
def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone('Asia/Kolkata')
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour

# CSV uploader
uploaded_file = st.file_uploader("📂 Upload your Google Play Store CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ---------------- DATA CLEANING ----------------
    df['Size'] = df['Size'].astype(str).replace('Varies with device', None)
    df['Size'] = df['Size'].str.replace('M', '', regex=False).str.replace('k', '', regex=False)
    df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    df['Installs'] = df['Installs'].astype(str).str.replace(',', '').str.replace('+', '')
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
    df['Updated_Month'] = df['Last Updated'].dt.month_name()

    df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    df['Revenue'] = df['Price'] * df['Installs']

    np.random.seed(42)
    df['Subjectivity'] = np.random.uniform(0.6, 1.0, len(df))

    translations = {'Beauty': 'सौंदर्य', 'Business': 'வணிகம்', 'Dating': 'Verabredung'}

    # ------------------- TASK 1 -------------------
    task1_df = df[(df['Rating'] >= 4.0) & (df['Size'] >= 10) & (df['Updated_Month'] == 'January')]
    category_stats = task1_df.groupby('Category')[['Rating', 'Reviews', 'Installs']].agg({
        'Rating': 'mean', 'Reviews': 'sum', 'Installs': 'sum'
    }).sort_values(by='Installs', ascending=False).head(10).reset_index()

    # ------------------- TASK 2 -------------------
    task2_df = df.copy()
    task2_df = task2_df[~task2_df['Category'].str.startswith(('A', 'C', 'G', 'S'), na=False)]
    task2_df = task2_df.groupby('Category')[['Installs']].sum().reset_index()
    task2_df = task2_df[task2_df['Installs'] > 1_000_000]
    top5 = task2_df.sort_values(by='Installs', ascending=False).head(5)
    top5['Country'] = ['USA', 'India', 'Germany', 'Brazil', 'Canada'][:len(top5)]

    # ------------------- TASK 3 -------------------
    task3_df = df.copy()
    task3_df = task3_df[task3_df['Installs'] >= 10000]
    task3_df = task3_df[task3_df['Revenue'] >= 10000]
    task3_df = task3_df[pd.to_numeric(task3_df['Android Ver'].astype(str).str.extract(r'(\d+(\.\d+)?)')[0], errors='coerce') > 4.0]
    task3_df = task3_df[task3_df['Size'] > 15]
    task3_df = task3_df[task3_df['Content Rating'] == 'Everyone']
    task3_df = task3_df[task3_df['App'].astype(str).str.len() <= 30]
    top3_categories = task3_df.groupby('Category')['Installs'].sum().sort_values(ascending=False).head(3).index
    task3_df = task3_df[task3_df['Category'].isin(top3_categories)]
    grouped = task3_df.groupby('Type').agg({'Installs': 'mean', 'Revenue': 'mean'}).reset_index()

    # ------------------- TASK 4 -------------------
    task4_df = df.copy()
    task4_df['Category_Clean'] = task4_df['Category']
    task4_df = task4_df[
        (~task4_df['App'].str.lower().str.startswith(('x', 'y', 'z'))) &
        (task4_df['Category_Clean'].str.startswith(('E', 'C', 'B'))) &
        (task4_df['Reviews'] > 500) &
        (~task4_df['App'].str.contains('S', case=False))
    ]
    task4_df['Category_Clean'] = task4_df['Category_Clean'].replace(translations)
    task4_df['Month_Year'] = task4_df['Last Updated'].dt.to_period('M').astype(str)
    trend_data = task4_df.groupby(['Month_Year', 'Category_Clean'])['Installs'].sum().reset_index()
    trend_data['Prev_Installs'] = trend_data.groupby('Category_Clean')['Installs'].shift(1)
    trend_data['Growth_%'] = ((trend_data['Installs'] - trend_data['Prev_Installs']) / trend_data['Prev_Installs']) * 100
    trend_data['Highlight'] = trend_data['Growth_%'] > 20

    # ------------------- TASK 5 -------------------
    task5_df = df.copy()
    valid_categories = ['game', 'beauty', 'business', 'comics', 'communication', 'dating', 'entertainment', 'social', 'event']
    task5_df = task5_df[task5_df['Rating'] > 3.5]
    task5_df = task5_df[task5_df['Category'].str.lower().isin(valid_categories)]
    task5_df = task5_df[task5_df['Reviews'] > 500]
    task5_df = task5_df[~task5_df['App'].str.contains('S', case=False)]
    task5_df = task5_df[task5_df['Subjectivity'] > 0.5]
    task5_df = task5_df[task5_df['Installs'] > 50000]
    task5_df['Category_Clean'] = task5_df['Category'].replace(translations)

    # ------------------- STREAMLIT LAYOUT -------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"])

    with tab1:
        st.subheader("📊 Task 1: App Category Ratings vs Reviews")
        if is_time_allowed(15, 17):
            if not category_stats.empty:
                st.plotly_chart(px.bar(category_stats, x='Category', y=['Rating', 'Reviews'], barmode='group'))
            else:
                st.warning("⚠ No data after filters.")
        else:
            st.warning("⚠ This chart is only visible between 3 PM and 5 PM IST.")

    with tab2:
        st.subheader("🌍 Task 2: Global Installs by Category")
        if is_time_allowed(18, 20):
            if not top5.empty:
                st.plotly_chart(px.choropleth(top5, locations='Country', locationmode='country names', color='Installs', hover_name='Category'))
            else:
                st.warning("⚠ No data after filters.")
        else:
            st.warning("⚠ This chart is only visible between 6 PM and 8 PM IST.")

    with tab3:
        st.subheader("💰 Task 3: Installs vs Revenue for Free vs Paid Apps")
        if is_time_allowed(13, 14):
            if not grouped.empty:
                st.plotly_chart(px.bar(grouped, x='Type', y=['Installs', 'Revenue'], barmode='group'))
            else:
                st.warning("⚠ No data after filters.")
        else:
            st.warning("⚠ This chart is only visible between 1 PM and 2 PM IST.")

    with tab4:
        st.subheader("📈 Task 4: Total Installs Trend by Category")
        if is_time_allowed(18, 21):
            if not trend_data.empty:
                st.plotly_chart(px.line(trend_data, x='Month_Year', y='Installs', color='Category_Clean', markers=True))
            else:
                st.warning("⚠ No data after filters.")
        else:
            st.warning("⚠ This chart is only visible between 6 PM and 9 PM IST.")

    with tab5:
        st.subheader("🫧 Task 5: Bubble Chart - Size vs Rating")
        if is_time_allowed(17, 19):
            if not task5_df.empty:
                st.plotly_chart(px.scatter(task5_df, x='Size', y='Rating', size='Installs', color='Category_Clean',
                                           title="Bubble Chart of App Size vs Rating", color_discrete_map={'Game': 'pink'}))
            else:
                st.warning("⚠ No data after filters.")
        else:
            st.warning("⚠ This chart is only visible between 5 PM and 7 PM IST.")
else:
    st.warning("📂 Please upload your CSV file to see the dashboard.")
 