# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Grey Americana
- Step 0.12, results of the three runs without a session (optional): skipped (optional step)
- Step 0.16, blocks of "how many of the three tools are excluded":
  - none excluded (0) - `[]`
  - one excluded (1) - `["Knife"]`, `["Scissors"]`
  - two excluded (2) - `["Knife", "Scissors"]`
  - all three excluded (3) - `["Knife", "Pizza cutter", "Scissors"]` - this block reveals the defect

## Defect report
- Title: Excluding all three tools makes /api/pizza answer 500 with an empty body
- Request: `POST /api/pizza` with header `Authorization: token abcdef0123456789` and body `{"excludedTools": ["Knife","Pizza cutter","Scissors"]}`
- Expected result: status 400 and a JSON error message, because no pizza can satisfy the request
- Actual result: status 500 Internal Server Error, `Content-Length: 0` (empty body)
- Severity: Medium. A client error is reported as a server failure with no message, so the app cannot tell the user what to change. No data is lost.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: read -> 404 (`{"error":"not found"}`), change (PUT) -> 400 (`{"error":"rating ID ... not found"}`), delete -> 400 (`{"error":"rating ID ... not found"}`). In every case the owner's rating was unchanged afterwards.

## Part B
1. Real-network tests can find failures in the deployment and the infrastructure that a stubbed unit test cannot see: e.g. the load balancer sending requests to a different server (session/cookie problem), wrong status codes or JSON fields as really serialised, auth being wrongly configured, network/TLS errors, and the server crashing with 500 (Defect 1). Unit tests with stubs are still worth writing because they are fast, deterministic, free of network flakiness, run without the shared server, and point to the exact failing function.
2. The public token's ratings belong to everyone, so another student could change or delete data while my test runs, giving random failures, and my tests could damage their data. A new user with a unique name gives each test private data, so tests are independent and repeatable. In Project 2 I will create my own customer/booking/product (with unique names) in each test, only touch what my tests created, and delete it afterwards, since the shop/hotel is shared with other groups.
3. The site runs on several servers behind a load balancer and each server has its own users. The AWSALB cookie pins a client to one server, and a `requests.Session` keeps that cookie, so creating the user and logging in reach the same server. Without a session the login can hit a server that never saw the user and fail with 401 (flaky). I did not do Step 0.12 (optional), so I have no three runs to describe.
4. The block where all three tools are excluded (3 of 3) revealed it; one or two excluded work. A 500 with an empty body tells the app nothing: it looks like a server fault, may trigger retries or a generic crash message, and gives no hint of what to fix. A 400 with a message tells the app that the input was wrong and why. The test stays as xfail (strict) so the defect stays documented and visible, the rest of the suite stays green, and the run fails when QuickPizza fixes it, reminding us to remove the mark; deleting it would lose that knowledge and the regression protection.
5. Base choice: one base test plus (number of blocks - 1) per characteristic: 1 + (3-1) + (4-1) + (2-1) + (3-1) = 1 + 2 + 3 + 1 + 2 = 9 tests. All combinations: 3 x 4 x 2 x 3 = 72 tests.
6. Read -> 404, change -> 400, delete -> 400. I would expect 403 Forbidden (or 404 for all, to avoid revealing that the rating exists) consistently for all three. The important requirement (access refused and data unchanged) is met, so it is not a security defect, but 400 for PUT/DELETE is inconsistent with the 404 on GET and misuses "Bad Request" (the request itself is valid); it is a minor API-design defect/inconsistency.
7. `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` returned 200 with a JSON list of about 50 ratings (belonging to the public/shared data) instead of 401. Yes, it is a defect: the server accepts a token that nobody issued (any 16-character token seems to work), so authentication is not really checked. On a real system a stranger could invent a token and read, and probably change or delete, other people's data. I only read with it.
8. An API test checks business rules, status codes, error messages and data in the response better and faster (e.g. boundary values for stars, many invalid inputs, authorization), without the browser. Only a test through the web pages can check what the user sees: layout, rendering, JavaScript behaviour, links/buttons, and that the page really calls the API correctly.
