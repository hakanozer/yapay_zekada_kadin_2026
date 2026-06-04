import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

"""
siparisler_cleaned.csv örneği:
siparis_id,musteri_adi,sehir,fiyat,adet,tarih,kategori,toplam_harcama
10002,Ayşe Kaya,Ankara,2222.45,7,01-01-2024 03:00:00,Elektronik,15557.15
10003,Mehmet Demir,İzmi̇r,4300.06,6,03-06-2024 04:28:30,Giyim,25800.36
10004,Fatma Şahin,Bursa,3501.97,8,01-01-2024 09:00:00,Giyim,28015.76
10005,Ahmet Yılmaz,İstanbul,516.18,2,01-01-2024 12:00:00,Ev,1032.36
10006,Ayşe Kaya,İstanbul,4879.33,9,01-01-2024 15:00:00,Giyim,43913.97
10008,Fatma Şahin,İzmi̇r,3941.02,5,01-01-2024 21:00:00,Ev,19705.1
10011,Mehmet Demir,İstanbul,1885.45,3,01-02-2024 06:00:00,Giyim,5656.35
10012,Fatma Şahin,Ankara,4637.49,8,01-02-2024 09:00:00,Giyim,37099.92
10014,Ayşe Kaya,Bursa,4122.67,3,01-02-2024 15:00:00,Giyim,12368.01
"""

class ML:
    
    def __init__(self):
        print("ML class initialized")

    def load_csv(self) -> pd.DataFrame:
        file_path = "data/processed/siparisler_cleaned.csv";
        df = pd.read_csv(file_path)
        return df
    
    # scikit-learn kullanarak basit bir model eğitme örneği
    def train_model(self, df: pd.DataFrame):
        
        # Özellikler ve hedef değişkeni belirleme
        X = df[['fiyat', 'adet']]
        y = df['toplam_harcama']

        # Veriyi eğitim ve test setlerine ayırma
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Modeli oluşturma ve eğitme
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Modelin performansını değerlendirme
        score = model.score(X_test, y_test)
        print(f"Model R^2 Score: {score}")
     
        
    # makine öğrenmesi önümüzdeki 30 gün içinde en çok harcama yapacak 5 müşteriyi tahmin etme
    def predict_top_spenders_next_30_days(self, df):

        # Tarihi datetime'a çevir
        df["tarih"] = pd.to_datetime(
            df["tarih"],
            format="%d-%m-%Y %H:%M:%S"
        )

        # Veri setindeki son tarih
        reference_date = df["tarih"].max()

        # Müşteri bazında özellik çıkarımı
        customer_features = df.groupby("musteri_adi").agg(
            toplam_siparis=("siparis_id", "count"),
            toplam_harcama=("toplam_harcama", "sum"),
            ortalama_harcama=("toplam_harcama", "mean"),
            son_siparis=("tarih", "max")
        ).reset_index()

        # Son siparişten geçen gün
        customer_features["gun_farki"] = (
            reference_date - customer_features["son_siparis"]
        ).dt.days

        # Eğitim verisi
        X = customer_features[
            [
                "toplam_siparis",
                "toplam_harcama",
                "ortalama_harcama",
                "gun_farki"
            ]
        ]

        # Basit örnek:
        # Gelecek 30 gün harcaması yerine
        # geçmiş toplam harcamayı hedef alıyoruz.
        y = customer_features["toplam_harcama"]

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        model.fit(X, y)

        # Tahmin
        customer_features["gelecek_30_gun_tahmin"] = model.predict(X)

        # En yüksek 5 müşteri
        top5 = customer_features.sort_values(
            by="gelecek_30_gun_tahmin",
            ascending=False
        ).head(5)

        print("\nÖnümüzdeki 30 gün için en yüksek harcama tahmini:")
        print(
            top5[
                [
                    "musteri_adi",
                    "gelecek_30_gun_tahmin"
                ]
            ]
        )
        # top5 datasını gelecekte_en_cok_harcama_yapan_5_musteri.png dosyasına görselleştirme olarak kaydet
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=top5,
            x="musteri_adi",
            y="gelecek_30_gun_tahmin",
            palette="viridis"
        )
        plt.title("Gelecek 30 Gün İçin En Yüksek Harcama Tahmini")
        plt.xlabel("Müşteri Adı")
        plt.ylabel("Harcama Tahmini")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("data/processed/30_gun_icinde_en_cok_harcama_yapan_5_musteri.png")
        return top5
    
    # makine öğrenmesi ile önümüzdeki 30 gün içinde hiç harcama yapmayacak müşterileri tahmin etme
    def predict_no_spenders_next_30_days(self, df):
        
        no_spenders = self.train_model(df)
        # no_spenders datasını gelecekte_harcama_yapmayacak_musteriler.png dosyasına görselleştirme olarak kaydet
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=no_spenders,
            x="musteri_adi",
            y="prob_not_buy",
            palette="magma"
        )
        plt.title("Gelecek 30 Gün İçin Harcama Yapmayacak Müşteriler")
        plt.xlabel("Müşteri Adı")
        plt.ylabel("Harcama Yapmama Olasılığı")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("data/processed/gelecekte_harcama_yapmayacak_musteriler.png")
        return no_spenders
    
    def train_model(self, df):
        df["tarih"] = pd.to_datetime(df["tarih"], format="%d-%m-%Y %H:%M:%S")
        reference_date = df["tarih"].max()

        features = df.groupby("musteri_adi").agg(
            frequency=("siparis_id", "count"),
            monetary=("toplam_harcama", "sum"),
            avg_order=("toplam_harcama", "mean"),
            last_purchase=("tarih", "max")
        ).reset_index()

        features["recency"] = (reference_date - features["last_purchase"]).dt.days

        # LABEL: 30 gün içinde aktif mi?
        features["label"] = (features["recency"] <= 30).astype(int)

        X = features[["frequency", "monetary", "avg_order", "recency"]]
        y = features["label"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)

        features["prob_not_buy"] = 1 - model.predict_proba(X)[:, 1]

        # EN RİSKLİ 5 MÜŞTERİ
        worst5 = features.sort_values("prob_not_buy", ascending=False).head(5)
        print(worst5[["musteri_adi", "prob_not_buy"]])

        return worst5

""""  
if __name__ == "__main__":
    ml = ML()
    df = ml.load_csv()
    ml.train_model(df)
    ml.predict_top_spenders_next_30_days(df)
    ml.predict_no_spenders_next_30_days(df)
"""