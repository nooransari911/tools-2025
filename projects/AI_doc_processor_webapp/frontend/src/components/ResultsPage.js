import React, { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { JsonViewer } from '@textea/json-viewer';
import './ResultsPage.css';

// --- JSDoc type definitions for clarity (optional but helpful) --- 
/**
 * @typedef {object} SingleFileResult
 * @property {string} file_name
 * @property {'success' | 'error'} status
 * @property {string | null | undefined} raw_output
 * @property {any | null | undefined} structured_output
 * @property {string | null | undefined} error_message
 */

/**
 * @typedef {object} UsageMetadata
 * @property {number | null | undefined} prompt_token_count
 * @property {number | null | undefined} candidates_token_count
 * @property {number | null | undefined} total_token_count
 */

/**
 * @typedef {object} ResultsData
 * @property {'success' | 'error' | 'partial_success'} status
 * @property {string | null | undefined} overall_error_message
 * @property {SingleFileResult[]} results
 * @property {string | null | undefined} schema_used
 * @property {UsageMetadata | null | undefined} overall_usage_metadata
 */

/**
 * Default empty state matching the ResultsData structure
 * @type {ResultsData}
 */
const defaultResultsData = {
	status: 'error',
	overall_error_message: 'No result data found or invalid format. Please go back and process documents.',
	results: [],
	schema_used: null,
	overall_usage_metadata: null
};

function ResultsPage() {
	const location = useLocation();

	/** @type {ResultsData} */
	const result = location.state?.resultData && Array.isArray(location.state.resultData.results)
		? location.state.resultData
		: defaultResultsData;

	const {
		status: overallStatus,
		overall_error_message,
		results,
		schema_used,
		overall_usage_metadata
	} = result;

    /** @type {[Record<string, string>, React.Dispatch<React.SetStateAction<Record<string, string>>>]} */
	const [copyStatus, setCopyStatus] = useState({}); // { [key: string]: 'Copy' | 'Copied!' | 'Failed' }

    // Generic copy function (no type annotations needed for parameters)
    const copyToClipboard = (text, type, index) => {
		const key = `${type}-${index}`;
        // Initialize button state immediately
        setCopyStatus(prev => ({ ...prev, [key]: 'Copying...' })); 

		if (!navigator.clipboard || !text) {
            console.error('Clipboard API not available or text is empty.');
            setCopyStatus(prev => ({ ...prev, [key]: 'Copy Failed' }));
            setTimeout(() => setCopyStatus(prev => ({ ...prev, [key]: prev[key] === 'Copy Failed' ? 'Copy' : prev[key] })), 2000); // Reset only if still 'Failed'
            return;
        }

        navigator.clipboard.writeText(text).then(() => {
            setCopyStatus(prev => ({ ...prev, [key]: 'Copied!' }));
            setTimeout(() => setCopyStatus(prev => ({ ...prev, [key]: prev[key] === 'Copied!' ? 'Copy' : prev[key] })), 1500); // Reset only if still 'Copied!'
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            setCopyStatus(prev => ({ ...prev, [key]: 'Copy Failed' }));
            setTimeout(() => setCopyStatus(prev => ({ ...prev, [key]: prev[key] === 'Copy Failed' ? 'Copy' : prev[key] })), 2000); // Reset only if still 'Failed'
        });
    };

	// RETURN STATEMENT STARTS HERE - NO TYPE ANNOTATIONS BEFORE THIS
	return (
		<div className="results-page-container">
			<h1>Processing Results</h1>

			<div className="back-link-container">
				<Link to="/">← Process More Documents</Link>
			</div>

			{/* Display overall error/status messages */}
			{overallStatus === 'error' && overall_error_message && (
				<div className="error-message full-width-message">
					<strong>Error:</strong> {overall_error_message}
				</div>
			)}
            {overallStatus === 'partial_success' && (
				<div className="warning-message full-width-message">
					<strong>Note:</strong> Some files encountered errors during processing.
				</div>
			)}
            {(overallStatus === 'success' || overallStatus === 'partial_success') && (!results || results.length === 0) && !overall_error_message && (
                <div className="info-message full-width-message">
                    Processing completed, but no valid files were found or processed.
                </div>
            )}

			{/* --- Loop through results for each file --- */ } 
			<div className="results-content-area">
                {results && results.length > 0 && results.map((fileResult, index) => {
                    const jsonCopyKey = `json-${index}`;
                    const rawCopyKey = `raw-${index}`;
                    // Provide default 'Copy' status if key doesn't exist yet
                    const currentJsonCopyText = copyStatus[jsonCopyKey] || 'Copy JSON';
                    const currentRawCopyText = copyStatus[rawCopyKey] || 'Copy Raw Text';
                    const isJsonCopying = currentJsonCopyText !== 'Copy JSON';
                    const isRawCopying = currentRawCopyText !== 'Copy Raw Text';

                    const isFileError = fileResult.status === 'error';
                    const isJsonParseWarning = fileResult.status === 'success' && fileResult.error_message && fileResult.structured_output === null;

                    let rawTitle = "Response";
                    if (isJsonParseWarning) {
                        rawTitle = "Raw Output (JSON Parsing Failed)";
                    } else if (!fileResult.structured_output && fileResult.raw_output) {
                        rawTitle = "Response";
                    } else if (fileResult.structured_output && fileResult.raw_output) {
                        rawTitle = "Raw Output (Fallback)";
                    }

                    return (
                        <section key={index} className={`result-section file-result-section ${isFileError ? 'file-error-section' : ''}`}>
                            <h2 className="file-result-header">File: {fileResult.file_name || `Item ${index + 1}`}</h2>

                            {isFileError && fileResult.error_message && (
                                <div className="error-message file-error-message">
                                    <strong>Error:</strong> {fileResult.error_message}
                                </div>
                            )}
                             {isJsonParseWarning && fileResult.error_message && (
                                <div className="warning-message file-error-message">
                                    <strong>Note:</strong> {fileResult.error_message}
                                </div>
                            )}

                            {/* Structured Output for this file */}
                            {fileResult.structured_output && (
                                <div className="sub-result-section">
                                    <header className="section-header">
                                        <h3>Structured Output ({schema_used || 'N/A'})</h3>
                                        <button
                                            onClick={() => copyToClipboard(JSON.stringify(fileResult.structured_output, null, 2), 'json', index)}
                                            className={`copy-button ${isJsonCopying && currentJsonCopyText !== 'Copy Failed' ? 'copied' : ''}`}
                                            disabled={isJsonCopying}
                                        >
                                            {currentJsonCopyText}
                                        </button>
                                    </header>
                                    <div className="json-viewer-wrapper">
                                        <JsonViewer
                                            value={fileResult.structured_output}
                                            theme="vscode" dark={true} indentWidth={2}
                                            collapsed={false} enableClipboard={false}
                                            displayDataTypes={false} displayObjectSize={true}
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Raw Output for this file */}
                            {fileResult.raw_output && (
                                <div className="sub-result-section">
                                    <header className="section-header">
                                        <h3>{rawTitle}</h3>
                                         <button
                                            onClick={() => copyToClipboard(fileResult.raw_output, 'raw', index)}
                                            className={`copy-button ${isRawCopying && currentRawCopyText !== 'Copy Failed' ? 'copied' : ''}`}
                                            disabled={isRawCopying}
                                        >
                                            {currentRawCopyText}
                                        </button>
                                    </header>
                                    {!fileResult.structured_output ? (
                                        <div className="markdown-content-wrapper">
                                            {/* Added className for potential styling */}
                                            <ReactMarkdown remarkPlugins={[remarkGfm]} className="markdown-content">{fileResult.raw_output}</ReactMarkdown>
                                        </div>
                                    ) : (
                                        <pre className="raw-output-box-results">{fileResult.raw_output}</pre>
                                    )}
                                </div>
                            )}

                             {fileResult.status === 'success' && !fileResult.raw_output && !fileResult.structured_output && (
                                 <p><i>No output content generated for this file.</i></p>
                             )}
                        </section>
                    )
                })}

				{/* --- Overall Usage Statistics --- */ } 
				{overall_usage_metadata && (overallStatus === 'success' || overallStatus === 'partial_success') && (
					<section className="result-section usage-stats-results overall-usage">
						<h3>Overall Usage Statistics</h3>
						<p><strong>Total Input Tokens:</strong> {overall_usage_metadata.prompt_token_count?.toLocaleString() ?? 'N/A'}</p>
						<p><strong>Total Output Tokens:</strong> {overall_usage_metadata.candidates_token_count?.toLocaleString() ?? 'N/A'}</p>
						<p><strong>Grand Total Tokens:</strong> {overall_usage_metadata.total_token_count?.toLocaleString() ?? 'N/A'}</p>
					</section>
				)}

			</div>
		</div>
	);
}

export default ResultsPage;
