def refused(res):
    return 400 <= res.status_code <= 499


def owner_view(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    return res.json()


# Another user cannot read the rating of its owner.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert refused(res), res.status_code
    assert owner_view(api, auth, rating) == rating


# Another user cannot change the rating of its owner.
def test_other_user_cannot_change(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 1}, headers=other_auth)
    assert refused(res), res.status_code
    assert owner_view(api, auth, rating) == rating


# Another user cannot delete the rating of its owner.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert refused(res), res.status_code
    assert owner_view(api, auth, rating) == rating
