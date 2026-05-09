class Customer:
    # müşteri kayıt, güncelleme, silme, arama, listeleme gibi işlemler yapacak bir sınıf

    # müşteri kayıt fonksiyonu
    def add_customer(self, customer_name: str, email: str) -> str:
        return f"Customer '{customer_name}' added with email {email}."

    # güncelleme fonksiyonu
    def update_customer(self, customer_name: str, new_email: str) -> str:
        return f"Customer '{customer_name}' updated with new email {new_email}."

    # silme fonksiyonu
    def delete_customer(self, customer_name: str) -> str:
        return f"Customer '{customer_name}' deleted."

    # arama fonksiyonu
    def search_customer(self, customer_name: str) -> str:
        return f"Customer '{customer_name}' found."

    # listeleme fonksiyonu
    def list_customers(self) -> str:
        return "Listing all customers."
