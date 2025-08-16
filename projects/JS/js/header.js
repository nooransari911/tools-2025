document.addEventListener ("DOMContentLoaded", function () {
    let PageRootHeadingLevel = 1;
    let SectionHeadingLevel = 2;
    let SubsectionHeadingLevel = 3;    


    let PageRoot = document.getElementById ("L1N0");
    PageRoot.insertAdjacentHTML ("afterbegin", `<h${PageRootHeadingLevel}>Page Title</h${PageRootHeadingLevel}>`);

    let SectionElements = document.querySelectorAll (".Section");
    //console.log (SectionElements);
    SectionElements.forEach ((element, i) => {
        element.insertAdjacentHTML ("afterbegin", `<h${SectionHeadingLevel}>Section ${i + 1}</h${SectionHeadingLevel}>`);
    });

    let Subsection1Elements = document.querySelectorAll (".Subsection1");
    //console.log (Subsection1Elements);
    Subsection1Elements.forEach ((element, i) => {
        element.insertAdjacentHTML ("afterbegin", `<h${SubsectionHeadingLevel}>Subsection ${i + 1}</h${SubsectionHeadingLevel}>`);
    })
})
