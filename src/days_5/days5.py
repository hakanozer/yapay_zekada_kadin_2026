import pandas as pd

"""
siparisler_raw.csv örnek içeriği:
siparis_id,musteri_adi,sehir,fiyat,adet,tarih,kategori
10001,ahmet yılmaz,istanbul,3881.08,8,2024-01-01 00:00:00,?
10002,AYŞE KAYA,Ankara,2222.45,7,2024-01-01 03:00:00,Merkaz
10003,Mehmet  Demir,İZMİR,4300.06,6,2024 01 06:00:00,Gym
10004, Fatma Şahin,bursa,3501.97,8,2024-01-01 09:00:00,Giyim
10005,ahmet yılmaz,Istanbul,516.18,2,2024-01-01 12:00:00,Ev
10006,AYŞE KAYA,istanbul,4879.33,9,2024-01-01 15:00:00,Giyim
10007,Mehmet  Demir,Ankara,3817.64,8,2024-01-01 18:00:00,N/A
10008, Fatma Şahin,İZMİR,3941.02,5,2024-01-01 21:00:00,Ev
10009,ahmet yılmaz,bursa,684.16,7,2024-01-02 00:00:00,N/A
"""
class DataCleans:
    
    def __init__(self):
        print("DataCleans class initialized")
        
    # csv dosyasını pandas ile yüklüyoruz
    def load_csv(self) -> pd.DataFrame:
        file_path = "data/raw/siparisler_raw.csv";
        return pd.read_csv(file_path)
    
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
        
        # yeni bir csv dosyasına temizlenmiş veriyi kaydediyoruz
        df.to_csv("data/processed/siparisler_cleaned.csv", index=False)
        self.control(df)
        
        
if __name__ == "__main__":
    obj = DataCleans()
    df = obj.load_csv()
    obj.clean_data(df)
    