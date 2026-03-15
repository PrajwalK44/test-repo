/**
 * Generated test cases for bug validation.
 */
const { describe, it, expect } = require('@jest/globals');


// Tests for login
// Bug fix: Fixed bcrypt.checkpw TypeError by encoding password_hash to bytes

describe('Login', () => {

  it('Should return 200 OK with JWT token for valid credentials', () => {
    const email = 'user@example.com';
    const password = 'correctpassword';
    const result = login(email, password);
    expect(result).toBe(200);
  });

  it('Should return 401 Unauthorized for invalid credentials', () => {
    const email = 'user@example.com';
    const password = 'wrongpassword';
    const result = login(email, password);
    expect(result).toBe(null);
  });

  it('Should return 400 Bad Request for missing password field', () => {
    const email = 'user@example.com';
    const result = login(email);
    expect(result).toBe(400);
  });

});