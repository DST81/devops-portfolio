#!/usr/bin/env bash
#
# Smoke test for the libraryApp application.
#
# Usage:
#   ./smoke-test.sh https://libraryapp-sxmp.onrender.com
#
# Exercises the critical path end to end against a *running* instance:
#   1. /health   liveness (retried with backoff, because a Render free
#                instance is spun down after 15 min and needs up to a minute
#                to wake up on the first request)
#   2. /ready    readiness
#   3. POST      create a member and book
#   4. POST      borrow the book and verify the member's loan list
#   5. POST      return the book and verify availability
#   6. DELETE    remove the test book and member
#
# Exits non-zero on the first failing check so a CI job fails loudly, and
# prints "SMOKE TEST PASSED" only when every check succeeded.
#
# Data is held in memory by the app; the test creates and removes its own
# records. Dependencies: bash, curl, grep. No jq is required.

set -euo pipefail

# --- arguments ---------------------------------------------------------------

if [ "$#" -ne 1 ]; then
  echo "usage: $0 <base-url>" >&2
  echo "example: $0 https://libraryapp-sxmp.onrender.com" >&2
  exit 2
fi

# Strip a trailing slash so we can concatenate paths without doubling it.
BASE_URL="${1%/}"

# Retry budget for /health. A cold Render free instance can take ~30-60 s
# (occasionally up to a minute) to come back. Linear backoff: 5, 10, 15, ...
# Override via environment when needed, e.g. HEALTH_RETRIES=20 ./smoke-test.sh
HEALTH_RETRIES="${HEALTH_RETRIES:-12}"
BACKOFF_SECONDS="${BACKOFF_SECONDS:-5}"

# Shared curl options. We deliberately do NOT use --fail: curl must return the
# body and status even on 4xx/5xx so we can assert on them ourselves.
CURL_OPTS=(--silent --show-error --connect-timeout 10 --max-time 60)

echo "Target: ${BASE_URL}"

# --- helpers -----------------------------------------------------------------

# fail MESSAGE -> print message and abort with a non-zero exit code.
fail() {
  echo "FAIL: $1" >&2
  exit 1
}

# Global scratch variables filled by split_response().
STATUS=""
BODY=""

# Split a curl response of the form "<body>\n<http_status>" (produced with
# -w '\n%{http_code}') into BODY and STATUS using bash parameter expansion.
split_response() {
  local raw="$1"
  STATUS="${raw##*$'\n'}"   # everything after the last newline = status code
  BODY="${raw%$'\n'*}"      # everything before the last newline = body
}

MEMBER_ID=""
BOOK_ID=""

cleanup() {
  if [ -n "$BOOK_ID" ]; then
    if [ -n "$MEMBER_ID" ]; then
      curl "${CURL_OPTS[@]}" -X POST \
        -H 'Content-Type: application/json' \
        -d "{\"member_id\":${MEMBER_ID}}" \
        "${BASE_URL}/api/books/${BOOK_ID}/return" >/dev/null 2>&1 || true
    fi
    curl "${CURL_OPTS[@]}" -X DELETE \
      "${BASE_URL}/api/books/${BOOK_ID}" >/dev/null 2>&1 || true
  fi
  if [ -n "$MEMBER_ID" ]; then
    curl "${CURL_OPTS[@]}" -X DELETE \
      "${BASE_URL}/api/members/${MEMBER_ID}" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT

# --- 1/5 liveness with cold-start backoff ------------------------------------

echo "== 1/6 waiting for /health (tolerates a cold start) =="

attempt=1
healthy=0
while [ "$attempt" -le "$HEALTH_RETRIES" ]; do
  # Guard the request: a not-yet-awake instance may refuse the connection,
  # which makes curl exit non-zero and would trip 'set -e' without this 'if'.
  if raw="$(curl "${CURL_OPTS[@]}" -w $'\n%{http_code}' "${BASE_URL}/health" 2>/dev/null)"; then
    split_response "$raw"
    if [ "$STATUS" = "200" ] && printf '%s' "$BODY" | grep -q '"status":"ok"'; then
      echo "  /health OK (attempt ${attempt}): ${BODY}"
      healthy=1
      break
    fi
  fi
  wait_for=$(( BACKOFF_SECONDS * attempt ))
  echo "  not ready yet (attempt ${attempt}/${HEALTH_RETRIES}); waiting ${wait_for}s..."
  sleep "$wait_for"
  attempt=$(( attempt + 1 ))
done

[ "$healthy" -eq 1 ] || fail "/health did not become healthy after ${HEALTH_RETRIES} attempts"

# --- 2/5 readiness -----------------------------------------------------------

echo "== 2/6 checking /ready =="
raw="$(curl "${CURL_OPTS[@]}" -w $'\n%{http_code}' "${BASE_URL}/ready")" || fail "/ready request failed"
split_response "$raw"
[ "$STATUS" = "200" ] || fail "/ready returned HTTP ${STATUS} (expected 200); body: ${BODY}"
printf '%s' "$BODY" | grep -q '"status":"ready"' || fail "/ready body missing status ready: ${BODY}"
echo "  /ready OK: ${BODY}"

# --- 3/6 create member -------------------------------------------------------

echo "== 3/6 creating a member via POST /api/members =="
member_name="Smoke Test ${RANDOM}-$$"
member_email="smoke-${RANDOM}-$$@example.test"
raw="$(curl "${CURL_OPTS[@]}" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"${member_name}\",\"email\":\"${member_email}\"}" \
  -w $'\n%{http_code}' \
  "${BASE_URL}/api/members")" || fail "POST /api/members request failed"
split_response "$raw"
[ "$STATUS" = "201" ] || fail "POST /api/members returned HTTP ${STATUS} (expected 201); body: ${BODY}"
printf '%s' "$BODY" | grep -q "\"name\":\"${member_name}\"" || fail "created member is missing its name: ${BODY}"

if [[ "$BODY" =~ \"id\"[[:space:]]*:[[:space:]]*([0-9]+) ]]; then
  MEMBER_ID="${BASH_REMATCH[1]}"
else
  fail "could not parse a member id from: ${BODY}"
fi
echo "  created member id=${MEMBER_ID}"

# --- 4/6 create book ---------------------------------------------------------

echo "== 4/6 creating a book via POST /api/books =="
book_title="Smoke Test Book ${RANDOM}-$$"
book_author="Smoke Test Author"
book_isbn="smoke-${RANDOM}-$$"
raw="$(curl "${CURL_OPTS[@]}" \
  -H 'Content-Type: application/json' \
  -d "{\"title\":\"${book_title}\",\"author\":\"${book_author}\",\"isbn\":\"${book_isbn}\"}" \
  -w $'\n%{http_code}' \
  "${BASE_URL}/api/books")" || fail "POST /api/books request failed"
split_response "$raw"
[ "$STATUS" = "201" ] || fail "POST /api/books returned HTTP ${STATUS} (expected 201); body: ${BODY}"
printf '%s' "$BODY" | grep -q "\"title\":\"${book_title}\"" || fail "created book is missing its title: ${BODY}"

if [[ "$BODY" =~ \"id\"[[:space:]]*:[[:space:]]*([0-9]+) ]]; then
  BOOK_ID="${BASH_REMATCH[1]}"
else
  fail "could not parse a book id from: ${BODY}"
fi
echo "  created book id=${BOOK_ID}"

# --- 5/6 borrow and verify member -------------------------------------------

echo "== 5/6 borrowing book ${BOOK_ID} for member ${MEMBER_ID} =="
raw="$(curl "${CURL_OPTS[@]}" \
  -H 'Content-Type: application/json' \
  -d "{\"member_id\":${MEMBER_ID}}" \
  -w $'\n%{http_code}' \
  "${BASE_URL}/api/books/${BOOK_ID}/borrow")" || fail "POST /api/books/${BOOK_ID}/borrow request failed"
split_response "$raw"
[ "$STATUS" = "200" ] || fail "borrow returned HTTP ${STATUS} (expected 200); body: ${BODY}"
printf '%s' "$BODY" | grep -q '"status":"borrowed"' || fail "borrow response does not show a borrowed book: ${BODY}"
printf '%s' "$BODY" | grep -Eq '"borrowed_to"[[:space:]]*:[[:space:]]*'"${MEMBER_ID}" || fail "borrow response has the wrong member id: ${BODY}"

raw="$(curl "${CURL_OPTS[@]}" -w $'\n%{http_code}' "${BASE_URL}/api/members/${MEMBER_ID}")" || fail "GET /api/members/${MEMBER_ID} request failed"
split_response "$raw"
[ "$STATUS" = "200" ] || fail "GET /api/members/${MEMBER_ID} returned HTTP ${STATUS} (expected 200); body: ${BODY}"
printf '%s' "$BODY" | grep -Eq '"borrowed_count"[[:space:]]*:[[:space:]]*1' || fail "member does not show one borrowed book: ${BODY}"
printf '%s' "$BODY" | grep -q "\"title\":\"${book_title}\"" || fail "member's borrowed book list is missing the book title: ${BODY}"
echo "  borrow and member overview OK"

# --- 6/6 return, verify, and delete ------------------------------------------

echo "== 6/6 returning book ${BOOK_ID} =="
raw="$(curl "${CURL_OPTS[@]}" \
  -H 'Content-Type: application/json' \
  -d "{\"member_id\":${MEMBER_ID}}" \
  -w $'\n%{http_code}' \
  "${BASE_URL}/api/books/${BOOK_ID}/return")" || fail "POST /api/books/${BOOK_ID}/return request failed"
split_response "$raw"
[ "$STATUS" = "200" ] || fail "return returned HTTP ${STATUS} (expected 200); body: ${BODY}"
printf '%s' "$BODY" | grep -q '"status":"available"' || fail "return response does not show an available book: ${BODY}"
printf '%s' "$BODY" | grep -q '"borrowed_to":null' || fail "return response still shows a borrower: ${BODY}"
printf '%s' "$BODY" | grep -Eq '"borrowed_count"[[:space:]]*:[[:space:]]*0' || fail "return response does not show zero borrowed books: ${BODY}"

status="$(curl "${CURL_OPTS[@]}" -o /dev/null -w '%{http_code}' -X DELETE "${BASE_URL}/api/books/${BOOK_ID}")" || fail "DELETE /api/books/${BOOK_ID} request failed"
[ "$status" = "200" ] || fail "DELETE /api/books/${BOOK_ID} returned HTTP ${status} (expected 200)"
BOOK_ID=""

status="$(curl "${CURL_OPTS[@]}" -o /dev/null -w '%{http_code}' -X DELETE "${BASE_URL}/api/members/${MEMBER_ID}")" || fail "DELETE /api/members/${MEMBER_ID} request failed"
[ "$status" = "200" ] || fail "DELETE /api/members/${MEMBER_ID} returned HTTP ${status} (expected 200)"
MEMBER_ID=""
echo "  returned book and removed smoke-test records"

echo
echo "SMOKE TEST PASSED"
