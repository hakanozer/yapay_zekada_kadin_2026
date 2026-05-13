import pandas as pd
import numpy as np
import time

class objPandas:
        
    def testPandas(self):
        fiyatlar = pd.Series([150.0, 250.0, 80.0, 320.0, 95.0],
                     index=["Laptop Çantası", "Klavye", "Mouse Pad", "Kulaklık", "USB Hub"],
                     name="Fiyat (TL)")
        print(fiyatlar)
        print("Laptop Çantası fiyatı:", fiyatlar["Laptop Çantası"])
        print("Klavye fiyatı:", fiyatlar["Klavye"])
        print("Mouse Pad fiyatı:", fiyatlar["Mouse Pad"])
        print("Kulaklık fiyatı:", fiyatlar["Kulaklık"])
        print("USB Hub fiyatı:", fiyatlar["USB Hub"])
        
        print(f"\nOrtalama: {fiyatlar.mean():.2f} TL")
        print(f"Maksimum: {fiyatlar.idxmax()} — {fiyatlar.max():.2f} TL")
        
        # Koşullu erişim
        pahali = fiyatlar[fiyatlar > 200]
        print(f"\n200 TL üzeri:\n{pahali}")
        
        # ayraç
        print("====="*10)
        # DataFrame oluşturma
        siparisler = pd.DataFrame({
            "siparis_id":    [10001, 10002, 10003, 10004, 10005],
            "musteri_id":    [201, 202, 201, 203, 202],
            "urun":          ["Laptop", "Mouse", "Klavye", "Monitor", "Mouse"],
            "kategori":      ["Bilgisayar", "Aksesuar", "Aksesuar", "Bilgisayar", "Aksesuar"],
            "fiyat":         [14999.0, 249.0, 449.0, 5499.0, 249.0],
            "adet":          [1, 2, 1, 1, 3],
            "tarih":         ["2024-01-05", "2024-01-07", "2024-01-07", "2024-01-10", "2024-01-12"],
            "durum":         ["Teslim", "Teslim", "Kargoda", "İptal", "Teslim"]
        })
        
        print(f"Sütunlar: {list(siparisler.columns)}")
        print(f"\nVeri tipleri:\n{siparisler.dtypes}")
        print("====="*10)
        # Tarih sütununu datetime formatına çevirme
        siparisler["tarih"] = pd.to_datetime(siparisler["tarih"])
        print("\nSiparişler DataFrame:\n", siparisler)
        print(f"\nŞekil: {siparisler.shape}")
        
        print(f"Sütunlar: {list(siparisler.columns)}")
        print(f"\nVeri tipleri:\n{siparisler.dtypes}")
        # durum türünü enumerate etme
        siparisler["durum"] = pd.Categorical(siparisler["durum"], categories=["Teslim", "Kargoda", "İptal"], ordered=True)
        print("\nSiparişler DataFrame (durum_kod eklendi):\n", siparisler)
        
obj = objPandas()
obj.testPandas()        
