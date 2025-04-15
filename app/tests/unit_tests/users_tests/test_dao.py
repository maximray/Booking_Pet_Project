import pytest

from app.users.DAO import UsersDAO


@pytest.mark.parametrize("id,email,exists", [
    (1, "user@example.com", True),
    (2, "test@test.com", True),
    (3, "....", False)
])
async def test_find_user_by_id(id, email, exists):
    user = await UsersDAO.find_by_id(id)

    if exists:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user
    