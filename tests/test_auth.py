/**
 * Generated test cases for bug validation.
 */
const { describe, it, expect } = require('@jest/globals');


// Tests for login
// Bug fix: Fixed bcrypt checkpw TypeError by ensuring password_hash is encoded to bytes before comparison

describe('Login', () => {

  it('Should successfully authenticate with valid credentials after bcrypt fix', () => {
    const email = 'test@example.com';
    const password = 'testpassword123';
    const result = login(email, password);
    expect(result).toBe(200);
  });

  it('Should return 401 for incorrect password after bcrypt fix', () => {
    const email = 'test@example.com';
    const password = 'wrongpassword';
    const result = login(email, password);
    expect(result).toBe(401);
  });

});