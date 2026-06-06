# Yapay Zeka Web Görselleştirme

Bu görevde, yapay zeka tarafından oluşturulan görselleri web üzerinde görselleştirmek için HTML ve CSS kullanarak bir web sayfası oluşturacağız. Aşağıda, bu görevi tamamlamak için adım adım bir rehber bulunmaktadır.

# End Point: 
Get -> http://localhost:8000/ml/30gunHarcamaYapacaklar
Gelen Data:
{
    "success": true,
    "images": [
        "30_gun_icinde_en_cok_harcama_yapan_5_musteri.png"
    ],
    "data": [
        {
            "musteri_adi": "Ahmet Yılmaz",
            "toplam_siparis": 68,
            "toplam_harcama": 901513.3,
            "ortalama_harcama": 13257.548529411766,
            "son_siparis": "2024-12-02T12:00:00",
            "gun_farki": 0,
            "gelecek_30_gun_tahmin": 881654.0672999986
        },
        {
            "musteri_adi": "Fatma Şahin",
            "toplam_siparis": 68,
            "toplam_harcama": 841184.55,
            "ortalama_harcama": 12370.361029411766,
            "son_siparis": "2024-12-01T21:00:00",
            "gun_farki": 0,
            "gelecek_30_gun_tahmin": 838275.3901999987
        }
    ]
}

## Adım 1: HTML Dosyası Oluşturma
Endpoint'ten gelen verileri görselleştirmek için bir HTML dosyası oluştur.
Html tema için bootstrap kullanabilirsin. CDN yapısı aşağıdaki gibi ola
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>

## Adım 2: Verileri Görselleştirme
Endpoint'ten gelen verileri kullanarak bir tablo oluştur. Tablo, müşteri adı, toplam sipariş, toplam harcama, ortalama harcama, son sipariş tarihi, gün farkı ve gelecek 30 gün tahmini harcama gibi bilgileri içermelidir.

## Adım 3: responseive Tasarım
Tablonun farklı cihazlarda düzgün görüntülenebilmesi için responsive tasarım kullan. Bootstrap'ın grid sistemini kullanarak tabloyu mobil, tablet ve masaüstü cihazlarda uygun şekilde görüntüleyebilirsin.

## adım 4: Kayıt Yeri
Oluşturduğun HTML dosyasını projenin data/processed/ klasörüne kaydet. Dosya adı olarak "30gunHarcamaYapacaklar.html" kullanabilirsin.

## Adım 5: Grafikleri Gösterme
Gelen Data içinde "images" alanında belirtilen görselleri HTML dosyasında uygun şekilde göster. Görsellerin doğru şekilde yüklenebilmesi için data/processed/ klasöründe bulunmaları gerekmektedir.

## Adım 6: Grafiklere tıklanıldığında büyük boyutta gösterme
Görsellerin küçük boyutlu versiyonlarını HTML dosyasında gösterirken, kullanıcıların bu görsellere tıklayarak büyük boyutlu versiyonlarını görebilmeleri için bir modal (açılır pencere) oluştur. Bootstrap'ın modal bileşenini kullanarak bu işlevselliği ekleyebilirsin.