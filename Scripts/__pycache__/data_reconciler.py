
import pandas as pd
import numpy as np
import logging
from sklearn.impute import SimpleImputer

# تنظیم لاگ‌گیری
logging.basicConfig(
    filename='data_reconciliation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataReconciler:
    """کلاسی برای تصحیح داده‌های گمشده و صاف کردن داده‌های پرنویز."""
    
    def __init__(self, id_column='id', timestamp_column='timestamp'):
        self.id_column = id_column
        self.timestamp_column = timestamp_column
        self.logger = logging.getLogger(__name__)

    def impute_missing_values(self, df):
        """پر کردن داده‌های گمشده با استفاده از Linear Interpolation."""
        df = df.copy()
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col not in [self.id_column, self.timestamp_column]:
                missing_before = df[col].isna().sum()
                if missing_before > 0:
                    # استفاده از Linear Interpolation
                    df[col] = df[col].interpolate(method='linear', limit_direction='both')
                    missing_after = df[col].isna().sum()
                    for idx, val in df[col].items():
                        if pd.isna(df.loc[idx, col]) and not pd.isna(val):
                            self.logger.info(
                                f"Value at timestamp {df.loc[idx, self.timestamp_column]} "
                                f"in column {col} imputed from NaN to {val:.4f}"
                            )
                    if missing_after > 0:
                        # اگر هنوز NaN باقی مونده، با میانگین پر کن
                        imputer = SimpleImputer(strategy='mean')
                        df[col] = imputer.fit_transform(df[[col]])
                        for idx, val in df[col].items():
                            if pd.isna(df.loc[idx, col]) and not pd.isna(val):
                                self.logger.info(
                                    f"Value at timestamp {df.loc[idx, self.timestamp_column]} "
                                    f"in column {col} imputed from NaN to {val:.4f} (mean)"
                                )
        return df

    def smooth_data(self, df, span=3):
        """صاف کردن داده‌ها با Exponential Moving Average."""
        df = df.copy()
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col not in [self.id_column, self.timestamp_column]:
                original_values = df[col].copy()
                df[col] = df[col].ewm(span=span, adjust=False).mean()
                for idx, (orig, smoothed) in enumerate(zip(original_values, df[col])):
                    if not pd.isna(orig) and abs(orig - smoothed) > 1e-6:
                        self.logger.info(
                            f"Value at timestamp {df.loc[idx, self.timestamp_column]} "
                            f"in column {col} smoothed from {orig:.4f} to {smoothed:.4f}"
                        )
        return df

    def reconcile(self, df):
        """اجرای فرآیند تصحیح داده‌ها (پر کردن گمشده‌ها و صاف کردن)."""
        if self.id_column not in df.columns:
            raise ValueError(f"Column {self.id_column} not found in DataFrame")
        if self.timestamp_column not in df.columns:
            raise ValueError(f"Column {self.timestamp_column} not found in DataFrame")

        # پر کردن داده‌های گمشده
        df = self.impute_missing_values(df)
        # صاف کردن داده‌ها
        df = self.smooth_data(df)
        return df

# تست‌های واحد
import unittest

class TestDataReconciler(unittest.TestCase):
    def setUp(self):
        # دیتاست نمونه برای تست
        self.df = pd.DataFrame({
            'id': [1001, 1002, 1003, 1004, 1005],
            'timestamp': pd.to_datetime(['2023-01-01 00:00', '2023-01-01 00:01',
                                        '2023-01-01 00:02', '2023-01-01 00:03',
                                        '2023-01-01 00:04']),
            'sensor1': [10.0, np.nan, 12.0, 15.0, np.nan],
            'sensor2': [20.0, 21.0, 22.0, np.nan, 24.0]
        })
        self.reconciler = DataReconciler(id_column='id', timestamp_column='timestamp')

    def test_impute_missing_values(self):
        df_imputed = self.reconciler.impute_missing_values(self.df)
        self.assertFalse(df_imputed['sensor1'].isna().any(), "sensor1 should have no NaN after imputation")
        self.assertFalse(df_imputed['sensor2'].isna().any(), "sensor2 should have no NaN after imputation")
        self.assertAlmostEqual(df_imputed.loc[1, 'sensor1'], 11.0, places=2,
                              msg="sensor1 at index 1 should be interpolated to 11.0")

    def test_smooth_data(self):
        df_imputed = self.reconciler.impute_missing_values(self.df)
        df_smoothed = self.reconciler.smooth_data(df_imputed, span=3)
        self.assertFalse(df_smoothed['sensor1'].isna().any(), "sensor1 should have no NaN after smoothing")
        # بررسی صاف شدن داده‌ها (مقدار تقریبی)
        expected_sensor1 = df_imputed['sensor1'].ewm(span=3, adjust=False).mean()
        for idx in range(len(df_smoothed)):
            self.assertAlmostEqual(df_smoothed.loc[idx, 'sensor1'], expected_sensor1[idx], places=4,
                                  msg=f"sensor1 at index {idx} not smoothed correctly")

    def test_reconcile(self):
        df_reconciled = self.reconciler.reconcile(self.df)
        self.assertFalse(df_reconciled.isna().any().any(), "No NaN values should remain after reconciliation")
        self.assertTrue((df_reconciled['id'] == self.df['id']).all(), "ID column should remain unchanged")
        self.assertTrue((df_reconciled['timestamp'] == self.df['timestamp']).all(),
                        "Timestamp column should remain unchanged")

if __name__ == '__main__':
    unittest.main()
