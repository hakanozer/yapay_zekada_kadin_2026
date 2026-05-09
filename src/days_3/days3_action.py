from days3 import word_count, sum
from product import Product
from customer import Customer

count_1 = word_count("Hello world, this is a test sentence.")
print(count_1)

count_2 = word_count("Python, a programming is language.")
print(count_2)

sum_result = sum(10, 20)
print(sum_result)

# nesne üretim işlemi
productObj = Product()
# nesne içinde özelliğe (.) operatörü ile erişim sağlanır.
addPro = productObj.add_product("Laptop", 1500.00)
print(addPro)

updatePro = productObj.update_product("Laptop", 1200.00)
print(updatePro)

deletePro = productObj.delete_product("Laptop")
print(deletePro)

searchPro = productObj.search_product("Laptop")
print(searchPro)

listPro = productObj.list_products()
print(listPro)

# müşteri işlemleri için de benzer şekilde Customer sınıfından nesne üretip işlemleri gerçekleştirebilirsiniz.


customerObj = Customer()

addCust = customerObj.add_customer("John Doe", "john.doe@example.com")
print(addCust)

updateCust = customerObj.update_customer("John Doe", "john.new@example.com")
print(updateCust)

deleteCust = customerObj.delete_customer("John Doe")
print(deleteCust)

searchCust = customerObj.search_customer("John Doe")
print(searchCust)

listCust = customerObj.list_customers()
print(listCust)

