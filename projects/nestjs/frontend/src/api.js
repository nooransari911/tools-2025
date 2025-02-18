import { API_URL, API_URL_DEST_BASE, API_URL_GET_USER, API_URL_HELLO } from "./constants";

export async function FetchData (url = API_URL_HELLO) {

    try {
        let response = await fetch(url);

        if (!response.ok)
            throw new Error(`HTTP error! Status: ${response.status}`);

        return response.json();

    }
    
    catch (error) {
        return { error: error.message };
    }
}



export async function src_db_test_json () {
    return FetchData (`${API_URL_GET_USER}0`);
};



export async function dest_db_test_json () {
    return FetchData (`${API_URL_DEST_BASE}0`);
};


