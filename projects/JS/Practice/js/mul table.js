document.addEventListener("DOMContentLoaded", main);


function calctable(inputnum, resultelement) {
    const number = parseInt(inputnum.value, 10);

    if (isNaN(number)) {
        resultelement.textContent = "Please enter a valid number.";
        return;
    }

    if (number == 0) {
        resultelement.innerHTML = "<p>Please enter a valid<br>non-zero number</p>";
        return;
    }

    let table = "";
    for (let i = 1; i <= 10; i++) {
        table += `<p><br>${number} x ${i} = ${number * i}</p>`;
    }

    resultelement.innerHTML = table;
}




function main() {
    let resultelement = document.getElementById("ResultTable");
    let submit = document.getElementById("SubmitButton");
    let inputnum = document.getElementById("InputNum"); // Assuming you have an input field

    submit.addEventListener("click", () => {
        calctable (inputnum, resultelement);
    });
}