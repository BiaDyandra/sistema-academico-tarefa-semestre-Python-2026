from enum import Enum


class Role(Enum):
    ADMIN = "ADMIN"
    PROFESSOR = "PROFESSOR"


class User:
    def __init__(self, username: str, password: str, role: Role):
        if not username or not username.strip():
            raise ValueError("O nome de usuário não pode ser vazio.")
        if not password or not password.strip():
            raise ValueError("A senha não pode ser vazia.")
        if role is None:
            raise ValueError("O papel do usuário não pode ser nulo.")

        self._username = username.strip()
        self._password = password
        self._role = role

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def role(self) -> Role:
        return self._role

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self._username == other._username

    def __hash__(self):
        return hash(self._username)

    def __repr__(self):
        return f"User(username={self._username}, role={self._role})"
