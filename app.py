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
        "provider": ["Open AI", "Open AI"],
        "models": ["o3-mini", "GPT-4o"],
        #"release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "correct_answer_accuracy": [0.66, 0.30],
        "justified_answer_accuracy": [0.61, 0.25],
        "correct_answer_mean_picarats": [34.54, 31.86],
        "justified_answer_mean_picarats": [33.04, 27.17],
        "cost": ["-", "-"],
        "speed": ["-", "-"]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)


    st.caption("Text and image questions")
    data = {
        "provider": ["Open AI", "Open AI"],
        "models": ["o4-mini", "GPT-4-1"],
        #"release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "correct_answer_accuracy": [0.28, 0.22],
        "justified_answer_accuracy": [0.26, 0.19],        
        "correct_answer_mean_picarats": [33.62, 30.70],
        "justified_answer_mean_picarats": [31.17, 27.05],        
        "cost": ["-", "-"],
        "speed": ["-", "-"]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)
    
    st.caption("Only text questions with hints")
    data = {
        "provider": ["Open AI", "Open AI", "Open AI", "Mistral"],
        "models": ["o3", "o4-mini", "GPT-4o", "Pixtral Large"],
        #"release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "0-hint accuracy": [0, 0, 0, 0],
        "2-hint accuracy": [0, 0, 0, 0],
        "3-hint accuracy": [0, 0, 0, 0],
        "4-hint accuracy": [0, 0, 0, 0],
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)
    
    
    st.caption("Text and image questions with hints")
    data = {
        "provider": ["Open AI", "Open AI", "Open AI", "Mistral"],
        "models": ["o3", "o4-mini", "GPT-4o", "Pixtral Large"],
        #"release": ["2025-04-16", "2025-04-16", "2025-04-16", "2025-04-16"],
        "0-hint accuracy": [0, 0, 0, 0],
        "2-hint accuracy": [0, 0, 0, 0],
        "3-hint accuracy": [0, 0, 0, 0],
        "4-hint accuracy": [0, 0, 0, 0],
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

    df = df[df["requires_game_engine"]==False]


    st.write("For the purpose of this Benchmark, we filter out the riddles that require a game engine to be verified")


    st.write("Number of riddles without game engine need:", len(df))
    st.write("Number of riddles without image need:", len(df[df["is_description_sufficient"]==True]))
    st.write("Number of riddles with image need:", len(df[df["is_description_sufficient"]==False]))


    category_counts = df['category'].value_counts()
    single_occurrences = category_counts[category_counts < 10].index
    df['category_grouped'] = df['category'].apply(lambda x: 'Other' if x in single_occurrences else x)
    grouped_counts = df['category_grouped'].value_counts().reset_index()
    grouped_counts.columns = ['Category', 'Count']

    fig1 = px.pie(
        grouped_counts,
        values='Count',
        names='Category',
        title='Categories',
        hole=0.4  
    )
    st.plotly_chart(fig1, key="camembert")



    counts = df['picarats'].value_counts().sort_index().reset_index()
    counts.columns = ['Values', 'Count']
    fig2 = px.bar(counts, x='Values', y='Count', title='Picarats distribution')
    fig2.update_xaxes(tickmode='linear', tick0=0, dtick=10)
    st.plotly_chart(fig2, key="picarats")


    counts = {
        '1': (df['first_hint'].notna().sum() / len(df)) * 100,
        '2': (df['second_hint'].notna().sum() / len(df)) * 100,
        '3': (df['third_hint'].notna().sum() / len(df)) * 100,
        '4': (df['special_hint'].notna().sum() / len(df)) * 100,
    }
    counts_df = pd.DataFrame(list(counts.items()), columns=['Nb of hints', 'Percentage'])

    fig3 = px.bar(
        counts_df,
        x='Nb of hints',
        y='Percentage',
        title='Riddles with at least n hints',
        text='Percentage'
    )

    # Afficher les valeurs sur les barres
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')

    # Adapter l'échelle Y
    fig3.update_yaxes(range=[0, max(counts.values()) + 1])

    # Afficher dans Streamlit
    st.plotly_chart(fig3, key="hints", use_container_width=True)





with tab3:

    st.markdown("This is an example of a third tab.")