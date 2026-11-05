import uuid

USER_PASSWORD = "Pizza-2026"


def new_name():
    return "lab-" + uuid.uuid4().hex[:12]


# A second user with a name that is already taken gets 400.
def test_duplicate_username_is_refused(api):
    user = {"username": new_name(), "password": USER_PASSWORD}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in with a wrong password gets 401.
def test_wrong_password_is_refused(api):
    user = {"username": new_name(), "password": USER_PASSWORD}
    assert api.post("/api/users", json=user).status_code == 201
    bad = {"username": user["username"], "password": "Wrong-password"}
    res = api.post("/api/users/token/login", json=bad)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# A user with an empty name gets 400.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": USER_PASSWORD})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
