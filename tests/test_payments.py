/**
 * Generated test cases for bug validation.
 */
const { describe, it, expect } = require('@jest/globals');


// Tests for calculate_tax
// Bug fix: Fixed incorrect tax calculation for orders under $100

describe('CalculateTax', () => {

  it('Should calculate 8.5% tax on $49.99 correctly after fix', () => {
    const subtotal = 49.99;
    const result = calculateTax(subtotal);
    expect(result).toBe(4.25);
  });

  it('Should calculate 8.5% tax on $50.00 correctly after fix', () => {
    const subtotal = 50.0;
    const result = calculateTax(subtotal);
    expect(result).toBe(4.25);
  });

  it('Should calculate 8.5% tax on $99.99 correctly after fix', () => {
    const subtotal = 99.99;
    const result = calculateTax(subtotal);
    expect(result).toBe(8.5);
  });

});