import React from 'react';
import { JsonViewer } from '@textea/json-viewer';
import './OutputDisplay.css';

const OutputDisplay = ({ result }) => {
	if (!result) {
		return null;
	}

	const {
		status,
		raw_output,
		structured_output,
		schema_used,
		usage_metadata,
		error_message // Can be error OR warning (like failed JSON parse)
	} = result;

	const hasStructuredData = structured_output !== null && structured_output !== undefined;
	const wasStructuredAttempted = schema_used && schema_used !== '(No Schema - Plain Text)';
	const isProcessingError = status === 'error'; // Use status to determine if it was a hard error
	const isParsingWarning = status === 'success' && error_message; // Success but with a post-processing issue

	return (
		<div className="output-container">
			<h2>Processing Result</h2>

			{/* Display hard processing error */}
			{isProcessingError && error_message && (
				<div className="error-message">
					<strong>Processing Error:</strong> {error_message}
				</div>
			)}

            {/* Display parsing/validation warning */}
            {isParsingWarning && error_message && (
				<div className="warning-message"> {/* Style this differently? */} 
					<strong>Note:</strong> {error_message}
				</div>
			)}

			{/* Display Structured Output Section - only if attempted */}
			{wasStructuredAttempted && (
				 <div className="output-section">
					<h3>Structured Output ({schema_used || 'Attempted'})</h3>
					{hasStructuredData ? (
						<JsonViewer
							value={structured_output}
                            theme="vscode" // Example dark theme for json-viewer
                            dark={true}
                            indentWidth={2}
                            collapsed={false}
                            enableClipboard={true}
                            displayDataTypes={false}
                            displayObjectSize={true}
                            style={{ padding: '15px', borderRadius: '5px', backgroundColor: '#1e1e1e' /* Dark background for viewer */ }}
						/>
					) : (
						// Don't show if processing error, error message already covers it
                        // Show only if success but parsing failed (isParsingWarning)
                        isParsingWarning && <p><i>JSON parsing failed. See raw output below.</i></p>
					)}
				</div>
			)}

			{/* Display Raw Output Section - always show if available */}
			{raw_output && (
				<div className="output-section">
					<h3>Raw Output</h3>
					<pre className="raw-output-box">{raw_output}</pre>
				</div>
			)}

			{/* Display Usage Statistics Section - only on success */}
			{usage_metadata && status === 'success' && (
				<div className="output-section usage-stats">
					<h3>Usage Statistics</h3>
					<p><strong>Input Tokens:</strong> {usage_metadata.prompt_token_count?.toLocaleString() ?? 'N/A'}</p>
					<p><strong>Output Tokens:</strong> {usage_metadata.candidates_token_count?.toLocaleString() ?? 'N/A'}</p>
					<p><strong>Total Tokens:</strong> {usage_metadata.total_token_count?.toLocaleString() ?? 'N/A'}</p>
				</div>
			)}

			{/* Fallback message */}
			{status === 'success' && !raw_output && !hasStructuredData && !isParsingWarning && (
				 <p><i>Processing completed successfully, but the model returned no output content.</i></p>
			)}
		</div>
	);
};

export default OutputDisplay;
