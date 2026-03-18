const request = require("supertest");
const app = require("../src/index");
const { sequelize, Product } = require("../src/models");

let authToken;

beforeAll(async () => {
  await sequelize.sync({ force: true });

  // Register a test user to get auth token
  const res = await request(app)
    .post("/api/auth/register")
    .send({
      email: "producttest@example.com",
      password: "password123",
      name: "Product Test",
    });

  authToken = res.body.token;

  // Seed products
  const products = [];
  for (let i = 1; i <= 25; i++) {
    products.push({
      name: `Product ${i}`,
      description: `Description for product ${i}`,
      price: (i * 10.99).toFixed(2),
      stock: i * 5,
      category: i % 3 === 0 ? "electronics" : i % 2 === 0 ? "clothing" : "books",
    });
  }
  await Product.bulkCreate(products);
});

afterAll(async () => {
  await sequelize.close();
});

describe("GET /api/products", () => {
  test("should list products with default pagination", async () => {
    const res = await request(app).get("/api/products");

    expect(res.statusCode).toBe(200);
    expect(res.body.products).toBeDefined();
    expect(res.body.total).toBe(25);
  });

  test("should return first page correctly", async () => {
    const res = await request(app).get("/api/products?page=1&limit=5");

    expect(res.statusCode).toBe(200);
    expect(res.body.products.length).toBe(5);
    expect(res.body.page).toBe(1);

    expect(res.body.totalPages).toBe(5);
  });

  test("should return correct products on page 2", async () => {
    const page1 = await request(app).get("/api/products?page=1&limit=5");
    const page2 = await request(app).get("/api/products?page=2&limit=5");

    expect(page2.statusCode).toBe(200);

    // Pages should not overlap
    const page1Ids = page1.body.products.map((p) => p.id);
    const page2Ids = page2.body.products.map((p) => p.id);
    const overlap = page1Ids.filter((id) => page2Ids.includes(id));
    expect(overlap.length).toBe(0);
  });
});

describe("GET /api/products/search", () => {
  test("should search products by name", async () => {
    const res = await request(app).get("/api/products/search?q=Product");

    expect(res.statusCode).toBe(200);
    expect(res.body.products).toBeDefined();
    expect(res.body.count).toBeGreaterThan(0);
  });

  test("should return 400 without query parameter", async () => {
    const res = await request(app).get("/api/products/search");

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toContain("Search query");
  });

  test("should reject SQL injection attempts", async () => {
    // Test for basic SQL injection
    const res1 = await request(app).get("/api/products/search?q=test' OR '1'='1");
    expect(res1.statusCode).toBe(200);
    expect(res1.body.products.length).toBeLessThan(25); // Should not return all products

    // Test for UNION-based SQL injection
    const res2 = await request(app).get("/api/products/search?q=test' UNION SELECT id,email,password_hash,null,null FROM users--");
    expect(res2.statusCode).toBe(200);
    expect(res2.body.products.length).toBeLessThan(25); // Should not return all products or sensitive data
  });

  test("should return filtered results for valid search queries", async () => {
    const res = await request(app).get("/api/products/search?q=Product 1");
    expect(res.statusCode).toBe(200);
    expect(res.body.products.length).toBeGreaterThan(0);
    expect(res.body.products.every(p => p.name.includes("Product 1"))).toBe(true);
  });
});

describe("GET /api/products/:id", () => {
  test("should return product by ID", async () => {
    const listRes = await request(app).get("/api/products?page=1&limit=1");
    const productId = listRes.body.products[0].id;

    const res = await request(app).get(`/api/products/${productId}`);
    expect(res.statusCode).toBe(200);
    expect(res.body.product.id).toBe(productId);
  });

  test("should return 404 for non-existent product", async () => {
    const res = await request(app).get("/api/products/99999");
    expect(res.statusCode).toBe(404);
  });
});

describe("POST /api/products", () => {
  test("should create a new product", async () => {
    const res = await request(app)
      .post("/api/products")
      .set("Authorization", `Bearer ${authToken}`)
      .send({
        name: "New Product",
        description: "A brand new product",
        price: 29.99,
        stock: 100,
        category: "books",
      });

    expect(res.statusCode).toBe(201);
    expect(res.body.product.name).toBe("New Product");
  });

  test("should reject product without name", async () => {
    const res = await request(app)
      .post("/api/products")
      .set("Authorization", `Bearer ${authToken}`)
      .send({ price: 29.99 });

    expect(res.statusCode).toBe(400);
  });

  test("should require authentication", async () => {
    const res = await request(app)
      .post("/api/products")
      .send({ name: "Test", price: 9.99 });

    expect(res.statusCode).toBe(401);
  });
});
