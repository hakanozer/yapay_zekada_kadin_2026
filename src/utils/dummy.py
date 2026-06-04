from src.models.userAddRequest import UserAddRequest


def allUserData() -> list[UserAddRequest]:
    users = [
        UserAddRequest(id=1, name="Hakan", surname="Yıldız", email="hakan@mail.com", password="12345"),
        UserAddRequest(id=2, name="Ayşe", surname="Demir", email="ayse@mail.com", password="67890"),
        UserAddRequest(id=3, name="Mehmet", surname="Kara", email="mehmet@mail.com", password="54321"),
        UserAddRequest(id=4, name="Elif", surname="Yılmaz", email="elif@mail.com", password="98765"),
        UserAddRequest(id=5, name="Ahmet", surname="Çelik", email="ahmet@mail.com", password="11223"),
        UserAddRequest(id=6, name="Fatma", surname="Öztürk", email="fatma@mail.com", password="33445"),
        UserAddRequest(id=7, name="Ali", surname="Kaya", email="ali@mail.com", password="55667")
    ]
    return users