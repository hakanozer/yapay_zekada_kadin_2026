import pandas as pd
import numpy as np

"""
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

    def load_csv(self):
        file_path = "data/processed/siparisler_cleaned.csv";
        df = pd.read_csv(file_path)
        

if __name__ == "__main__":
    ml = ML()
    ml.load_csv()
