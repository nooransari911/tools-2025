'''
const { chromium } = require('playwright'); // Use 'firefox' or 'webkit' for other browsers
const readline = require('readline');

// Function to get user input in terminal
const getUserInput = (query) => {
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

return new Promise((resolve) => {
    rl.question(query, (answer) => {
    rl.close();
    resolve(answer);
    });
});
};

(async () => {
// Launch browser in headless mode
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

try {
    // Navigate to the first page
    await page.goto('https://notebooklm.google.com/');
    await page.waitForLoadState('networkidle'); // Ensure the page is fully loaded

    // Prompt user for input to fill the first field
    const firstInputValue = await getUserInput('Enter value for the first input field: ');

    // Select and fill the first input field
    const firstInput = page.locator('input').first();
    await firstInput.fill(firstInputValue);

    // Click the first button
    const firstButton = page.locator('button').first();
    await firstButton.click();

    // Wait for the second page to load
    await page.waitForLoadState('networkidle');

    // Take a screenshot of the second page
    await page.screenshot({ path: 'screenshot_after_first_click.png' });
    console.log('Screenshot saved: screenshot_after_first_click.png');

    // Prompt user for input for the second page
    const secondInputValue = await getUserInput('Enter value for the second input field: ');

    // Select and fill the second input field
    const secondInput = page.locator('input').first(); // Assuming the new page also has an input
    await secondInput.fill(secondInputValue);

    // Click the second button
    const secondButton = page.locator('button').first();
    await secondButton.click();

    // Wait for any final changes to process
    await page.waitForLoadState('networkidle');

    // Take a screenshot after the second button click
    await page.screenshot({ path: 'screenshot_after_second_click.png' });
    console.log('Screenshot saved: screenshot_after_second_click.png');
} catch (error) {
    console.error('Error occurred:', error);
} finally {
    // Close the browser
    await browser.close();
}
})();
'''
