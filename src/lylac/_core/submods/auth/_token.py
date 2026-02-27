from datetime import datetime

class _Token_Interface():

    def create_session_token(
        self,
        session_uuid: str,
        expiration_date: datetime,
    ) -> str:
        ...
