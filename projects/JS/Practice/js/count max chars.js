document.addEventListener("DOMContentLoaded", main);

function calcmaxchar(input, countarray, result) {
    let CharArray = Array.from(input.toLowerCase());

    for (let Char of CharArray) {
        // Only process alphabetic characters
        if (Char >= 'a' && Char <= 'z') {
            let index = Char.charCodeAt(0) - 'a'.charCodeAt(0);
            countarray[index] += 1;
            console.log(`Character: ${Char}, Index: ${index}, Count: ${countarray[index]}`);
        }
    }

    // Find the maximum count and its index using linear search
    let maxCount = countarray[0];
    let maxIndex = 0;

    for (let i = 1; i < countarray.length; i++) {
        if (countarray[i] > maxCount) {
            maxCount = countarray[i];
            maxIndex = i;
        }
    }

    // Convert index back to character
    let maxChar = String.fromCharCode(maxIndex + 'a'.charCodeAt(0));

    result.innerHTML = `Counts: ${countarray.join(', ')}<br>Max Count: ${maxCount}<br>Character: '${maxChar}'`;
    return { countarray, maxCount, maxIndex, maxChar };
}

function main() {
    let CountArray = Array.from(
        { length: 26 },
        () => 0
    );

    let resultelement = document.getElementById("Result");
    let submit = document.getElementById("SubmitButton");
    let inputElement = document.getElementById("InputString"); // Assuming you have an input field

    submit.addEventListener("click", () => {
        // Get the current input value instead of using a fixed string
        let input = inputElement ? inputElement.value : "abcd"; // fallback to "abcd" if no input element
        calcmaxchar(input, CountArray, resultelement);
    });
}