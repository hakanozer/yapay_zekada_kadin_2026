# fonksiyonlar
# fonksiyonlar "def" anahtar kelimesi ile tanımlanır
# fonksiyon adını tanımlanız gerekir


# sum -> fonksiyon adı
# a, b -> parametreler
# return -> fonksiyonun geri döndürdüğü değer
def sum(a: int, b: int) -> int:
    return a + b

# ad ve soyadı birleştiren fonksiyon
def full_name(first_name: str, last_name: str) -> str:
    return first_name + " " + last_name


# paramtere olarak gelen cümlenin kelimesini bulan fonksiyon, bu davranışta a, is gibi kelimeleri dahil etme.
def word_count(sentence: str) -> int:
    words = sentence.split()
    count = 0
    for word in words:
        if len(word) > 2:
            count += 1
    return count


# gönderilen cümle içinde "python" kelimesinin olup olmadığını kontrol eden fonksiyon
def contains_python(sentence: str) -> bool:
    print("this line called")
    return "python" in sentence.lower()



if __name__ == '__main__':
    sm = sum(50, 100)
    print(sm)

    fn = full_name("John", "Doe")
    print(fn)

    sentence = "Selam istanbul güzel bir şehir"
    count = word_count(sentence)
    print(count)

    sentence = "I love Python programming."
    print(contains_python(sentence))