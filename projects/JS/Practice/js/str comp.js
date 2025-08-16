function compareStrings(str1, str2) {
    // Rule 2: Compare lengths first - shorter strings are "less than" longer strings.
    if (str1.length !== str2.length) {
        return str1.length < str2.length ? -1 : 1;
    }

    // If lengths are equal, compare character by character.
    for (let i = 0; i < str1.length; i++) {
        const char1 = str1[i];
        const char2 = str2[i];

        if (char1 !== char2) {
            const ascii1 = char1.charCodeAt(0);
            const ascii2 = char2.charCodeAt(0);

            // Check if both are letters.
            const isLetter1 = /[a-zA-Z]/.test(char1);
            const isLetter2 = /[a-zA-Z]/.test(char2);

            if (isLetter1 && isLetter2) {
                const lower1 = char1.toLowerCase();
                const lower2 = char2.toLowerCase();

                // Rule 3: If it's the same letter but different case.
                if (lower1 === lower2) {
                    // Rule 1: Lowercase letters are considered "less than" uppercase ones.
                    return char1 === lower1 ? -1 : 1;
                }

                // Rule 3: Earlier letters in the alphabet are "less than" later ones.
                return lower1 < lower2 ? -1 : 1;
            }

            // Rule 4: For non-letters or mixed types, use standard ASCII value comparison.
            return ascii1 < ascii2 ? -1 : 1;
        }
    }

    // If all characters are the same, the strings are equal.
    return 0;
}

/**
 * This function is called when the compare button is clicked in the HTML.
 * It gets the input values, compares them, and displays the result.
 */
function performComparison() {
    // Get the values from the input fields.
    const string1 = document.getElementById('string1').value;
    const string2 = document.getElementById('string2').value;
    const resultDiv = document.getElementById('result');

    // Get the numerical result from the core comparison function.
    const result = compareStrings(string1, string2);

    let relationSymbol;
    let relationText;

    // Determine the relationship based on the result.
    if (result < 0) {
        relationSymbol = '<';
        relationText = 'is less than';
    } else if (result > 0) {
        relationSymbol = '>';
        relationText = 'is greater than';
    } else {
        relationSymbol = '=';
        relationText = 'is equal to';
    }
    
    // Display the result in a user-friendly format with dark theme classes.
    resultDiv.innerHTML = `
        <div class="text-2xl md:text-3xl font-bold">
            <span class="text-sky-400">"${string1}"</span>
            <span class="mx-4 text-gray-500">${relationSymbol}</span>
            <span class="text-sky-400">"${string2}"</span>
        </div>
        <div class="mt-2 text-lg text-gray-400">
            Result: "${string1}" ${relationText} "${string2}".
        </div>
    `;
    resultDiv.classList.remove('hidden');
}

// Add an event listener to the compare button.
// The 'DOMContentLoaded' event ensures the script runs after the entire HTML document has been loaded.
document.addEventListener('DOMContentLoaded', () => {
    const compareBtn = document.getElementById('compareBtn');
    if (compareBtn) {
        compareBtn.addEventListener('click', performComparison);
    }
});
