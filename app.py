import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datasets import load_dataset

tab1, tab2, tab3 = st.tabs(["Benchmark", "Data viz", "Data explorer"])

with tab1:
    
    st.title("Professor Layton LLM Benchmark")
    
    st.caption("Only text questions")
    data = {
        "provider": ["Open AI", "Open AI", "Open AI", "Mistral"],
        "models": ["o3", "o4-mini", "GPT-4o", "Medium 3"],
        "release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "accuracy": [0.85, 0.90, 0.88, 0.56],
        "pika": [30000, 34000, 23000, 45000],
        "cost": [0.10, 0.15, 0.08, 0.3],
        "speed": [120, 100, 150, 455]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)
    
    st.caption("Only text questions with hints")
    data = {
        "provider": ["Open AI", "Open AI", "Open AI", "Mistral"],
        "models": ["o3", "o4-mini", "GPT-4o", "Pixtral Large"],
        "release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "0-hint accuracy": [0.85, 0.90, 0.88, 0.56],
        "2-hint accuracy": [0.85, 0.90, 0.88, 0.56],
        "3-hint accuracy": [0.85, 0.90, 0.88, 0.56],
        "4-hint accuracy": [0.85, 0.90, 0.88, 0.56],
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)
    
    st.caption("Text and image questions")
    data = {
        "provider": ["Open AI", "Open AI", "Open AI", "Mistral"],
        "models": ["o3", "o4-mini", "GPT-4o", "Pixtral Large"],
        "release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "accuracy": [0.85, 0.90, 0.88, 0.56],
        "pika": [30000, 34000, 23000, 45000],
        "cost": [0.10, 0.15, 0.08, 0.3],
        "speed": [120, 100, 150, 455]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)
    
    st.caption("Text and image questions with hints")
    data = {
        "provider": ["Open AI", "Open AI", "Open AI", "Mistral"],
        "models": ["o3", "o4-mini", "GPT-4o", "Pixtral Large"],
        "release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "0-hint accuracy": [0.85, 0.90, 0.88, 0.56],
        "2-hint accuracy": [0.85, 0.90, 0.88, 0.56],
        "3-hint accuracy": [0.85, 0.90, 0.88, 0.56],
        "4-hint accuracy": [0.85, 0.90, 0.88, 0.56],
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)


with tab2:

    @st.cache_data
    def load_data():
        dataset = load_dataset("cmenasse/layton",  data_files="layton_eval.csv")
        if isinstance(dataset, dict):
            dataset = list(dataset.values())[0]
        return dataset

    data = load_data()
    df = data.to_pandas()
    st.dataframe(df)

    counts = df['picarats'].value_counts().sort_index().reset_index()
    counts.columns = ['Values', 'Count']

    fig = px.bar(
        counts,
        x='Values',
        y='Count',
        title='Picarats distribution'
    )

    fig.update_xaxes(tickmode='linear', tick0=0, dtick=10)
    st.plotly_chart(fig)

    category_counts = df['category'].value_counts()
    single_occurrences = category_counts[category_counts < 10].index
    df['category_grouped'] = df['category'].apply(lambda x: 'Other' if x in single_occurrences else x)
    grouped_counts = df['category_grouped'].value_counts().reset_index()
    grouped_counts.columns = ['Category', 'Count']

    fig = px.pie(
        grouped_counts,
        values='Count',
        names='Category',
        title='Categories',
        hole=0.4  
    )
    st.plotly_chart(fig)




with tab3:

    st.markdown("This is an example of a third tab.")