# Authentication Security Note

## Password Storage

Passwords are never stored as plaintext. The application uses Werkzeug's
secure password hashing functions to store password hashes.

## Server-Side Validation

Registration input is validated on the server. Usernames have length and
character restrictions, and passwords have minimum and maximum length limits.

## Secure Sessions

Authenticated users receive a server-side session. Session cookies are
configured with HttpOnly, Secure, and SameSite settings.

Sessions also have a 30-minute lifetime.

## Logout

Logout clears the current session so that protected resources can no longer
be accessed using the previous authenticated session.

## Rate Limiting

The login endpoint limits repeated authentication attempts. Excessive
attempts receive a 429 response.

## Generic Authentication Errors

Failed authentication returns the same generic message:

"Invalid username or password"

This reduces username enumeration.

## Security Testing

Automated tests verify password hashing, input validation, authentication,
generic errors, rate limiting, protected routes, logout, and session cookie
settings.
