import pytest


# Boundary values of stars: 1 and 5 are saved, 0 and 6 are refused and
# leave the rating unchanged.
@pytest.mark.parametrize("stars, expected", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, expected):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected
    kept = stars if expected == 200 else rating["stars"]
    res = api.get(path, headers=auth)
    assert res.json()["stars"] == kept
