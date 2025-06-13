/**
 * Home Page E2E Tests
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): End-to-end tests for the home page
 * الوصف (ع): اختبارات شاملة للصفحة الرئيسية
 */

import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load home page successfully', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Zentix/);

    // Check main content
    await expect(page.locator('h1')).toContainText('Welcome to Zentix');

    // Check navigation
    await expect(page.locator('nav')).toBeVisible();
  });

  test('should handle theme switching', async ({ page }) => {
    // Check initial theme
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');

    // Toggle theme
    await page.click('[data-testid="theme-toggle"]');

    // Check theme change
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  });

  test('should handle language switching', async ({ page }) => {
    // Check initial language
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');

    // Switch to Arabic
    await page.click('[data-testid="language-switch"]');

    // Check language change
    await expect(page.locator('html')).toHaveAttribute('lang', 'ar');
  });

  test('should handle responsive design', async ({ page }) => {
    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();

    // Test desktop view
    await page.setViewportSize({ width: 1280, height: 800 });
    await expect(page.locator('[data-testid="desktop-menu"]')).toBeVisible();
  });

  test('should handle form submission', async ({ page }) => {
    // Fill form
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Check success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });
}); 