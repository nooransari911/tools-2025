import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
	baseURL: API_BASE_URL,
	headers: {
		'Accept': 'application/json',
	},
});

/**
 * Fetches the list of available schema names from the backend.
 * @returns {Promise<string[]>}
 * @throws {Error}
 */
export const fetchSchemas = async () => {
	console.log(`Fetching schemas from ${API_BASE_URL}/schemas`);
	try {
		const response = await apiClient.get('/schemas');
		if (response.data && Array.isArray(response.data.schemas)) {
			return response.data.schemas;
		} else {
			throw new Error("Invalid response format for schemas.");
		}
	} catch (error) {
		console.error("Error fetching schemas:", error.response || error.message);
		const detail = error.response?.data?.detail;
		throw new Error(detail || "Failed to fetch schemas.");
	}
};

/**
 * Sends the document processing request.
 * @param {FormData} formData
 * @returns {Promise<object>}
 * @throws {Error}
 */
export const processDocument = async (formData) => {
	console.log(`Sending processing request to ${API_BASE_URL}/process`);
	try {
		console.log("FormData entries before sending:");
        for (let [key, value] of formData.entries()) {
            if (value instanceof File) {
                console.log(`  ${key}: File(name=${value.name}, size=${value.size}, type=${value.type})`);
            } else {
                console.log(`  ${key}: ${value}`);
            }
        }

		const response = await apiClient.post('/process', formData, {
			// Axios automatically sets 'Content-Type': 'multipart/form-data' for FormData
			// timeout: 600000 // 10 minutes - Consider adding timeout for long processes
		});
		console.log("Processing response received:", response.data);
		return response.data;
	} catch (error) {
		console.error("Error processing document:", error);
		let errorMessage = "An unexpected error occurred during processing.";

		if (error.response) {
			// The request was made and the server responded with a status code
			// that falls out of the range of 2xx
			console.error("Backend Error Status:", error.response.status);
			console.error("Backend Error Data:", error.response.data);
			// Try to extract a meaningful message from FastAPI/Pydantic validation errors
			if (error.response.status === 422 && error.response.data?.detail) {
				try {
                    // FastAPI validation errors are often an array of objects
                    if (Array.isArray(error.response.data.detail)) {
                        errorMessage = error.response.data.detail
                            .map(err => `${err.loc ? err.loc.join(' -> ') : 'field'}: ${err.msg}`)
                            .join('; ');
                    } else if (typeof error.response.data.detail === 'string'){
                        errorMessage = error.response.data.detail;
                    } else {
                         errorMessage = `Validation Error (Code 422): ${JSON.stringify(error.response.data.detail)}`;
                    }
                } catch (parseError) {
                    errorMessage = `Validation Error (Code 422): Could not parse details.`;
                }
			} else {
                // Use error_message or detail if available, otherwise a generic status message
			    errorMessage = error.response.data?.error_message 
                               || error.response.data?.detail 
                               || `Request failed with status ${error.response.status}`;
            }
		} else if (error.request) {
			// The request was made but no response was received
			console.error("No response received:", error.request);
			errorMessage = "No response from server. Check network connection or server status.";
		} else {
			// Something happened in setting up the request that triggered an Error
			console.error('Error setting up request:', error.message);
            errorMessage = error.message;
		}
		throw new Error(errorMessage);
	}
};
