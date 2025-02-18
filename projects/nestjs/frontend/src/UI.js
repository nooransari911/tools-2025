import React from "react";

// Static HTML structure with styles
export default function UI_comp_src_db_test ({ response_json, error, NO_DATA_MESSAGE }) {
    return (
        <div style={{ padding: "20px", fontFamily: "Arial" }}>
        <h1>Test source db</h1>

        <button onClick={response_json}>
        GET Data
        </button>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <pre>
        {response_json ? JSON.stringify(response_json, null, 4) : NO_DATA_MESSAGE}
        </pre>
        </div>
    );
}




export function UI_comp_dest_db_test ({ response_json, error, NO_DATA_MESSAGE }) {
    return (
        <div style={{ padding: "20px", fontFamily: "Arial" }}>
        <h1>Test dest db</h1>

        <button onClick={response_json}>
        GET Data
        </button>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <pre>
        {response_json? JSON.stringify(response_json, null, 4) : NO_DATA_MESSAGE}
        </pre>
        </div>
    );


}
