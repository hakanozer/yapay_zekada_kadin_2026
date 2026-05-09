# numpy import
import numpy as np

class arrNumPy:
    
    def call(self):
        arr = [1, 2, 3, 4, 5]
        for i in arr:
            print(i)

    def numpytest(self):
        listArr = list(range(1,1000000))
        arr = np.array(listArr)
        print(arr)
        
        # np.empty() - > Bellekte boş bir array oluşturur.
        arr_empty = np.empty((3, 3))
        # 0, 0 -> 3
        arr_empty[0][0] = 3
        print(arr_empty)
        
        # toplam eleman sayısı
        print(arr.size)
        
        # içindekiler değerlerin toplamı
        print(arr.sum())
        
        # ortalama
        print(arr.mean())
        
        # en büyük değer
        print(arr.max())
        
        # en küçük değer
        print(arr.min())
        
        # Standart sapma hesaplar.
        print(arr.std())
        
        
        
objNumPy = arrNumPy()
objNumPy.call() 
objNumPy.numpytest()