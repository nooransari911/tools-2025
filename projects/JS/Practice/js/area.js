document.addEventListener("DOMContentLoaded", main);

function main() {
    // --- Area of triangle ---
    const TriHeight = document.getElementById("TriHeight");
    const TriBase = document.getElementById("TriBase");
    const TriSubmit = document.getElementById("TriSubmitButton");
    const TriResult = document.getElementById("TriResult");

    TriSubmit.addEventListener("click", () => {
        const height = parseFloat(TriHeight.value);
        const base = parseFloat(TriBase.value);
        // Check if inputs are valid numbers
        if (isNaN(height) || isNaN(base)) {
            TriResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        TriResult.innerHTML = `Area of Triangle is: ${(0.5) * (height * base)}`;
    });




/*     // --- Area of square ---
    const SqSide = document.getElementById("SqSide");
    const SqSubmit = document.getElementById("SqSubmitButton");
    const SqResult = document.getElementById("SqResult");

    SqSubmit.addEventListener("click", () => {
        const side = parseFloat(SqSide.value);
        // Check if inputs are valid numbers
        if (isNaN(side)) {
            SqResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        SqResult.innerHTML = `Area of Square is: ${(side * side)}`;
    }); */




    // --- Area of triangle ---
    const RectHeight = document.getElementById("RectHeight");
    const RectBase = document.getElementById("RectBase");
    const RectSubmit = document.getElementById("RectSubmitButton");
    const RectResult = document.getElementById("RectResult");

    RectSubmit.addEventListener("click", () => {
        const height = parseFloat(RectHeight.value);
        const base = parseFloat(RectBase.value);
        // Check if inputs are valid numbers
        if (isNaN(height) || isNaN(base)) {
            RectResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        RectResult.innerHTML = `Area of Rectangle is: ${(height * base)}`;
    });



    // --- Area of circle ---
    const CircRad = document.getElementById("CircRad");
    const CircSubmit = document.getElementById("CircSubmitButton");
    const CircResult = document.getElementById("CircResult");

    CircSubmit.addEventListener("click", () => {
        const radius = parseFloat(CircRad.value);
        // Check if inputs are valid numbers
        if (isNaN(radius)) {
            CircResult.innerHTML = "Please enter valid numbers.";
            return;
        }
        CircResult.innerHTML = `Area of Circle is: ${(Math.PI) * (radius * radius)}`;
    });
}