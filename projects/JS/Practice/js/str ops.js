/**
 * Displays a message in the result container.
 * @param {string} message - The text message to display.
 * @param {boolean} isError - If true, formats the message as an error.
 */
function ShowResult(message, isError = false) {
    const resultDiv = document.getElementById('Result');
    resultDiv.innerHTML = ''; // Clear previous result
    const resultSpan = document.createElement('span');
    resultSpan.textContent = message;
    // Apply different text colors for results and errors
    resultSpan.className = isError ? 'text-red-500 font-semibold' : 'text-green-400 font-semibold text-lg';
    resultDiv.appendChild(resultSpan);
}

/**
 * Checks if a given string is a palindrome.
 * @param {string} str - The input string.
 * @returns {string} - A message indicating if the string is a palindrome.
 */
function CheckPalindrome(str) {
    // Normalize the string: convert to lowercase and remove non-alphanumeric characters.
    const normalizedStr = str.toLowerCase().replace(/[\W_]/g, '');
    if (normalizedStr.length === 0) {
        return "Please enter some text to check.";
    }
    // Reverse the normalized string.
    const reversedStr = normalizedStr.split('').reverse().join('');
    // Compare the original normalized string with the reversed one.
    return normalizedStr === reversedStr
        ? `"${str}" is a palindrome!`
        : `"${str}" is not a palindrome.`;
}

/**
 * Reverses a given string.
 * @param {string} str - The input string.
 * @returns {string} - The reversed string.
 */
function ReverseString(str) {
    return str.split('').reverse().join('');
}

/**
 * Replaces the first occurrence of a character in a string with another character.
 * @param {string} str - The main string.
 * @param {string} target - The character to find.
 * @param {string} replacement - The character to replace with.
 * @returns {string|null} - The modified string, or null if validation fails.
 */
function ReplaceFirstChar(str, target, replacement) {
    // Validate that target and replacement characters are provided and are single characters
    if (!target || !replacement || target.length !== 1 || replacement.length !== 1) {
        ShowResult("Please enter a single character for both 'Find' and 'Replacement' fields.", true);
        return null; // Return null to indicate an error
    }
    return str.replace(target, replacement);
}

/**
 * Toggles the visibility of the input fields required for the 'replace' operation.
 */
function ToggleReplaceFields() {
    const operationSelect = document.getElementById('OperationSelect');
    const replaceFields = document.getElementById('ReplaceFields');
    if (operationSelect.value === 'replace') {
        replaceFields.classList.remove('hidden');
    } else {
        replaceFields.classList.add('hidden');
    }
}

/**
 * Main function to handle the calculation when the button is clicked.
 */
function PerformOperation() {
    const inputStr = document.getElementById('InputStr');
    const operationSelect = document.getElementById('OperationSelect');
    
    const str = inputStr.value;
    const operation = operationSelect.value;

    console.log (inputStr);

    // Basic validation: ensure the main string is not empty
    if (!str) {
        ShowResult('Please enter a string to get started.', true);
        return;
    }

    let result;

    // Use a switch statement to call the correct function based on user selection
    switch (operation) {
        case 'palindrome':
            result = CheckPalindrome(str);
            ShowResult(result);
            break;

        case 'reverse':
            result = ReverseString(str);
            ShowResult(`Reversed: ${result}`);
            break;

        case 'replace':
            const charToTarget = document.getElementById('CharToTarget');
            const charToReplace = document.getElementById('CharToReplace');
            const target = charToTarget.value;
            const replacement = charToReplace.value;
            result = ReplaceFirstChar(str, target, replacement);
            // Only show result if the replace function didn't return an error (null)
            if (result !== null) {
                ShowResult(`Result: ${result}`);
            }
            break;

        default:
            ShowResult('Please select a valid operation.', true);
    }
}

/**
 * The main entry point for the script.
 * It sets up event listeners after the DOM is fully loaded.
 */
function Main() {
    const operationSelect = document.getElementById('OperationSelect');
    const submitButton = document.getElementById('SubmitButton');

    // Listen for changes on the dropdown to show/hide the replace fields
    operationSelect.addEventListener('change', ToggleReplaceFields);

    // Listen for clicks on the submit button to perform the calculation
    submitButton.addEventListener('click', PerformOperation);
}

// Set the Main function to run after the HTML document has finished loading.
document.addEventListener("DOMContentLoaded", Main);
