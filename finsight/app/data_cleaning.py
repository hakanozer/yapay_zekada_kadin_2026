# data/raw/siparisler.csv dosyasındaki verileri temizleme işlemleri için gerekli fonksiyonları içeren modül
# imprt pandas as pd
import pandas as pd
import numpy as np

# siparisler.csv dosyası yükleniyor
def load_data(file_path) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# gelen DataFrame üzerindeki tüm hataları yakalayıp listeler halinde döndüren fonksiyon
def check_data_quality(data: pd.DataFrame) -> dict:
    errors = {}
    if data is None:
        errors['data'] = "Data is None"
        return errors

    # eksik değerleri kontrol et
    missing_values = data.isnull().sum()
    if missing_values.any():
        errors['missing_values'] = missing_values[missing_values > 0].to_dict()

    # veri tiplerini kontrol et
    expected_types = {
        'siparis_id': np.integer,
        'musteri_id': np.integer,
        'urun_id': np.integer,
        'adet': np.integer,
        'fiyat': np.float64,
        'tarih': np.datetime64
    }
    for column, expected_type in expected_types.items():
        if column in data.columns:
            if not np.issubdtype(data[column].dtype, expected_type):
                errors.setdefault('type_mismatch', {})[column] = str(data[column].dtype)

    return errors      
    
# main fonksiyon
if __name__ == "__main__":
    file_path = "data/raw/siparisler.csv"
    data = load_data(file_path)
    if data is not None:
        errors = check_data_quality(data)
        if errors:
            print("Data quality issues found:")
            for error_type, details in errors.items():
                print(f"{error_type}: {details}")
        else:
            print("No data quality issues found.")
    else:
        print("Failed to load data.")  