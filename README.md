# phitchanan-api-lab

API tests for QuickPizza (https://quickpizza.grafana.com) with pytest and requests.

## Install and run

```
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
pytest -v --html=report.html --self-contained-html
```

A full run sends about 140 requests and takes about a minute. Expected result: `32 passed, 1 xfailed`.
Every test creates its own user, so tests are independent of each other.

## Input domain model for POST /api/ratings

| Characteristic | Blocks | Values in the tests | Test that covers the block |
|---|---|---|---|
| C1 Value of stars | below 1 | 0 | `test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of stars | whole number (base) | 3 | `test_base_choice_is_saved` |
| | decimal | 3.5 | `test_stars_decimal` |
| | text | "3" | `test_stars_text` |
| | missing | no field | `test_stars_missing` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| | does not exist | 999999999 | `test_pizza_does_not_exist` |
| C4 Token | the user's own (base) | from `auth` | `test_base_choice_is_saved` |
| | none | no header | `test_token_missing` |
| | wrong length | token short | `test_token_wrong_length` |

Base choice coverage: 1 + 2 + 3 + 1 + 2 = 9 tests (all combinations: 3 x 4 x 2 x 3 = 72).
