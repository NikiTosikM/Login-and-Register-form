from datetime import datetime
from datetime import timezone, timedelta


token_time = [
    {
        "id": 10,
        "email": "4r332@mail.ru",
    },
    {
        "id": 10,
        "email": "4r332@mail.ru",
        "exp": 10
    },
    {
        "id": 10,
        "email": "4r332@mail.ru",
        "exp": "str"
    }
]

exp_token = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
token_dates = [
    {
        "id": 0,
        "email": "ivan@mail.ru",
        "exp": exp_token
    },
    {
        "id": 1,
        "email": "iva@mail.ru",
        "exp": exp_token
    },
    {
        "id": "ivan@mail.ru",
        "email": "ivan@mail.ru",
        "exp": exp_token
    },
        {
        "id": 1,
        "email": 10,
        "exp": exp_token
    }
]