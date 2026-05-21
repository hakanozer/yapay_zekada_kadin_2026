import random

def tahmin_oyunu():
    tutulan = random.randint(1, 10)

    while True:
        tahmin = int(input("1 ile 10 arasında tahmin giriniz: "))

        if tahmin == tutulan:
            print("Bildiniz!")
            break
        else:
            print("Tekrar deneyin")


def en_buyuk_bul():
    sayilar = [8, 21, 4, 17, 35, 9]

    en_buyuk = sayilar[0]

    for sayi in sayilar:
        if sayi > en_buyuk:
            en_buyuk = sayi

    print("En büyük sayı:", en_buyuk)


def tek_cift_ayir():
    tekSayilar = []
    ciftSayilar = []

    for i in range(5):
        sayi = int(input("Sayı giriniz: "))

        if sayi % 2 == 0:
            ciftSayilar.append(sayi)
        else:
            tekSayilar.append(sayi)

    print("Tek sayılar:", tekSayilar)
    print("Çift sayılar:", ciftSayilar)


def sifre_gucu():
    sifre = input("Şifre giriniz: ")

    if len(sifre) < 6:
        print("Zayıf")
    elif len(sifre) <= 10:
        print("Orta")
    else:
        print("Güçlü")


def ismi_tersten_yaz():
    isim = input("İsminizi giriniz: ")

    print("Tersten yazılışı:", isim[::-1])


def liste_filtreleme():
    sayilar = [3, 12, 7, 25, 10, 18, 2]
    yeni_liste = []

    for sayi in sayilar:
        if sayi > 10:
            yeni_liste.append(sayi)

    print("10'dan büyük sayılar:", yeni_liste)


def isimleri_al():
    isimler = []

    while True:
        isim = input("İsim giriniz. Çıkmak için q yazınız: ")

        if isim == "q":
            break
        else:
            isimler.append(isim)

    print("Girilen isimler:", isimler)


def not_ortalamasi():
    toplam = 0

    for i in range(5):
        notu = int(input("Not giriniz: "))
        toplam = toplam + notu

    ortalama = toplam / 5

    print("Ortalama:", ortalama)

    if ortalama >= 50:
        print("Geçti")
    else:
        print("Kaldı")


def ortak_elemanlar():
    liste1 = [2, 4, 6, 8, 10]
    liste2 = [1, 2, 5, 6, 9, 10]

    ortak = []

    for eleman in liste1:
        if eleman in liste2:
            ortak.append(eleman)

    print("Ortak elemanlar:", ortak)


def sayi_listesi_menu():
    liste = []

    while True:
        print("\n1- Sayı Ekle")
        print("2- Listeyi Göster")
        print("3- Çıkış")

        secim = input("Seçiminizi giriniz: ")

        if secim == "1":
            sayi = int(input("Eklenecek sayıyı giriniz: "))
            liste.append(sayi)
            print("Sayı listeye eklendi.")

        elif secim == "2":
            print("Liste:", liste)

        elif secim == "3":
            print("Çıkış yapıldı.")
            break

        else:
            print("Yanlış seçim yaptınız.")


def menu():
    while True:
        print("\n--- PYTHON ÖDEV MENÜSÜ ---")
        print("1- Sayı Tahmin Oyunu")
        print("2- En Büyük Sayıyı Bul")
        print("3- Tek ve Çift Sayıları Ayır")
        print("4- Şifre Güç Kontrolü")
        print("5- İsmi Tersten Yazdır")
        print("6- Listeyi Filtreleme")
        print("7- Sürekli İsim Alma")
        print("8- Ortalama Hesaplama")
        print("9- Ortak Elemanları Bul")
        print("10- Sayı Listesi Menüsü")
        print("0- Programdan Çık")

        secim = input("Bir seçim yapınız: ")

        if secim == "1":
            tahmin_oyunu()
        elif secim == "2":
            en_buyuk_bul()
        elif secim == "3":
            tek_cift_ayir()
        elif secim == "4":
            sifre_gucu()
        elif secim == "5":
            ismi_tersten_yaz()
        elif secim == "6":
            liste_filtreleme()
        elif secim == "7":
            isimleri_al()
        elif secim == "8":
            not_ortalamasi()
        elif secim == "9":
            ortak_elemanlar()
        elif secim == "10":
            sayi_listesi_menu()
        elif secim == "0":
            print("Program kapatıldı.")
            break
        else:
            print("Geçersiz seçim.")


menu()