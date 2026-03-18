const { validateEmail } = require('../src/middleware/validate');

describe('Email Validation', () => {
  test('should accept valid email with plus addressing', () => {
    const email = 'user+tag@example.com';
    const isValid = validateEmail(email);
    expect(isValid).toBe(true);
  });

  test('should accept valid email with dots', () => {
    const email = 'first.middle.last@example.com';
    const isValid = validateEmail(email);
    expect(isValid).toBe(true);
  });

  test('should reject invalid email without @ symbol', () => {
    const email = 'userexample.com';
    const isValid = validateEmail(email);
    expect(isValid).toBe(false);
  });

  test('should reject invalid email without domain', () => {
    const email = 'user@';
    const isValid = validateEmail(email);
    expect(isValid).toBe(false);
  });
});