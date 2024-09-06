from httpx import AsyncClient

import jwt

import pytest

from dates_for_test.auth_dates import token_time, \
    token_dates

from conftest import setting


@pytest.mark.parametrize("dates", token_time)
async def test_token_exp(ac:AsyncClient, dates):
    test_token = jwt.encode(dates, setting.SECRET_JWT, setting.JWT_ALGORITHM)
    ac.cookies.set("token_user", test_token)
    responce = await ac.get(
        "http://127.0.0.1:8000/auth/request"
    )
    assert responce.status_code == 401


@pytest.mark.parametrize("dates", token_dates)
async def test_token_dates(ac:AsyncClient, dates):
    test_token = jwt.encode(dates, setting.SECRET_JWT, setting.JWT_ALGORITHM)
    ac.cookies.set("token_user", test_token)
    responce = await ac.get(
        "http://127.0.0.1:8000/auth/request"
    )
    assert responce.status_code == 400


    

