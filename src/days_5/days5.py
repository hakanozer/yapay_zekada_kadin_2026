from difflib import SequenceMatcher

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataCleans:
    
    def __init__(self):
        print("DataCleans class initialized")
        
    # csv dosyasını pandas ile yüklüyoruz
    def load_csv(self) -> pd.DataFrame:
        file_path = "data/raw/siparisler_raw.csv";
        return pd.read_csv(file_path)
    
    # gönderilen kategori adına en çok benzeyen kategori adını döndüren fonksiyon
    def benzer_kategori(self, kategori, kategoriler):
        skorlar = [
            SequenceMatcher(None, kategori.lower(), k.lower()).ratio()
            for k in kategoriler
        ]
        en_benzeyen = kategoriler[skorlar.index(max(skorlar))]
        return en_benzeyen
    
    # dataframe'in içindeki sütunların veri tiplerini ve eksik değerleri kontrol ediyoruz
    def control(self, df: pd.DataFrame):
        print("Dataframe info:")
        print(df.info())
        print("\nMissing values in each column:")
        print(df.isnull().sum())
    
    # veriyi temizleme işlemi
    def clean_data(self, df: pd.DataFrame):
        self.control(df)
        
        # siparis_id sütununda tekrar eden değerler varsa sadece ilkini bırakıp diğerlerini siliyoruz
        # siparis_id sütununda tekrar eden değerler toplamının kaç tane olduğunu yazdırıyoruz
        duplicate_count = df.duplicated(subset=['siparis_id']).sum()
        print(f"Duplicate siparis_id count: {duplicate_count}")
        df = df.drop_duplicates(subset=['siparis_id'])
        
        # musteri_adi boş olanları "İsimsiz" ile dolduruyoruz
        df['musteri_adi'] = df['musteri_adi'].fillna("İsimsiz")
        # musteri_adi sütunundaki değerileri trim yaparak başındaki ve sonundaki boşlukları kaldırıyoruz
        df['musteri_adi'] = df['musteri_adi'].str.strip()
        # musteri_adi sütunundaki değerleri title case yaparak her kelimenin ilk harfini büyük yapıyoruz
        df['musteri_adi'] = df['musteri_adi'].str.title()
        # musteri_adi sütunundaki isim ve soyisim arasında birden fazla boşluk varsa tek boşluk yapıyoruz
        df['musteri_adi'] = df['musteri_adi'].str.replace(r'\s+', ' ', regex=True)

        # sehir sütunundaki değerleri title case yaparak her kelimenin ilk harfini büyük yapıyoruz
        df['sehir'] = df['sehir'].str.title()
        # sehir sütunundaki değerlerin baş harfinde "I", "İ" yapıyoruz
        df['sehir'] = df['sehir'].str.replace(r'^I', 'İ', regex=True)
        # sehir sütunundaki değerlere trim yaparak başındaki ve sonundaki boşlukları kaldırıyoruz
        df['sehir'] = df['sehir'].str.strip()
        
        # fiyat ve kategori sütunlarında "N/A" değerleri veya boş  veya ? olan satırları siliyoruz
        df = df[~((df['fiyat'].isnull()) | (df['fiyat'] == "N/A") | (df['fiyat'] == "?") | (df['kategori'].isnull()) | (df['kategori'] == "N/A") | (df['kategori'] == "?"))]
        # fiyat sütununu ondalıklı değerlerin . dan sonra 2 hane yoksa sona 0 ekle ve 2 hane olarak yazdırıyoruz
        df['fiyat'] = df['fiyat'].apply(lambda x: f"{float(x):.2f}")
        
        # adet sütunundaki değerleri pozitif integer yapıyoruz
        df['adet'] = df['adet'].apply(lambda x: abs(int(x)))
        
        # tarih sütunundaki tarih formatını "DD-MM-YYYY HH:MM:SS" yapıyoruz
        df['tarih'] = pd.to_datetime(df['tarih'], errors='coerce').dt.strftime('%d-%m-%Y %H:%M:%S')
        # tarih sütunundaki hatalı tarihleri tarihlerin ortalama tarihi ile dolduruyoruz
        mean_date = pd.to_datetime(df['tarih'], errors='coerce').mean()
        df['tarih'] = pd.to_datetime(df['tarih'], errors='coerce').fillna(mean_date).dt.strftime('%d-%m-%Y %H:%M:%S')
        
        # kategori dizisi
        kategoriler = ["Elektronik", "Giyim", "Ev"]
        # kategori sütunundaki değerleri en çok benzeyen kategori ile değiştiriyoruz
        df['kategori'] = df['kategori'].apply(lambda x: self.benzer_kategori(x, kategoriler))
        
        self.ortalama_fiyat_kategori(df)
        self.en_cok_satis_yapilan_sehirler(df)
        self.en_cok_harcama_yapilan_musteriler(df)
        
        # yeni bir excel dosyasına temizlenmiş veriyi kaydediyoruz
        df.to_excel("data/processed/siparisler_cleaned.xlsx", index=False)
        
        # yeni bir csv dosyasına temizlenmiş veriyi kaydediyoruz
        df.to_csv("data/processed/siparisler_cleaned.csv", index=False)
        # self.control(df)
        
    # Veri analizi için gerekli fonksiyonları yazıyoruz 
    # Kategorilerin ortalama fiyatını hesaplayan fonksiyon ve bunları matplotlib ile görselleştiren ve png dosyası olarak kaydeden fonksiyon yazıyoruz
    def ortalama_fiyat_kategori(self, df: pd.DataFrame):
        # Stil (modern görünüm)
        sns.set_theme(style="whitegrid", palette="muted")

        # Veri hazırlama
        df['fiyat'] = df['fiyat'].astype(float)
        ortalama_fiyat = df.groupby('kategori')['fiyat'].mean().sort_values(ascending=False)

        print("Kategorilerin ortalama fiyatları: ", ortalama_fiyat)

        # Figure boyutu
        plt.figure(figsize=(10, 6))

        # Renk paleti (modern gradient hissi)
        colors = sns.color_palette("viridis", len(ortalama_fiyat))

        # Bar plot
        ax = ortalama_fiyat.plot(
            kind='bar',
            color=colors,
            edgecolor='black',
            linewidth=0.6
        )

        # Başlık ve etiketler
        plt.title("Kategorilerin Ortalama Fiyatları", fontsize=14, fontweight='bold')
        plt.xlabel("Kategori", fontsize=12)
        plt.ylabel("Ortalama Fiyat", fontsize=12)

        # Grid iyileştirme
        plt.grid(axis='y', linestyle='--', alpha=0.4)

        # X ekseni yazılarını döndürme
        plt.xticks(rotation=45, ha='right')

        # Değerleri bar üstüne yazma
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", fontsize=10)

        # Layout düzeni
        plt.tight_layout()

        # PNG kaydetme
        plt.savefig(
            "data/processed/ortalama_fiyat_kategori.png",
            dpi=200,
            bbox_inches='tight'
        )
        # plt.show()
    
    # En çok satış yapılan şehirleri ve bu şehirlerdeki ortalama fiyatları hesaplayan fonksiyon ve bunları matplotlib ile görselleştiren ve png dosyası olarak kaydeden fonksiyon yazıyoruz
    def en_cok_satis_yapilan_sehirler(self, df: pd.DataFrame):
        # Stil (modern görünüm)
        sns.set_theme(style="whitegrid", palette="muted")

        # Veri hazırlama
        df['fiyat'] = df['fiyat'].astype(float)
        satis_sayisi = df['sehir'].value_counts().head(10)
        ortalama_fiyat = df.groupby('sehir')['fiyat'].mean().round(2).loc[satis_sayisi.index]

        print("En çok satış yapılan şehirler: ", satis_sayisi)
        print("Bu şehirlerdeki ortalama fiyatlar: ", ortalama_fiyat) 
        
        # Figure boyutu
        plt.figure(figsize=(12, 8))
        # Renk paleti (modern gradient hissi)
        colors = sns.color_palette("viridis", len(satis_sayisi))
        # Bar plot
        ax = satis_sayisi.plot(
            kind='bar',
            color=colors,
            edgecolor='black',
            linewidth=0.6
        )
        # Başlık ve etiketler
        plt.title("En Çok Satış Yapılan Şehirler", fontsize=14, fontweight='bold')
        plt.xlabel("Şehir", fontsize=12)
        plt.ylabel("Satış Sayısı", fontsize=12)
        # Grid iyileştirme
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        # X ekseni yazılarını döndürme
        plt.xticks(rotation=45, ha='right')
        # Değerleri bar üstüne yazma
        for container in ax.containers:
            ax.bar_label(container, fmt="%d", fontsize=10)
        # Layout düzeni
        plt.tight_layout()
        # PNG kaydetme
        plt.savefig(
            "data/processed/en_cok_satis_yapilan_sehirler.png",
            dpi=200,
            bbox_inches='tight'
        )
        # plt.show()
    
    
    # En çok 10 müşteri ve bu müşterilerin toplam harcamalarını hesaplayan fonksiyon ve bunları matplotlib ile görselleştiren ve png dosyası olarak kaydeden fonksiyon yazıyoruz
    def en_cok_harcama_yapilan_musteriler(self, df: pd.DataFrame):
        # Stil (modern görünüm)
        sns.set_theme(style="whitegrid", palette="muted")

        # Veri hazırlama
        df['fiyat'] = df['fiyat'].astype(float)
        df['toplam_harcama'] = (df['fiyat'] * df['adet']).round(2)
        harcama_siralamasi = df.groupby('musteri_adi')['toplam_harcama'].sum().sort_values(ascending=False).head(10)

        print("En çok harcama yapılan müşteriler: ", harcama_siralamasi)
        # Figure boyutu
        plt.figure(figsize=(12, 8))
        # Renk paleti (modern gradient hissi)
        colors = sns.color_palette("viridis", len(harcama_siralamasi))
        # Bar plot
        ax = harcama_siralamasi.plot(
            kind='bar',
            color=colors,
            edgecolor='black',
            linewidth=0.6
        )
        # Başlık ve etiketler
        plt.title("En Çok Harcama Yapılan Müşteriler", fontsize=14, fontweight='bold')
        plt.xlabel("Müşteri Adı", fontsize=12)
        plt.ylabel("Toplam Harcama", fontsize=12)
        # Grid iyileştirme
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        # X ekseni yazılarını döndürme
        plt.xticks(rotation=45, ha='right')
        # Değerleri bar üstüne yazma
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", fontsize=10)
        # Layout düzeni
        plt.tight_layout()
        # PNG kaydetme
        plt.savefig(
            "data/processed/en_cok_harcama_yapilan_musteriler.png",
            dpi=200,
            bbox_inches='tight'
        )
        # plt.show()    
        
        
if __name__ == "__main__":
    obj = DataCleans()
    df = obj.load_csv()
    obj.clean_data(df)
    