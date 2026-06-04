from dataclasses import dataclass

@dataclass
class UserAddRequest:
    id: int
    name: str
    surname: str
    email: str
    password: str
