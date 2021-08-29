import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def convert_to_sqft(str):
    tokens = str.split(' - ')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(tokens[0])
    except Exception:
        return np.NAN

def convert_to_num(num):
    tokens = str(num).split(' ')
    return float(tokens[0])

def train_model(X, Y):
    regression = LinearRegression()
    regression.fit(X, Y)
    return regression

def get_training_data():
    dataframe = pd.read_csv("./Bengaluru_House_Data.csv")
    df = dataframe.drop(columns=["area_type", "balcony", "society", "availability"], axis='columns')
    df['total_sqft'] = df['total_sqft'].apply(convert_to_sqft)
    df['size'] = df['size'].apply(convert_to_num)
    locations = pd.get_dummies(df["location"])
    df_merge = pd.concat([df.drop(columns=["location"]), locations], axis='columns')
    df_merge = df_merge.drop(columns=["Unnamed: 9"], axis='columns')
    df_merge = df_merge.dropna()
    X = df_merge.drop(['price'], axis='columns')
    Y = df_merge['price']
    return X, Y

def predict_price(regression, X, location, bhk, total_sqft, bath):
    location_index = np.where(X.columns == location)[0][0]
    x = np.zeros(len(X.columns))
    x[0] = bhk
    x[1] = total_sqft
    x[2] = bath
    if location_index >= 0:
        x[location_index] = 1
    return regression.predict([x])[0]

def main():
    X, Y = get_training_data()
    regression = train_model(X, Y)

    price = predict_price(regression, X, "Koramangala", 2, 1000, 1)
    print(price)

main()
