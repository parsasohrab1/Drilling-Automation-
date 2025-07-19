import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import os
import warnings

warnings.filterwarnings('ignore')

def load_data(file_path):
    print(f"🔍 Loading data from {file_path} ...")
    df = pd.read_parquet(file_path)
    print(f"✅ Loaded data with shape: {df.shape}")
    return df

def handle_missing_values(df):
    print("\n🔧 Handling missing values...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    num_imputer = SimpleImputer(strategy='median')
    df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print("Missing values after imputation:")
    print(df.isnull().sum())
    return df

def preprocess_timestamp(df):
    if 'Timestamp' in df.columns:
        print("\n⏰ Processing Timestamp column...")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

        # استخراج ویژگی‌های زمانی اگر تبدیل موفقیت‌آمیز بود
        df['hour'] = df['Timestamp'].dt.hour
        df['minute'] = df['Timestamp'].dt.minute
        df['second'] = df['Timestamp'].dt.second
        df['day_of_week'] = df['Timestamp'].dt.dayofweek
        df['day_of_year'] = df['Timestamp'].dt.dayofyear

        df.drop('Timestamp', axis=1, inplace=True)
    else:
        print("\n⏰ No Timestamp column found.")
    return df

def encode_categorical(df):
    print("\n🔠 Encoding categorical columns...")
    le_dict = {}
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
        print(f"Encoded '{col}' with mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    return df, le_dict

def detect_and_fix_outliers(df, threshold=3):
    print("\n⚠️ Detecting and fixing outliers...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
    outliers = (z_scores > threshold).any(axis=1)
    print(f"Found {outliers.sum()} outliers")

    for col in numeric_cols:
        median = df[col].median()
        std = df[col].std()
        df[col] = np.where(np.abs(df[col] - median) > threshold * std, median, df[col])

    return df

def normalize_features(df):
    print("\n📏 Normalizing numerical features...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df, scaler

def split_and_save(df, output_dir, base_filename):
    print("\n💾 Splitting data and saving CSV files...")
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs(output_dir, exist_ok=True)

    train_path = os.path.join(output_dir, f"{base_filename}_train.csv")
    test_path = os.path.join(output_dir, f"{base_filename}_test.csv")

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Training data saved to: {train_path} (shape: {train_df.shape})")
    print(f"Testing data saved to: {test_path} (shape: {test_df.shape})")

def main():
    input_file = r"C:\Users\morte\OneDrive\Desktop\cleaned_train.parquet"
    output_dir = r"C:\Users\morte\OneDrive\Desktop"
    base_filename = "cleaned_train_processed"

    df = load_data(input_file)
    df = handle_missing_values(df)
    df = preprocess_timestamp(df)
    df, le_dict = encode_categorical(df)
    df = detect_and_fix_outliers(df)
    df, scaler = normalize_features(df)
    split_and_save(df, output_dir, base_filename)

    print("\n✅ Preprocessing complete!")

if __name__ == "__main__":
    main()
