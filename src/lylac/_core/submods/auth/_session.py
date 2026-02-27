from datetime import datetime

class _Session_Interface():

    def generate_user_session(
        self,
        user_id: int,
    ) -> tuple[str, datetime]:
        ...

    def is_active_user(
        self,
        session_uid: str,
    ) -> bool:
        ...
