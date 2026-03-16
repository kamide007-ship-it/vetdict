#!/usr/bin/env python3
"""
VetDict REST API - FastAPI Implementation
Phase 2.1: Multi-Species Veterinary Disease Database API
"""

import json
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ============================================================================
# Pydantic Models
# ============================================================================

class DiseaseResponse(BaseModel):
    """Disease data model for API responses"""
    id: str
    name: str
    name_ja: Optional[str] = None
    species: str
    description: str
    pathophysiology: Optional[str] = None
    pathophysiology_ja: Optional[str] = None
    transmission: Optional[str] = None
    clinical_signs: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prognosis: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cat_0001",
                "name": "Feline Leukemia Virus (FeLV)",
                "name_ja": "Feline Leukemia Virus (FeLV)(Cat)",
                "species": "Cat",
                "description": "Feline Leukemia Virus (FeLV) in Cat",
                "pathophysiology": "FeLV is a retrovirus..."
            }
        }


class PaginatedResponse(BaseModel):
    """Paginated API response"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[DiseaseResponse]


class SearchResponse(BaseModel):
    """Search results response"""
    query: str
    total_results: int
    results: List[DiseaseResponse]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    total_diseases: int
    species_count: int


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="VetDict API",
    description="Multi-Species Veterinary Disease Database",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Global Data Cache
# ============================================================================

_diseases_data: Optional[List[dict]] = None
_diseases_index: Optional[dict] = None
_species_set: Optional[set] = None


def load_diseases_data() -> List[dict]:
    """Load diseases from JSON file"""
    global _diseases_data
    if _diseases_data is not None:
        return _diseases_data

    data_file = Path(__file__).parent / "diseases_all_species.json"
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    with open(data_file, 'r', encoding='utf-8') as f:
        _diseases_data = json.load(f)

    return _diseases_data


def build_index() -> tuple[dict, set]:
    """Build disease index and species set"""
    global _diseases_index, _species_set
    if _diseases_index is not None:
        return _diseases_index, _species_set

    diseases = load_diseases_data()
    _diseases_index = {d['id']: d for d in diseases}
    _species_set = {d.get('species', 'Unknown') for d in diseases}

    return _diseases_index, _species_set


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    diseases = load_diseases_data()
    index, species = build_index()

    return HealthResponse(
        status="healthy",
        total_diseases=len(diseases),
        species_count=len(species)
    )


@app.get("/api/diseases/search", response_model=SearchResponse, tags=["Diseases"])
async def search_diseases(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Max results"),
    search_type: str = Query("name", pattern="^(name|description|species)$",
                            description="Search field: name, description, or species")
) -> SearchResponse:
    """
    Search diseases by name, description, or species

    - **q**: Search query
    - **limit**: Maximum results (default: 20, max: 100)
    - **search_type**: Field to search - 'name', 'description', or 'species'
    """
    diseases = load_diseases_data()
    query_lower = q.lower()
    results = []

    for disease in diseases:
        if search_type == "name":
            search_field = disease.get('name', '').lower()
            if query_lower in search_field:
                results.append(disease)
        elif search_type == "description":
            search_field = disease.get('description', '').lower()
            if query_lower in search_field:
                results.append(disease)
        elif search_type == "species":
            search_field = disease.get('species', '').lower()
            if query_lower == search_field:
                results.append(disease)

        if len(results) >= limit:
            break

    return SearchResponse(
        query=q,
        total_results=len(results),
        results=[DiseaseResponse(**d) for d in results[:limit]]
    )


@app.get("/api/diseases", response_model=PaginatedResponse, tags=["Diseases"])
async def list_diseases(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    species: Optional[str] = Query(None, description="Filter by species")
) -> PaginatedResponse:
    """
    List all diseases with pagination support

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **species**: Optional species filter (e.g., 'Cat', 'Dog')
    """
    diseases = load_diseases_data()

    # Filter by species if provided
    if species:
        diseases = [d for d in diseases if d.get('species') == species]

    # Calculate pagination
    total = len(diseases)
    total_pages = (total + page_size - 1) // page_size
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    if page > total_pages and total > 0:
        raise HTTPException(
            status_code=404,
            detail=f"Page {page} exceeds total pages {total_pages}"
        )

    paginated_data = diseases[start_idx:end_idx]

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        data=[DiseaseResponse(**d) for d in paginated_data]
    )


@app.get("/api/diseases/{disease_id}", response_model=DiseaseResponse, tags=["Diseases"])
async def get_disease(disease_id: str) -> DiseaseResponse:
    """
    Get a specific disease by ID

    Example ID: 'cat_0001', 'dog_0042', 'horse_0015'
    """
    index, _ = build_index()

    if disease_id not in index:
        raise HTTPException(
            status_code=404,
            detail=f"Disease with ID '{disease_id}' not found"
        )

    disease_data = index[disease_id]
    return DiseaseResponse(**disease_data)


@app.get("/api/species", tags=["Metadata"])
async def list_species() -> JSONResponse:
    """List all available species in database"""
    _, species = build_index()
    sorted_species = sorted(list(species))

    return JSONResponse({
        "total": len(sorted_species),
        "species": sorted_species
    })


@app.get("/api/stats", tags=["Metadata"])
async def get_statistics() -> JSONResponse:
    """Get database statistics"""
    diseases = load_diseases_data()
    index, species = build_index()

    # Count by species
    species_counts = {}
    for disease in diseases:
        sp = disease.get('species', 'Unknown')
        species_counts[sp] = species_counts.get(sp, 0) + 1

    return JSONResponse({
        "total_diseases": len(diseases),
        "total_species": len(species),
        "species_breakdown": species_counts
    })


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with documentation links"""
    return JSONResponse({
        "name": "VetDict REST API",
        "version": "2.1.0",
        "description": "Multi-Species Veterinary Disease Database",
        "documentation": "/api/docs",
        "endpoints": {
            "health": "/api/health",
            "list_diseases": "/api/diseases",
            "get_disease": "/api/diseases/{disease_id}",
            "search_diseases": "/api/diseases/search",
            "list_species": "/api/species",
            "statistics": "/api/stats"
        }
    })


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    try:
        load_diseases_data()
        build_index()
        print(f"✓ Loaded {len(_diseases_data)} diseases into memory")
        print(f"✓ Indexed {len(_diseases_index)} disease records")
    except Exception as e:
        print(f"✗ Failed to load disease data: {e}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
