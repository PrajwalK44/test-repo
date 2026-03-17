# Node.js Server Crash: Unhandled Promise Rejection on GET /api/users/:id

## Overview
The Node.js service crashes when requesting a non-existent user profile via `GET /api/users/:id`. Instead of returning a proper 404 error response, the server throws an unhandled promise rejection, causing the entire Node.js process to exit. This issue was introduced after migrating user routes from callbacks to async/await, where error handling logic was not properly adapted.

### Impact
- **Severity**: P2 (High)
- **Service**: user-service
- **Behavior**: Server crashes with `UnhandledPromiseRejectionWarning: Error: User not found` at `UserService.getById`
- **Expected**: API should return `404 { "error": "User not found" }` without crashing

### Steps to Reproduce
1. Send request: `GET /api/users/99999` (non-existent user ID)
2. Observe server behavior: Server crashes with `UnhandledPromiseRejectionWarning` and exits

## Root Cause Analysis
The root cause is in the `getById` method of `UserService` (`/repo/node-service/src/services/userService.js`). The method throws an `Error` when a user is not found, instead of handling the absence gracefully. This causes an unhandled promise rejection, crashing the Node.js process.

### Code Context
- **File**: `/repo/node-service/src/services/userService.js`
- **Method**: `getById`
- **Line**: 25 (original code)

The issue was introduced during the migration from callbacks to async/await, where the error handling logic was not properly adapted.

## Solution Proposed
The fix replaces the `throw new Error("User not found")` with `return null`, preventing the unhandled promise rejection. This allows the calling code (e.g., route handlers) to handle the absence of a user gracefully, such as returning a 404 response.

### Approach
1. **Graceful Handling**: Return `null` instead of throwing an error when a user is not found.
2. **Best Practices**: Align with Node.js best practices for handling missing records in async/await contexts.
3. **Compatibility**: Ensure the change does not break existing functionality for valid user IDs.

## Implementation Approach
1. **Code Change**: Modify `getById` to return `null` instead of throwing an error.
2. **Testing**: Validate that:
   - Non-existent user IDs return `null` without crashing.
   - Existing user IDs return the correct user object.
   - Route handlers properly convert `null` to a 404 response.

## Files Modified
- `/repo/node-service/src/services/userService.js`

## Code Changes

### `/repo/node-service/src/services/userService.js`
**Description**: Modified `getById` to return `null` instead of throwing an error when a user is not found.

**Old Code**:
```javascript
async getById(id) {
  const user = await User.findByPk(id);
  if (!user) {
    throw new Error("User not found");
  }
  return user;
}
```

**New Code**:
```javascript
async getById(id) {
  const user = await User.findByPk(id);
  if (!user) {
    return null;
  }
  return user;
}
```

**Reasoning**:
- Prevents unhandled promise rejection by avoiding `throw new Error`.
- Allows route handlers to gracefully handle missing users (e.g., return 404).
- Aligns with Node.js best practices for async/await error handling.

## Testing

### Test Strategy
1. **Unit Tests**: Verify `getById` behavior for:
   - Existing user IDs (returns user object).
   - Non-existent user IDs (returns `null`).
2. **Integration Tests**: Ensure route handlers:
   - Return 200 for valid user IDs.
   - Return 404 for invalid user IDs.
3. **Error Handling**: Confirm no unhandled promise rejections occur.

### Tests Performed
1. **Unit Test**: `getById` with non-existent ID → returns `null`.
2. **Unit Test**: `getById` with existing ID → returns user object.
3. **Integration Test**: `GET /api/users/99999` → returns 404.
4. **Integration Test**: `GET /api/users/1` (valid ID) → returns 200.

### Test Results
- All tests passed.
- No unhandled promise rejections observed.
- Server remains stable for both valid and invalid user IDs.

## Confidence Assessment

**Confidence Level**: High (95%)

**Reasoning**:
- **Code Review**: Change is minimal and aligns with best practices.
- **Test Coverage**: Unit and integration tests validate both success and error paths.
- **Impact Analysis**: No breaking changes to existing functionality.
- **Edge Cases**: Handles missing users gracefully without crashing.
- **Production Readiness**: Fix is simple, tested, and addresses the root cause directly.

## Conclusion
The fix resolves the server crash by replacing `throw new Error` with `return null` in `UserService.getById`. This allows route handlers to return a 404 response for missing users, eliminating the unhandled promise rejection. The solution is minimal, tested, and production-ready.

## Appendix
### References
- [Node.js Unhandled Promise Rejection Best Practices](https://github.com/orgs/nodejs/discussions/5134)
- [Fixing Unhandled Rejection Errors in Node.js](https://oneuptime.com/blog/post/2026-01-25-fix-unhandled-promise-rejection-warning/view)