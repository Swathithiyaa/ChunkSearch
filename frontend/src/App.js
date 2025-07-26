import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/json') {
      setSelectedFile(file);
      setUploadStatus('');
    } else {
      setUploadStatus('Please select a valid JSON file.');
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first.');
      return;
    }

    setIsUploading(true);
    setUploadStatus('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/upload-json', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadStatus('File uploaded successfully!');
      setSelectedFile(null);
      // Reset file input
      document.getElementById('file-input').value = '';
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Error uploading file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      return;
    }

    setIsSearching(true);
    setSearchResults([]);

    try {
      const response = await axios.get('/search', {
        params: {
          query: searchQuery,
          top_k: 50
        }
      });

      setSearchResults(response.data.results || []);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>ChunkSearch</h1>
        <p>Upload JSON files and search through document chunks using BM25 algorithm</p>
      </div>

      {/* File Upload Section */}
      <div className="section">
        <h2>Upload JSON File</h2>
        <div className="form-group">
          <label htmlFor="file-input">Select JSON File:</label>
          <input
            id="file-input"
            type="file"
            accept=".json"
            onChange={handleFileSelect}
            className="form-control"
          />
        </div>
        
        {selectedFile && (
          <div className="form-group">
            <p><strong>Selected file:</strong> {selectedFile.name}</p>
          </div>
        )}

        <button
          className="btn"
          onClick={handleFileUpload}
          disabled={!selectedFile || isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload File'}
        </button>

        {uploadStatus && (
          <div className={uploadStatus.includes('Error') ? 'error' : 'success'}>
            {uploadStatus}
          </div>
        )}
      </div>

      {/* Search Section */}
      <div className="section">
        <h2>Search Chunks</h2>
        <div className="form-group">
          <label htmlFor="search-input">Enter your search query:</label>
          <input
            id="search-input"
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="e.g., ERP, technology, 2025 predictions..."
            className="form-control"
          />
        </div>

        <button
          className="btn"
          onClick={handleSearch}
          disabled={!searchQuery.trim() || isSearching}
        >
          {isSearching ? 'Searching...' : 'Search'}
        </button>

        {/* Search Results */}
        {isSearching && (
          <div className="loading">
            Searching for relevant chunks...
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="search-results">
            <h3>Search Results ({searchResults.length} chunks found)</h3>
            {searchResults.map((result, index) => (
              <div key={index} className="result-item">
                <div className="result-content">
                  {result.content}
                </div>
                <div className="result-metadata">
                  {result.metadata.file_source && (
                    <span className="metadata-item">
                      📄 {result.metadata.file_source}
                    </span>
                  )}
                  {result.metadata.label && (
                    <span className="metadata-item">
                      📍 {result.metadata.label}
                    </span>
                  )}
                  {result.metadata.author && (
                    <span className="metadata-item">
                      👤 {result.metadata.author}
                    </span>
                  )}
                  {result.metadata.category && (
                    <span className="metadata-item">
                      🏷️ {result.metadata.category}
                    </span>
                  )}
                  <span className="result-score">
                    Score: {result.score.toFixed(3)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {!isSearching && searchResults.length === 0 && searchQuery && (
          <div className="loading">
            No relevant chunks found for your query.
          </div>
        )}
      </div>
    </div>
  );
}

export default App; 