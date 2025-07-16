import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import warnings
import os

warnings.filterwarnings('ignore')

def load_and_inspect_data(file_path):
    print("🔍 Loading and inspecting data...")
    df = pd.read_csv(file_path)
    print("\n📊 Data Overview:")
    print(f"Shape: {df.shape}")
    print("\nColumns:", df.columns.tolist())
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nSample data:\n", df.head())
    return df

def handle_missing_values(df):
    print("\n🔧 Handling missing values...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    imputer = SimpleImputer(strategy='median')
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    print("Missing values after imputation:\n", df.isnull().sum())
    return df

def preprocess_timestamp(df):
    print("\n⏰ Processing Timestamp column...")
    # تلاش برای تبدیل ستون Timestamp به تاریخ
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        # در صورت وجود مقادیر تبدیل نشده، حذف آنها
        df = df.dropna(subset=['Timestamp'])
        df['hour'] = df['Timestamp'].dt.hour
        df['minute'] = df['Timestamp'].dt.minute
        df['second'] = df['Timestamp'].dt.second
        df['day_of_week'] = df['Timestamp'].dt.dayofweek
        df['day_of_year'] = df['Timestamp'].dt.dayofyear
        df.drop('Timestamp', axis=1, inplace=True)
    except Exception as e:
        print("Error processing Timestamp:", e)
    return df

def encode_categorical(df):
    print("\n🔠 Encoding categorical columns...")
    le = LabelEncoder()
    df['Location'] = le.fit_transform(df['Location'])
    location_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print("Location mapping:", location_mapping)
    return df, le

def normalize_features(df):
    print("\n📏 Normalizing numerical features...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_cols = [col for col in numeric_cols if col not in ['Location']]
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df, scaler

def detect_outliers(df, threshold=3):
    print("\n⚠️ Detecting outliers...")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_cols = [col for col in numeric_cols if col not in ['Location']]
    z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
    outliers = (z_scores > threshold).any(axis=1)
    print(f"Found {outliers.sum()} potential outliers (Z-score > {threshold})")
    for col in numeric_cols:
        median = df[col].median()
        std = df[col].std()
        df[col] = np.where(np.abs(df[col] - median) > threshold * std, median, df[col])
    return df

def split_and_save_data(df, output_dir, test_size=0.2, random_state=42):
    print("\n💾 Splitting and saving data as CSV...")
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    os.makedirs(output_dir, exist_ok=True)
    train_path = os.path.join(output_dir, 'processed_train_data.csv')
    test_path = os.path.join(output_dir, 'processed_test_data.csv')
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"Training data saved to {train_path} (Shape: {train_df.shape})")
    print(f"Testing data saved to {test_path} (Shape: {test_df.shape})")
    return train_path, test_path

def main():
    # مسیر فایل خام روی دسکتاپ
    input_file = r'C:\Users\morte\OneDrive\Desktop\sensor_extended_processed.csv'

    # مسیر پوشه خروجی روی دسکتاپ
    output_dir = r'C:\Users\morte\OneDrive\Desktop\processed_data'

    df = load_and_inspect_data(input_file)
    df = handle_missing_values(df)
    df = preprocess_timestamp(df)
    df, label_encoder = encode_categorical(df)
    df = detect_outliers(df)
    df, scaler = normalize_features(df)
    train_path, test_path = split_and_save_data(df, output_dir)

    print("\n✅ Data preprocessing completed successfully!")
    print(f"Processed data saved to:\n  {train_path}\n  {test_path}")

if __name__ == "__main__":
    main()
