class Product:
    
    # product kayıt, güncelleme, silme, arama, listeleme gibi işlemler yapacak bir sınıf oluşturun.
   
    # product kayıt fonksiyonu
    def add_product(self, product_name: str, price: float) -> str:
        return f"Product '{product_name}' added with price {price}."
    
    # güncelleme fonksiyonu
    def update_product(self, product_name: str, new_price: float) -> str:
        return f"Product '{product_name}' updated with new price {new_price}."
    
    # silme fonksiyonu
    def delete_product(self, product_name: str) -> str:
        return f"Product '{product_name}' deleted."
    
    # arama fonksiyonu
    def search_product(self, product_name: str) -> str:
        return f"Product '{product_name}' found."
    
    # listeleme fonksiyonu
    def list_products(self) -> str:
        return "Listing all products."