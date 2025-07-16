import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import os
import warnings

warnings.filterwarnings('ignore')

def load_and_inspect_data(file_path):
    print(f"🔍 Loading and inspecting data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Data shape: {df.shape}")
    print("Missing values per column:\n", df.isnull().sum())
    return df

def handle_missing_values(df):
    print("🔧 Handling missing values...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    imputer = SimpleImputer(strategy='median')
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print("Missing values after imputation:\n", df.isnull().sum())
    return df

def normalize_features(df):
    print("📏 Normalizing numerical features...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def split_data(df, test_size=0.2, random_state=42):
    print("📊 Splitting data into train and test sets...")
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    print(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
    return train_df, test_df

def save_csv(df, file_path):
    print(f"💾 Saving data to {file_path} ...")
    df.to_csv(file_path, index=False)
    print("Save completed.")

def main():
    input_file = r"C:\Users\morte\OneDrive\Desktop\newone.csv"
    output_train_file = r"C:\Users\morte\OneDrive\Desktop\newone_processed_train.csv"
    output_test_file = r"C:\Users\morte\OneDrive\Desktop\newone_processed_test.csv"

    df = load_and_inspect_data(input_file)
    df = handle_missing_values(df)
    df = normalize_features(df)
    train_df, test_df = split_data(df)
    save_csv(train_df, output_train_file)
    save_csv(test_df, output_test_file)
    print("✅ Data preprocessing pipeline completed successfully.")

if __name__ == "__main__":
    main()
