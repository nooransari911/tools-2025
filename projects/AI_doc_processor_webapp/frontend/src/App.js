import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { fetchSchemas, processDocument } from './services/api';
import ResultsPage from './components/ResultsPage';
import './index.css';

// Uppy imports
import Uppy from '@uppy/core';
import { DragDrop } from '@uppy/react';

function App() {
	return (
		<Routes>
			<Route path="/" element={<MainForm />} />
			<Route path="/results" element={<ResultsPage />} />
		</Routes>
	);
}

// --- Main Form Component ---
function MainForm() {
	const navigate = useNavigate();

	// State variables
	const [prompt, setPrompt] = useState('');
	const [schemas, setSchemas] = useState([]);
	const [selectedSchema, setSelectedSchema] = useState('');
	const [selectedModel, setSelectedModel] = useState('flash');
	const [selectedApiKeyType, setSelectedApiKeyType] = useState('paid');
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState(null);
    const [fileCount, setFileCount] = useState(0);

	// UseRef for Uppy instance
    const uppyRef = useRef(null);
    if (!uppyRef.current) {
        uppyRef.current = new Uppy({
            autoProceed: false,
            debug: false, // Keep false unless debugging uppy
            restrictions: { },
            allowMultipleUploadBatches: true,
        });
        console.log("Uppy instance created.");
    }

    // Update file count when Uppy's file list changes
    useEffect(() => {
        const uppy = uppyRef.current;
        if (!uppy) return;

        const updateCounter = () => {
            setFileCount(uppy.getFiles().length);
        };

        uppy.on('file-added', updateCounter);
        uppy.on('file-removed', updateCounter);
        uppy.on('restored', updateCounter);
        uppy.on('reset', updateCounter);

        updateCounter(); // Initial count

        // Cleanup listeners
        return () => {
            // Only remove listeners if uppy instance still exists
            if (uppyRef.current) {
                 console.log("Cleaning up Uppy listeners...");
                 uppyRef.current.off('file-added', updateCounter);
                 uppyRef.current.off('file-removed', updateCounter);
                 uppyRef.current.off('restored', updateCounter);
                 uppyRef.current.off('reset', updateCounter);
            }
        };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []); // Run only once on mount

    // Close Uppy instance on unmount
    useEffect(() => {
        const uppyInstance = uppyRef.current; // Capture instance for cleanup
        // Return the cleanup function
        return () => {
            if (uppyInstance) {
                console.log("Closing Uppy instance...");
                try {
                    uppyInstance.close({ reason: 'unmount' });
                    // ** REMOVED uppyRef.current = null; **
                } catch (closeError) {
                    // Log error if closing fails, but don't crash
                    console.error("Error closing Uppy instance:", closeError);
                }
            }
        };
    }, []); // Run only once on unmount


	// Fetch schemas on mount (no changes)
	const loadSchemas = useCallback(async () => {
        // ... (same fetch logic as before)
		try {
			const schemaList = await fetchSchemas();
			setSchemas(schemaList || []);
			if (schemaList && schemaList.length > 0) {
				// Set default selected schema only if it's not already set or invalid
                // Ensure '(No Schema - Plain Text)' is handled if present
                const defaultSchema = schemaList.includes('(No Schema - Plain Text)') 
                                      ? '(No Schema - Plain Text)' 
                                      : schemaList[0];
				if (!selectedSchema || !schemaList.includes(selectedSchema)) {
					setSelectedSchema(defaultSchema);
				}
			} else {
                // If no schemas fetched, explicitly set to the plain text option
                setSelectedSchema('(No Schema - Plain Text)');
            }
		} catch (err) {
			setError(`Failed to load schemas: ${err.message}`);
			setSchemas([]);
            setSelectedSchema('(No Schema - Plain Text)'); // Fallback on error
		}
	// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []); // Removed selectedSchema from dependencies to prevent loop if fetch fails

	useEffect(() => {
		loadSchemas();
	}, [loadSchemas]);

    // Handle API Key Type change (no changes)
    const handleApiKeyTypeChange = (event) => {
        setSelectedApiKeyType(event.target.value);
    };

	// Handle form submission (FIXED: navigate *before* uppy.reset)
	const handleSubmit = async (event) => {
		event.preventDefault();
        const uppy = uppyRef.current;
        if (!uppy) return;
        const currentFiles = uppy.getFiles();
		if (currentFiles.length === 0) { setError("Please add files or folders."); return; }
		if (!prompt.trim()) { setError("Please enter a prompt."); return; }
        if (!selectedSchema) { setError("Schema selection is missing. Please wait or refresh."); return; } // Add check
		setIsLoading(true);
		setError(null);
		const formData = new FormData();
		formData.append('prompt', prompt);
		formData.append('schema_name', selectedSchema);
		formData.append('model_type', selectedModel);
		formData.append('api_key_type', selectedApiKeyType);
        currentFiles.forEach(file => { formData.append('files', file.data, file.name); });
		console.log("Submitting FormData...");
		try {
			const response = await processDocument(formData);
			console.log("API call successful, response received:", response); // Add log
			setError(null);
			// Navigate FIRST, then reset Uppy. This prevents potential issues
			// if uppy.reset() somehow interferes with navigation or state updates.
			navigate('/results', { state: { resultData: response } });
			console.log("Navigation triggered to /results");
			uppy.reset();
			console.log("Uppy reset called.");
		} catch (err) {
			 console.error("Form submission -> API error:", err);
			 setError(err.message || "An unexpected error occurred.");
		} finally {
			setIsLoading(false);
			console.log("Finished handleSubmit, isLoading set to false.");
		}
	};

	// JSX for the main form (no changes)
	return (
		<div className="app-container">
			<h1>AI Document Processor</h1>
			{error && !isLoading && <div className="error-message">{error}</div>}
			<form onSubmit={handleSubmit}>
				{/* Uppy Input */}
				<div className="form-group">
					<label htmlFor="uppy-drag-drop">1. Add Documents / Folders</label>
					{uppyRef.current && (
                        <DragDrop id="uppy-drag-drop" uppy={uppyRef.current} locale={{ strings: { dropHereOr: 'Drop files or folders here, or %{browse}', browse: 'browse', } }} note="Files/folders added will be processed." height="200px" width="100%" disabled={isLoading}/>
                    )}
                    <p className='file-count-display'>{fileCount} file(s) added.</p>
				</div>
				{/* Prompt Input */}
				<div className="form-group">
					<label htmlFor="prompt">2. Enter Processing Prompt</label>
					<textarea id="prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="e.g., Summarize..." required disabled={isLoading} rows={4} />
				</div>
				{/* Schema Selector */}
				<div className="form-group">
					<label htmlFor="schema-select">3. Select Output Schema (Optional)</label>
					<select id="schema-select" value={selectedSchema} onChange={(e) => setSelectedSchema(e.target.value)} disabled={isLoading || schemas.length === 0}>
						{schemas.length === 0 && <option value="(No Schema - Plain Text)">Loading / None Available</option>} 
                        {schemas.map((schema) => (<option key={schema} value={schema}>{schema}</option>))}
					</select>
				</div>
				 {/* Model Selector */}
				 <div className="form-group">
					<label>4. Select Model</label>
					<div className="radio-group">
						<label><input type="radio" value="flash" checked={selectedModel === 'flash'} onChange={(e) => setSelectedModel(e.target.value)} disabled={isLoading} /> Flash</label>
						<label><input type="radio" value="pro" checked={selectedModel === 'pro'} onChange={(e) => setSelectedModel(e.target.value)} disabled={isLoading} /> Pro</label>
					</div>
				</div>
                {/* API Key Type Selector */}
                <div className="form-group">
					<label>5. Select API Key Type</label>
					<div className="radio-group">
						<label><input type="radio" value="paid" checked={selectedApiKeyType === 'paid'} onChange={handleApiKeyTypeChange} disabled={isLoading}/> Paid Tier</label>
						<label><input type="radio" value="free" checked={selectedApiKeyType === 'free'} onChange={handleApiKeyTypeChange} disabled={isLoading} /> Free Tier</label>
					</div>
				</div>
				{/* Submit Button */}
				<button type="submit" disabled={isLoading || fileCount === 0}>
					{isLoading ? 'Processing...' : `Process ${fileCount} File(s)`}
				</button>
			</form>
			{isLoading && <div className="loading-message">Processing documents, please wait...</div>}
		</div>
	);
}

export default App;
