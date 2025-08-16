document.addEventListener("DOMContentLoaded", main);



function CreateElement ({Tag, Content = null, Parent = null, ChildCls = null, ChildId = null, DivCls = null, DivId = null}) {
    let NewDivElement = document.createElement ("div");
    if (DivCls) NewDivElement.className = DivCls;
    if (DivId)  NewDivElement.id = DivId;
    
    let NewElement = document.createElement (Tag);
    if (ChildCls) NewElement.className = ChildCls;
    if (ChildId)  NewElement.id = ChildId;
    if (Content)  NewElement.insertAdjacentHTML ("beforeend", Content);

    NewDivElement.appendChild (NewElement);

    if (Parent) Parent.appendChild (NewDivElement);

    return NewElement;
}


function CreateElementBatch ({
    ChildTag,
    Count,
    ChildBaseTextContent,
    Parent,
    NewParentCls,
    NewParentId,
    DivCls=null,
    DivId=null,
    ChildCls,
    ChildBaseId,
    CreateWrapper = false
}) {
    let NewParentWrapper = document.createElement ("div");
    if (NewParentCls) NewParentWrapper.className = NewParentCls;
    if (NewParentId)  NewParentWrapper.id = NewParentId;

    for (let i=0; i<Count; i++) {
        let ChildTextContent = ChildBaseTextContent + ` ${i+1}`;
        let ChildId = ChildBaseId + + `-${i+1}` + `-${ChildTag}` ;

        let NewElement = CreateElement ({
            Tag: ChildTag,
            Content: ChildTextContent,
            Parent: CreateWrapper ? NewParentWrapper : Parent,
            ChildCls: `${ChildCls} ${ChildTag}`,
            ChildId: ChildId,
            DivCls: DivCls + "-Wrapper",
            DivId: DivId + `-${i+1}-Wrapper`
        })
    }
    

    if (CreateWrapper) Parent.appendChild (NewParentWrapper);

    return NewParentWrapper;
}



function Theme(config) {
    const { triggerSelector, stylesheetId, themes, defaultTheme } = config;

    const trigger = document.querySelector(triggerSelector);
    const stylesheet = document.getElementById(stylesheetId);

    if (!trigger || !stylesheet) {
        console.error("Theme switcher trigger or stylesheet element not found.");
        return;
    }

    // Set the initial state based on the default theme
    stylesheet.href = themes[defaultTheme].file;
    trigger.textContent = themes[defaultTheme].buttonText;

    // The event handler is a closure, accessing variables from its parent scope
    const handleThemeSwitch = () => {
        // Determine the *next* theme
        const currentTheme = stylesheet.getAttribute('href');
        const nextThemeName = (currentTheme === themes.dark.file) ? 'light' : 'dark';
        const nextThemeData = themes[nextThemeName];

        // Apply the next theme
        stylesheet.setAttribute('href', nextThemeData.file);
        trigger.textContent = nextThemeData.buttonText;
    };

    // Attach the single event listener
    trigger.addEventListener('click', handleThemeSwitch);
}




function OnLoadToList (Parent, DataList, Tag) {
    let NewUL = CreateElement ({
        Tag: "ul",
        Parent: Parent,
        ChildCls: `${Parent.className} DataList`,
        ChildId: Parent.id + `DataList`,
        DivCls: `${Parent.className} DataList-Wrapper`,
        DivId: Parent.id + `DataList-Wrapper`
    });


    DataList.forEach ((element, i) => {
        let NewElement = CreateElement ({
            Tag: Tag,
            Content: `${element.title}: ${element.body}`,
            Parent: NewUL,
            ChildCls: `${Parent.className} DataListItem`,
            ChildId: Parent.id + `DataListItem-${i+1}`,
            DivCls: `${Parent.className} DataListItem-Wrapper`,
            DivId: Parent.id + `DataListItem-Wrapper-${i+1}`
        });
    })

    return NewUL;
}


function XHRReqFakeData (Parent) {
    let FakeJSONXHR = new XMLHttpRequest ();
    let LoadDataQuantity = "";
    
    FakeJSONXHR.open ("GET", `https://jsonplaceholder.typicode.com/posts/${LoadDataQuantity}`, true);
    FakeJSONXHR.onload = () => {
        if (FakeJSONXHR.status === 200) {
            let XHRResponseJSON = JSON.parse (FakeJSONXHR.responseText);
            let XHRDataList = [];
            //console.log (XHRResponseJSON);
            XHRResponseJSON.forEach ((element, i) => {
                XHRDataList.push ({
                    title: element.title,
                    body: element.body
                });
            });

            OnLoadToList (Parent, XHRDataList, "li");
        }

        else {
            console.error (`Error: ${FakeJSONXHR.status} - ${FakeJSONXHR.statusText}`);
        }
    }

    FakeJSONXHR.send ();
}

function PreparedXHRs (URLs, Methods, XHRDataList, XHRLoadState, Bodys = null, IsBodys = null) {
    let XHRReqList  = [];
    URLs.forEach ((URL, i) => {
        let NewXHRReqObj = new XMLHttpRequest ();
        NewXHRReqObj.open (Methods [i], URL, true);
        //NewXHRReqObj.setRequestHeader ("Access-Control-Allow-Origin", "*");
        NewXHRReqObj.onload = () => {
            if (NewXHRReqObj.status == 200) {
                XHRLoadState [i] = true;

                let XHRResponseJSON = JSON.parse (NewXHRReqObj.responseText);
                XHRDataList [i] = {
                    "data": XHRResponseJSON
                };
                console.log (XHRResponseJSON);
                document.dispatchEvent (new CustomEvent ("XHRDataLoaded", {
                    detail: {
                        SlidesPosition: i
                    }
                }));
            }
            else {
                console.log (`Error: ${NewXHRReqObj.status} - ${NewXHRReqObj.statusText}`);
            }
        };
        // Add this to catch CORS errors:
        NewXHRReqObj.onerror = (e) => {
            console.log(`XHR Error for index ${i}, URL: ${URL}`);
            console.log('Error event:', e);
            console.log('XHR object:', NewXHRReqObj);
        };
        XHRReqList.push (NewXHRReqObj);
    });

    return XHRReqList;
}




function main () {
    Theme({
        triggerSelector: '#theme-switcher',
        stylesheetId: 'theme-stylesheet',
        defaultTheme: 'dark',
        themes: {
            light: {
                file: '../css/light.css',
                buttonText: 'Switch to Dark Mode'
            },
            dark: {
                file: '../css/dark.css',
                buttonText: 'Switch to Light Mode'
            }
        }
    });
    //console.log ("hello");
    // Get the button and stylesheet elements from the DOM
    const themeSwitcherBtn = document.getElementById('theme-switcher');
    const stylesheet = document.getElementById('theme-stylesheet');

    themeSwitcherBtn.addEventListener('click', Theme);
    let Page = document.getElementById ("PageRoot");
    let DidClickBool = false;



    let Sections = CreateElementBatch ({
        ChildTag: "H1",
        Count: 4,
        ChildBaseTextContent: "Section",
        Parent: Page,
        NewParentCls: "Sections",
        NewParentId: "Sections",
        DivCls: "Section",
        DivId: `Section`,
        ChildCls: "Section",
        ChildBaseId: "Section",
        CreateWrapper: true
    });

    let SectionsArray = Array.from (Sections.children);
    

    SectionsArray.forEach ((element, i) => {
        CreateElementBatch ({
            ChildTag: "H2",
            Count: 4,
            ChildBaseTextContent: "Subsection-L0",
            Parent: element,
            NewParentCls: "Subsections-L0",
            NewParentId: `Subsections-L0-${i+1}`,
            DivCls: "Subsection-L0",
            DivId: `Section-${i+1}-Subsection-L0`,
            ChildCls: "Subsection-L0",
            ChildBaseId: `Section-${i+1}-Subsection-L0`,
            CreateWrapper: false
        });
    });



    let Subsection1 = document.getElementById ("Section-1-Subsection-L0-1-Wrapper");

    Subsection1.addEventListener ("click", (event) => {
        
        XHRReqFakeData (Subsection1);
        console.log (`${event.target.id}`);
        console.log (Subsection1);

        if (DidClickBool) {
            Subsection1.innerHTML = "<H2>Subsection-L0 1</H2>"
            DidClickBool = false;
        }

        else {
            CreateElementBatch ({
                ChildTag: "H3",
                Count: 4,
                ChildBaseTextContent: "Subsection-L1",
                Parent: Subsection1,
                NewParentCls: "Subsections-L1",
                NewParentId: `Subsections-L1`,
                DivCls: "Subsection-L1",
                DivId: `Section-1-Subsection-L1`,
                ChildCls: "Subsection-L1",
                ChildBaseId: `Section-1-Subsection-L1`,
                CreateWrapper: false
            });

            DidClickBool = true;
        }
    })


    let Subsection2 = document.getElementById ("Section-2-Subsection-L0-1-Wrapper");
    let Subsection3 = document.getElementById ("Section-2-Subsection-L0-2-Wrapper");
    let PrevBtn = document.getElementById ("switch-prev");
    let NextBtn = document.getElementById ("switch-next");
    let XHRURLsBaseURL = "https://d3isj3hu8683a4.cloudfront.net/api/json/";
    let XHRURLs = [
        XHRURLsBaseURL + "json-file-0.json",
        XHRURLsBaseURL + "json-file-1.json",
        XHRURLsBaseURL + "json-file-2.json",
        XHRURLsBaseURL + "json-file-3.json"
    ]
    let XHRURLs2 = [
        "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-1.png",
        "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-2.png",
        "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-3.png",
        "https://d3isj3hu8683a4.cloudfront.net/test/img/test-img-4.png"
    ];
    let XHRMethods = [
        "GET",
        "GET",
        "GET",
        "GET"
    ]
    
    let XHRLoadState = [];
    let XHRDataList = [];
    let XHRRequestsList = PreparedXHRs (XHRURLs2, XHRMethods, XHRDataList, XHRLoadState);
    let SlidesPosition = 0;
    let TotalSlidesCount = 4;

    Subsection2.appendChild (PrevBtn);
    Subsection2.appendChild (NextBtn);

    for (let i=0; i< TotalSlidesCount; i++) {
        XHRDataList.push ({
            "dummydata": `dummy ${i}`
        });
    }

    for (let i=0; i< TotalSlidesCount; i++) {
        XHRLoadState.push (false);
    }


    PrevBtn.addEventListener ("click", (event) => {
        if (SlidesPosition > 0) {
            SlidesPosition -= 1;
        }
        else {
            SlidesPosition = TotalSlidesCount - 1;
        }
        console.log (`Prev button hit; value: ${SlidesPosition}`);
        //console.log (`XHRLoadState: ${XHRLoadState}`);
        //console.log (`XHRDataList: ${JSON.stringify (XHRDataList [SlidesPosition])}`);

        if (XHRLoadState [SlidesPosition]) {
            document.dispatchEvent (new CustomEvent ("XHRDataLoaded", {
                detail: {
                    SlidesPosition: SlidesPosition
                }
            }));
        }
        else {
            XHRRequestsList [SlidesPosition].send ();
            console.log (`XHR request sent for slide position: ${SlidesPosition}`);
        }

    })

    NextBtn.addEventListener ("click", (event) => {
        if (SlidesPosition < TotalSlidesCount - 1) {
            SlidesPosition += 1;
        }
        else {
            SlidesPosition = 0;
        }
        console.log (`Next button hit; value: ${SlidesPosition}`);
        //console.log (`XHRLoadState: ${XHRLoadState}`);
        //console.log (`XHRDataList: ${JSON.stringify (XHRDataList [SlidesPosition])}`);


        if (XHRLoadState [SlidesPosition]) {
            document.dispatchEvent (new CustomEvent ("XHRDataLoaded", {
                "detail": {
                    SlidesPosition: SlidesPosition
                }
            }));
        }
        else {
            XHRRequestsList [SlidesPosition].send ();
            console.log (`XHR request sent for slide position: ${SlidesPosition}`);
        }

    })


    document.addEventListener ("XHRDataLoaded", (event) => {
        let DataLoadedSlidesPosition = event.detail.SlidesPosition;
        let DataLoadedSubsectionHTMLData = JSON.stringify (XHRDataList [SlidesPosition], null, 4);
        //console.log (`Data loaded for slide position: ${DataLoadedSlidesPosition}`);
        Subsection3.innerHTML = "";
        
        /* CreateElement ({
            Tag: "code",
            Content: `<pre>${DataLoadedSubsectionHTMLData}</pre>`,
            Parent: Subsection3,
            ChildCls: "Subsection-L0-Data",
            ChildId: `${Subsection3.id}-Data-${DataLoadedSlidesPosition}`,
            DivCls: "Subsection-L0-Data-Wrapper",
            DivId: `${Subsection3.id}-Data-Wrapper-${DataLoadedSlidesPosition}`
        }); */
        
        CreateElement ({
            Tag: "img",
            Parent: Subsection3,
            ChildCls: "Subsection-L0-Data",
            ChildId: `${Subsection3.id}-Data-${DataLoadedSlidesPosition}`,
            DivCls: "Subsection-L0-Data-Wrapper",
            DivId: `${Subsection3.id}-Data-Wrapper-${DataLoadedSlidesPosition}`
        }).setAttribute ("src", XHRURLs2 [DataLoadedSlidesPosition]);
       
    });

    


}
