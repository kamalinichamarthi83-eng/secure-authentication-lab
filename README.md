# secure-authentication-lab
Secure local authentication lab with password hashing, validation, rate limiting, and secure sessions.
## Security Controls Implemented

### 1. Password Hashing
Passwords are never stored as plaintext. Passwords are stored using secure password hashing.

### 2. Server-Side Validation
Username and password input is validated on the server before registration or authentication.

### 3. Secure Sessions
Authenticated sessions use HttpOnly, Secure, and SameSite cookie settings.

Sessions expire after 30 minutes.

### 4. Logout
The logout endpoint clears the authenticated session.

### 5. Rate Limiting
Repeated login attempts are rate-limited to reduce brute-force attacks.

### 6. Generic Authentication Errors
Failed login attempts return the generic message:

"Invalid username or password"

This helps prevent username enumeration.

## Automated Security Tests

GitHub Actions automatically runs the authentication security test suite.

Tests cover:

- Password hashing
- Invalid input rejection
- Successful authentication
- Incorrect password handling
- Generic authentication errors
- Rate limiting
- Protected routes
- Logout
- Session cookie security settings

### Test Result

Authentication Security Tests: PASSED ✅

All automated authentication security tests completed successfully.

## Project Files

- `app.py` — authentication service
- `test_auth.py` — automated security tests
- `requirements.txt` — Python dependencies
- `security-note.md` — authentication security notes
- `.github/workflows/main.yml` — automated test workflow
