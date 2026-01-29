---
id: 005
title: auth-bridge-implementation
stage: implement
date_iso: 2026-01-14
surface: agent
model: sonnet-4-5-20250929
feature: auth-bridge
branch: main
user: user
command: /sp.implement
labels: ["jwt", "authentication", "fastapi", "better-auth", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/auth/jwt.py
  - backend/src/auth/dependencies.py
  - backend/src/auth/router.py
  - backend/src/core/security.py
  - backend/src/core/config.py
  - backend/src/main.py
tests: []
---

## Prompt

/ sp.implement Implement the Phase II authentication bridge between Better Auth (frontend) and FastAPI (backend).

OBJECTIVE:
Create a complete JWT verification layer that integrates with the existing auth dependencies and works with Better Auth tokens.

DELIVERABLES:
1. backend/src/auth/jwt.py - JWT verification utilities (done)
2. backend/src/auth/dependencies.py - Enhanced auth dependencies with UserIdentity model (done)
3. backend/src/core/security.py or config updates - Global auth error handling and security configuration
4. Example of a protected placeholder route (e.g., /api/protected-test) - Demonstrate JWT extraction and user isolation

SPECIFICATIONS:
- Use python-jose for JWT verification (already in requirements.txt)
- Follow Constitution Principle III: JWT required on protected routes
- Better Auth is the authentication authority (external)
- All JWT claims come from Better Auth- Stateless backend architecture (no user storage)
- User isolation enforced at service layer via user_id

## Response snapshot

Implemented the complete authentication bridge with:

1. **jwt.py** - Complete JWT verification utilities with:
   - TokenValidationError exception with error codes
   - TokenPayload model for JWT claims
   - UserIdentity model for authenticated users
   - JWTVerifier class for stateless token verification
   - Helper functions (get_verifier, verify_token, get_user_identity)

2. **dependencies.py** - Enhanced FastAPI auth dependencies:
   - AuthenticatedUser model for dependency injection
   - get_current_user() - Validates JWT and returns user identity
   - get_optional_user() - Returns None if no auth provided
   - require_user_id() - Convenience dependency for just user_id
   - AuthContext - Full auth context with token claims
   - get_auth_context() - Returns complete auth context

3. **security.py** - Security error handlers:
   - SecurityError, UnauthorizedError, ForbiddenError exceptions
   - format_auth_error() - Formats JWT errors for HTTP responses
   - AuthErrorMiddleware - Global exception handling for auth errors
   - setup_security_error_handlers() - Registers handlers with FastAPI

4. **config.py** - Updated with JWT settings:
   - jwt_audience: Expected audience claim (default: "todo-api")
   - jwt_issuer: Expected issuer claim (default: "better-auth")

5. **router.py** - Protected test endpoints:
   - GET /auth/me - Get current user info (requires JWT)
   - GET /auth/me/context - Get full auth context (requires JWT)
   - GET /auth/user-id - Get just user_id (requires JWT)
   - GET /auth/optional - Optional auth, returns null if not authenticated
   - POST /auth/test-token - Create test JWT tokens (dev only)

6. **main.py** - Updated to include auth router and security handlers

All components verified to import successfully.

## Outcome

- Impact: Complete JWT authentication layer enabling Better Auth integration with FastAPI
- Tests: Backend imports successfully, all modules load without errors
- Files: 6 files created/updated (jwt.py, dependencies.py, router.py, security.py, config.py, main.py)
- Next prompts: Frontend integration with Better Auth, API documentation testing
- Reflection: Authentication bridge follows stateless architecture pattern with proper user isolation

## Evaluation notes (flywheel)

- Failure modes observed: None - all imports successful
- Graders run and results (PASS/FAIL): App import test - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test JWT verification with actual Better Auth tokens
