import pandas as pd


def load_data():
    df = pd.read_csv('./app/data/ChatbotData.csv')

    questions = df['Q']
    answers = df['A']

    return questions, answers