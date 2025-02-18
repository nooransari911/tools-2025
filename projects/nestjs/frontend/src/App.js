import React, { useEffect, useState } from "react";
import { dest_db_test_json, FetchData, src_db_test_json } from "./api";
import { API_URL_GET_USER, API_URL_HELLO, NO_DATA_MESSAGE } from "./constants";
import UI_comp_src_db_test, { UI_comp_dest_db_test } from "./UI";


function App() {
    const [srcData, setSrcData] = useState(null);
    const [srcError, setSrcError] = useState(null);
    const [destData, setDestData] = useState(null);
    const [destError, setDestError] = useState(null);
    const [loading, setLoading] = useState(false); // Add a loading state
    // useEffect (() => {
    //     async function fetchData () {
    //         const srcResult = src_db_test_json;  // Call the function from api.js
    //         if (srcResult.error) {
    //             setSrcError(srcResult.error);
    //             setSrcData(null);
    //         }
    //         else {
    //             setSrcData(srcResult);
    //             setSrcError(null);
    //         }

    //         const destResult = dest_db_test_json; // Call the function from api.js
    //         if (destResult.error) {
    //             setDestError(destResult.error);
    //             setDestData(null);
    //         } else {
    //             setDestData(destResult);
    //             setDestError(null);
    //         }
    //     };

    //     fetchData();

    // }, []);



      // Function to fetch src data, called by the onClick handler
    const fetchSrcData = async () => {
        setLoading(true); // Set loading to true before the fetch
        setSrcError(null);  // Clear previous errors
        setSrcData(null)
        try {
            const srcResult = await src_db_test_json();
            if (srcResult.error) {
                setSrcError(srcResult.error);
            } else {
                setSrcData(srcResult);
            }
        } finally {
            setLoading(false); // Set loading to false after fetch (success or failure)
        }
    };

    // Function to fetch dest data, called by the onClick handler
    const fetchDestData = async () => {
        setLoading(true);
        setDestError(null);
        setDestData(null);
        try{
            const destResult = await dest_db_test_json();
            if (destResult.error) {
                setDestError(destResult.error);
            } else {
                setDestData(destResult);
            }
        } finally {
            setLoading(false)
        }
    };



  return (
    <>
      <button onClick={fetchSrcData} disabled={loading}>
        {loading ? "Loading..." : "Fetch Source Data"}
      </button>
      <UI_comp_src_db_test
        response_json={srcData}
        data={srcData}
        error={srcError}
        NO_DATA_MESSAGE={NO_DATA_MESSAGE}
      />
      <br /><br />
      <button onClick={fetchDestData} disabled={loading}>
        {loading ? "Loading..." : "Fetch Destination Data"}
      </button>
      <UI_comp_dest_db_test
        response_json={destData}
        data={destData}
        error={destError}
        NO_DATA_MESSAGE={NO_DATA_MESSAGE}
      />
      <br /><br />
        {loading && <p>Loading data...</p>} {/* Display loading message */}
    </>
  );


}


export default App;
