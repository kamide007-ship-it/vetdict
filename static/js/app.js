// VetDict Frontend Application
// React-based Veterinary Disease Database UI

const { useState, useEffect, useRef } = React;

// API Configuration
const API_BASE = 'http://localhost:8000/api';

// ============================================================================
// API Service
// ============================================================================

const API = {
    health: () => fetch(`${API_BASE}/health`).then(r => r.json()),
    diseases: (page = 1, pageSize = 10, species = null) => {
        const params = new URLSearchParams({ page, page_size: pageSize });
        if (species) params.append('species', species);
        return fetch(`${API_BASE}/diseases?${params}`).then(r => r.json());
    },
    disease: (id) => fetch(`${API_BASE}/diseases/${id}`).then(r => r.json()),
    search: (query, searchType = 'name', limit = 20) => {
        const params = new URLSearchParams({ q: query, search_type: searchType, limit });
        return fetch(`${API_BASE}/diseases/search?${params}`).then(r => r.json());
    },
    species: () => fetch(`${API_BASE}/species`).then(r => r.json()),
    stats: () => fetch(`${API_BASE}/stats`).then(r => r.json())
};

// ============================================================================
// Components
// ============================================================================

const DiseaseCard = ({ disease, expanded, onToggle }) => {
    const speciesClass = `species-${disease.species.toLowerCase()}`;

    return (
        <div
            className={`disease-card ${expanded ? 'expanded' : ''}`}
            onClick={onToggle}
            role="button"
            tabIndex="0"
        >
            <div className="disease-header">
                <div className="disease-title">
                    <h3>{disease.name}</h3>
                    <div className="id">{disease.id}</div>
                    {disease.name_ja && <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '0.25rem' }}>{disease.name_ja}</div>}
                </div>
                <span className={`disease-badge ${speciesClass}`}>{disease.species}</span>
            </div>

            <div className="disease-details">
                {disease.description && (
                    <div className="detail-section">
                        <h4>Description</h4>
                        <p>{disease.description}</p>
                    </div>
                )}

                {disease.pathophysiology && (
                    <div className="detail-section">
                        <h4>Pathophysiology</h4>
                        <p>{disease.pathophysiology}</p>
                    </div>
                )}

                {disease.treatment && (
                    <div className="detail-section">
                        <h4>Treatment</h4>
                        <p>{disease.treatment}</p>
                    </div>
                )}

                {disease.diagnosis && (
                    <div className="detail-section">
                        <h4>Diagnosis</h4>
                        <p>{disease.diagnosis}</p>
                    </div>
                )}

                {disease.clinical_signs && (
                    <div className="detail-section">
                        <h4>Clinical Signs</h4>
                        <p>{disease.clinical_signs}</p>
                    </div>
                )}

                {disease.transmission && (
                    <div className="detail-section">
                        <h4>Transmission</h4>
                        <p>{disease.transmission}</p>
                    </div>
                )}

                {disease.prognosis && (
                    <div className="detail-section">
                        <h4>Prognosis</h4>
                        <p>{disease.prognosis}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

const StatCard = ({ title, value }) => (
    <div className="stat-card">
        <h3>{value}</h3>
        <p>{title}</p>
    </div>
);

const PaginationControls = ({ current, total, onPageChange }) => {
    if (total <= 1) return null;

    const pages = [];
    const start = Math.max(1, current - 2);
    const end = Math.min(total, current + 2);

    if (start > 1) {
        pages.push(<button key="first" onClick={() => onPageChange(1)}>First</button>);
        if (start > 2) pages.push(<span key="dots1">...</span>);
    }

    for (let i = start; i <= end; i++) {
        pages.push(
            <button
                key={i}
                className={i === current ? 'active' : ''}
                onClick={() => onPageChange(i)}
            >
                {i}
            </button>
        );
    }

    if (end < total) {
        if (end < total - 1) pages.push(<span key="dots2">...</span>);
        pages.push(<button key="last" onClick={() => onPageChange(total)}>Last</button>);
    }

    return (
        <div className="pagination">
            <button
                onClick={() => onPageChange(current - 1)}
                disabled={current === 1}
            >
                ← Prev
            </button>
            {pages}
            <button
                onClick={() => onPageChange(current + 1)}
                disabled={current === total}
            >
                Next →
            </button>
        </div>
    );
};

// ============================================================================
// Main Application
// ============================================================================

const VetDictApp = () => {
    // State
    const [tab, setTab] = useState('browse'); // 'browse' or 'search'
    const [diseases, setDiseases] = useState([]);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [expandedId, setExpandedId] = useState(null);

    // Browse tab state
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);
    const [selectedSpecies, setSelectedSpecies] = useState(null);
    const [species, setSpecies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);

    // Search tab state
    const [searchQuery, setSearchQuery] = useState('');
    const [searchType, setSearchType] = useState('name');
    const [searchResults, setSearchResults] = useState([]);
    const [searchLoaded, setSearchLoaded] = useState(false);

    // Load initial data
    useEffect(() => {
        loadStats();
        loadSpecies();
        if (tab === 'browse') {
            loadDiseases();
        }
    }, []);

    // Load stats
    const loadStats = async () => {
        try {
            const data = await API.stats();
            setStats(data);
        } catch (err) {
            console.error('Error loading stats:', err);
        }
    };

    // Load species list
    const loadSpecies = async () => {
        try {
            const data = await API.species();
            setSpecies(data.species);
        } catch (err) {
            console.error('Error loading species:', err);
        }
    };

    // Load diseases
    const loadDiseases = async (p = 1, s = null) => {
        setLoading(true);
        setError(null);
        try {
            const data = await API.diseases(p, pageSize, s);
            setDiseases(data.data);
            setTotalPages(data.total_pages);
            setPage(p);
        } catch (err) {
            setError('Failed to load diseases. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // Handle species filter
    const handleSpeciesFilter = (sp) => {
        const newSpecies = selectedSpecies === sp ? null : sp;
        setSelectedSpecies(newSpecies);
        setPage(1);
        loadDiseases(1, newSpecies);
    };

    // Handle search
    const handleSearch = async (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) {
            setSearchResults([]);
            setSearchLoaded(false);
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const data = await API.search(searchQuery, searchType, 50);
            setSearchResults(data.results);
            setSearchLoaded(true);
        } catch (err) {
            setError('Search failed. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // Handle page change
    const handlePageChange = (newPage) => {
        loadDiseases(newPage, selectedSpecies);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <>
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <h1>🐾 VetDict</h1>
                    <p>Multi-Species Veterinary Disease Database</p>
                </div>
            </header>

            {/* Main Content */}
            <div className="container">
                {/* Stats */}
                {stats && (
                    <div className="stats-grid">
                        <StatCard title="Total Diseases" value={stats.total_diseases} />
                        <StatCard title="Species" value={stats.total_species} />
                        <StatCard title="Cat Diseases" value={stats.species_breakdown.Cat || 0} />
                        <StatCard title="Horse Diseases" value={stats.species_breakdown.Horse || 0} />
                    </div>
                )}

                {/* Tabs */}
                <div className="tabs">
                    <button
                        className={`tab-button ${tab === 'browse' ? 'active' : ''}`}
                        onClick={() => {
                            setTab('browse');
                            setExpandedId(null);
                        }}
                    >
                        📚 Browse
                    </button>
                    <button
                        className={`tab-button ${tab === 'search' ? 'active' : ''}`}
                        onClick={() => {
                            setTab('search');
                            setExpandedId(null);
                        }}
                    >
                        🔍 Search
                    </button>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="error-message">
                        <strong>Error</strong>
                        {error}
                    </div>
                )}

                {/* Browse Tab */}
                {tab === 'browse' && (
                    <>
                        {/* Filters */}
                        <div className="search-section">
                            <div className="search-container">
                                <div className="search-group">
                                    <label>Filter by Species</label>
                                    <select
                                        value={selectedSpecies || ''}
                                        onChange={(e) => handleSpeciesFilter(e.target.value || null)}
                                    >
                                        <option value="">All Species</option>
                                        {species.map(sp => (
                                            <option key={sp} value={sp}>{sp}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="search-group">
                                    <label>Items per Page</label>
                                    <select
                                        value={pageSize}
                                        onChange={(e) => {
                                            setPageSize(parseInt(e.target.value));
                                            setPage(1);
                                        }}
                                    >
                                        <option value={10}>10</option>
                                        <option value={20}>20</option>
                                        <option value={50}>50</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        {/* Diseases List */}
                        {loading ? (
                            <div className="loading">
                                <div className="spinner"></div>
                                <p>Loading diseases...</p>
                            </div>
                        ) : diseases.length > 0 ? (
                            <>
                                <div className="disease-list">
                                    {diseases.map(disease => (
                                        <DiseaseCard
                                            key={disease.id}
                                            disease={disease}
                                            expanded={expandedId === disease.id}
                                            onToggle={() => setExpandedId(
                                                expandedId === disease.id ? null : disease.id
                                            )}
                                        />
                                    ))}
                                </div>
                                <PaginationControls
                                    current={page}
                                    total={totalPages}
                                    onPageChange={handlePageChange}
                                />
                            </>
                        ) : (
                            <div className="empty-state">
                                <h3>No diseases found</h3>
                                <p>Try selecting a different species filter</p>
                            </div>
                        )}
                    </>
                )}

                {/* Search Tab */}
                {tab === 'search' && (
                    <>
                        {/* Search Form */}
                        <div className="search-section">
                            <form onSubmit={handleSearch}>
                                <div className="search-container">
                                    <div className="search-group" style={{ flex: 2 }}>
                                        <label>Search Query</label>
                                        <input
                                            type="text"
                                            placeholder="e.g., diabetes, feline, infection..."
                                            value={searchQuery}
                                            onChange={(e) => setSearchQuery(e.target.value)}
                                        />
                                    </div>
                                    <div className="search-group">
                                        <label>Search In</label>
                                        <select
                                            value={searchType}
                                            onChange={(e) => setSearchType(e.target.value)}
                                        >
                                            <option value="name">Disease Name</option>
                                            <option value="description">Description</option>
                                            <option value="species">Species</option>
                                        </select>
                                    </div>
                                    <button type="submit" className="btn-primary">
                                        Search
                                    </button>
                                </div>
                            </form>
                        </div>

                        {/* Search Results */}
                        {loading ? (
                            <div className="loading">
                                <div className="spinner"></div>
                                <p>Searching...</p>
                            </div>
                        ) : searchLoaded ? (
                            searchResults.length > 0 ? (
                                <div className="disease-list">
                                    {searchResults.map(disease => (
                                        <DiseaseCard
                                            key={disease.id}
                                            disease={disease}
                                            expanded={expandedId === disease.id}
                                            onToggle={() => setExpandedId(
                                                expandedId === disease.id ? null : disease.id
                                            )}
                                        />
                                    ))}
                                </div>
                            ) : (
                                <div className="empty-state">
                                    <h3>No results found</h3>
                                    <p>Try different keywords or search type</p>
                                </div>
                            )
                        ) : (
                            <div className="empty-state">
                                <h3>Start searching</h3>
                                <p>Enter a query above to find diseases</p>
                            </div>
                        )}
                    </>
                )}
            </div>
        </>
    );
};

// ============================================================================
// Render
// ============================================================================

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<VetDictApp />);
