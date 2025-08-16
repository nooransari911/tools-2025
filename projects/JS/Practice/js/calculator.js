document.addEventListener("DOMContentLoaded", main);

function main() {
    // --- Addition ---
    const addNum1 = document.getElementById("AddNum1");
    const addNum2 = document.getElementById("AddNum2");
    const addSubmit = document.getElementById("AddSubmitButton");
    const addResult = document.getElementById("AddResult");

    addSubmit.addEventListener("click", () => {
        const num1 = parseFloat(addNum1.value);
        const num2 = parseFloat(addNum2.value);
        // Check if inputs are valid numbers
        if (isNaN(num1) || isNaN(num2)) {
            addResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        addResult.innerHTML = num1 + num2;
    });

    // --- Subtraction ---
    const subNum1 = document.getElementById("SubNum1");
    const subNum2 = document.getElementById("SubNum2");
    const subSubmit = document.getElementById("SubSubmitButton");
    const subResult = document.getElementById("SubResult");

    subSubmit.addEventListener("click", () => {
        const num1 = parseFloat(subNum1.value);
        const num2 = parseFloat(subNum2.value);
        if (isNaN(num1) || isNaN(num2)) {
            subResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        subResult.innerHTML = num1 - num2;
    });

    // --- Multiplication ---
    const mulNum1 = document.getElementById("MulNum1");
    const mulNum2 = document.getElementById("MulNum2");
    const mulSubmit = document.getElementById("MulSubmitButton");
    const mulResult = document.getElementById("MulResult");

    mulSubmit.addEventListener("click", () => {
        const num1 = parseFloat(mulNum1.value);
        const num2 = parseFloat(mulNum2.value);
        if (isNaN(num1) || isNaN(num2)) {
            mulResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        mulResult.innerHTML = num1 * num2;
    });

    // --- Division ---
    const divNum1 = document.getElementById("DivNum1");
    const divNum2 = document.getElementById("DivNum2");
    const divSubmit = document.getElementById("DivSubmitButton");
    const divResult = document.getElementById("DivResult");

    divSubmit.addEventListener("click", () => {
        const num1 = parseFloat(divNum1.value);
        const num2 = parseFloat(divNum2.value);
        if (isNaN(num1) || isNaN(num2)) {
            divResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        // Handle division by zero
        if (num2 === 0) {
            divResult.innerHTML = "Error: Cannot divide by zero.";
            return;
        }
        divResult.innerHTML = num1 / num2;
    });
}