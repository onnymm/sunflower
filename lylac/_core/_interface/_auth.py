from typing import Literal

class Auth_Interface():

    def identify_user(
        self,
        token: str,
    ) -> int:
        ...

    def hash_password(
        self,
        password: str,
    ) -> str:
        ...

    def login(
        self,
        login: str,
        password: str,
    ) -> str | Literal[False]:
        ...

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
        close_sessions: bool = True,
    ) -> None:
        ...

    def reset_password(
        self,
        user_id: int,
    ) -> None:
        ...
