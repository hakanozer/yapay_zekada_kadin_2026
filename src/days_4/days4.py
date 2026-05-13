# numpy import
import time

import numpy as np

class arrNumPy:
    
    
    def numpytest(self):
        listArr = list(range(1,1000000))
        arr = np.array(listArr)
        
        # index eleman erişimi
        print(arr[0])  # ilk eleman
        
        # Karekök
        print(np.sqrt(arr))
        
        # Üs alma
        print("power (^2):", np.power(arr, 2))
        
        # Yuvarlama
        ondalikArr = np.array([1.525, 2.376, 3.745, 1.744, 2.933, 3.188])
        print("round:", np.round(ondalikArr, 2))
        print("floor:", np.floor(ondalikArr))
        print("ceil:", np.ceil(ondalikArr))
        
        # Eksene göre istatistik (axis=0: sütun, axis=1: satır)
        mat = np.array([[1, 2, 3],
                        [4, 5, 6]])
        mat.all()
        print("Sütunlara göre ortalama:", np.mean(mat, axis=0))
        print("Satırlara göre ortalama:", np.mean(mat, axis=1))
        print("Sütunlara göre standart sapma:", np.std(mat, axis=0))
        print("Satırlara göre standart sapma:", np.std(mat, axis=1))
        
        
        # argmax / argmin -> Max/min değerin indeksini döner
        arr2 = np.array([10, 10, 55, 3, 3, 3, 78, 22, 22, 45, 1, 99, 5, 10])
        # start time
        
        start_time = time.time()
        print("argmax:", np.argmax(arr))   # 7
        end_time = time.time()
        print("Execution time (numpy):", end_time - start_time, "seconds")
        print("argmin:", np.argmin(arr))   # 6
        
        # klasik for loop ile argmax
        start_time = time.time()
        max_index = 0
        max_value = arr[0]
        for i in range(1, len(arr)):
            if arr[i] > max_value:
                max_value = arr[i]
                max_index = i
        print("argmax (for loop):", max_index)
        end_time = time.time()
        print("Execution time (for loop):", end_time - start_time, "seconds")
        
        # medyan
        print("medyan:", np.median(arr2))
        
        # varyans
        sayilar = np.array([10, 11, 10, 10])
        print("varyans:", np.var(sayilar))
        
        # korelasyon
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([44, 45, 56, 71, 72])
        print("korelasyon:", np.corrcoef(x, y))
        
        # sıralama
        print("sıralama:", np.sort(arr2))
        # reverse sıralama
        print("reverse sıralama:", np.sort(arr2)[::-1])
        
        # Sıralama indekslerini döndürme
        print("sıralama indeksleri:", np.argsort(arr2))
        
        # Binary search ile sıralama
        sorted_arr = np.sort(arr2)
        target = 22
        index = np.searchsorted(sorted_arr, target)
        print(f"{target} sayısının sıralanmış dizideki konumu:", index)
        
        # unique değerler
        degerler, sayilar = np.unique(arr2, return_counts=True)
        print("unique değerler:", degerler)
        print("unique sayılar:", sayilar)
        
        # arrayler arası kıyaslama
        arrA = np.array([1, 2, 3, 4, 5])
        arrB = np.array([5, 4, 3, 2, 1])
        print("arrA > arrB:", arrA > arrB)
        print("arrA == arrB:", arrA == arrB)
        print("arrA < arrB:", arrA < arrB)
        
        # in1d
        in1d = np.in1d(arr2, arrA)
        print("in1d:", in1d)
        
objNumPy = arrNumPy()
objNumPy.numpytest()