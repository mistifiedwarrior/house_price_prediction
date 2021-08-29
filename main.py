import numpy as np
import pandas as pd

def convert_to_sqft(str):
    tokens = str.split(' - ')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(tokens[0])
    except Exception:
        return np.NAN

def main():
    dataframe = pd.read_csv("./Bengaluru_House_Data.csv")
    df = dataframe.drop(columns=["society", "availability"])
    df['total_sqft'] = df['total_sqft'].apply(convert_to_sqft)
    df = df.dropna()

main()
