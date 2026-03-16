#!/usr/bin/env python3
"""
VetDict REST API - FastAPI Implementation
Phase 2.1: Multi-Species Veterinary Disease Database API
"""

import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field

# ============================================================================
# Pydantic Models
# ============================================================================

class DiseaseResponse(BaseModel):
    """Disease data model for API responses"""
    id: str = Field(..., description="Unique disease identifier (e.g., 'cat_0001')")
    name: str = Field(..., description="Disease name in English")
    name_ja: Optional[str] = Field(None, description="Disease name in Japanese")
    species: str = Field(..., description="Target species (Cat, Dog, Horse, etc.)")
    description: str = Field(..., description="Disease description and overview")
    pathophysiology: Optional[str] = Field(None, description="Disease pathophysiology mechanism")
    pathophysiology_ja: Optional[str] = Field(None, description="Pathophysiology in Japanese")
    transmission: Optional[str] = Field(None, description="Disease transmission methods")
    clinical_signs: Optional[str] = Field(None, description="Clinical signs and symptoms")
    diagnosis: Optional[str] = Field(None, description="Diagnostic procedures and tests")
    treatment: Optional[str] = Field(None, description="Treatment options and protocols")
    prognosis: Optional[str] = Field(None, description="Disease prognosis and outcome")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cat_0001",
                "name": "Feline Leukemia Virus (FeLV)",
                "name_ja": "Feline Leukemia Virus (FeLV)",
                "species": "Cat",
                "description": "FeLV is a retrovirus that affects feline immune system...",
                "pathophysiology": "FeLV integrates into host genome...",
                "transmission": "Primarily through saliva contact, bites, shared food bowls",
                "clinical_signs": "Lethargy, fever, decreased appetite, pale mucous membranes",
                "diagnosis": "ELISA test, Western blot, IFA test",
                "treatment": "Supportive care, antiretroviral therapy, management of secondary infections",
                "prognosis": "Guarded to poor, median survival 2-3 years after diagnosis"
            }
        }


class PaginatedResponse(BaseModel):
    """Paginated API response with pagination metadata"""
    total: int = Field(..., description="Total number of items in database")
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    data: List[DiseaseResponse] = Field(..., description="List of diseases for current page")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 4230,
                "page": 1,
                "page_size": 10,
                "total_pages": 423,
                "data": []
            }
        }


class SearchResponse(BaseModel):
    """Search results response"""
    query: str = Field(..., description="The search query string")
    total_results: int = Field(..., description="Number of results found")
    results: List[DiseaseResponse] = Field(..., description="Matching disease records")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "diabetes",
                "total_results": 5,
                "results": []
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status (healthy/degraded/unhealthy)")
    total_diseases: int = Field(..., description="Total number of diseases in database")
    species_count: int = Field(..., description="Number of unique species")
    timestamp: str = Field(..., description="Health check timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "total_diseases": 4230,
                "species_count": 6,
                "timestamp": "2024-03-16T12:34:56Z"
            }
        }


class StatsResponse(BaseModel):
    """Database statistics response"""
    total_diseases: int = Field(..., description="Total number of disease records")
    total_species: int = Field(..., description="Number of unique animal species")
    species_breakdown: dict = Field(..., description="Disease count per species")
    timestamp: str = Field(..., description="Statistics update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "total_diseases": 4230,
                "total_species": 6,
                "species_breakdown": {
                    "Cat": 1200,
                    "Dog": 850,
                    "Horse": 650,
                    "Bird": 750,
                    "Rabbit": 430,
                    "Parakeet": 350
                },
                "timestamp": "2024-03-16T12:34:56Z"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error type/code")
    detail: str = Field(..., description="Detailed error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: str = Field(..., description="Error occurrence timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "NOT_FOUND",
                "detail": "Disease with ID 'cat_9999' not found",
                "status_code": 404,
                "timestamp": "2024-03-16T12:34:56Z"
            }
        }


class SpeciesResponse(BaseModel):
    """Species list response"""
    total: int = Field(..., description="Number of species")
    species: List[str] = Field(..., description="List of available species")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 6,
                "species": ["Bird", "Cat", "Dog", "Horse", "Parakeet", "Rabbit"]
            }
        }


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="VetDict REST API",
    description="""
# VetDict - Multi-Species Veterinary Disease Database API

A comprehensive REST API for accessing veterinary disease information across multiple animal species.

## Features

- **Paginated Disease Listing**: Browse diseases with customizable pagination
- **Full-Text Search**: Search diseases by name, description, or species
- **Disease Details**: Access comprehensive information including pathophysiology, transmission, diagnosis, and treatment
- **Statistics**: Get database statistics and species breakdown
- **Bilingual Content**: Support for English and Japanese disease names

## Species Supported

- Cat (Feline)
- Dog (Canine)
- Horse (Equine)
- Bird (Avian)
- Rabbit (Lagomorph)
- Parakeet (Psittacine)

## Authentication

Currently, this API is open without authentication. Future versions may include API key authentication.

## Rate Limiting

No rate limiting is currently enforced. Please use responsibly.

## Data Format

All responses are in JSON format with consistent schema structure.
""",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "VetDict API Support",
        "url": "https://github.com/kamide007/vetdict",
        "email": "support@vetdict.local"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
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

@app.get(
    "/api/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is degraded or unhealthy"}
    }
)
async def health_check() -> HealthResponse:
    """
    Check the health status of the VetDict API service.

    Returns:
    - **status**: Current service status (healthy/degraded/unhealthy)
    - **total_diseases**: Count of all diseases in database
    - **species_count**: Number of unique species
    - **timestamp**: Health check timestamp
    """
    diseases = load_diseases_data()
    index, species = build_index()

    return HealthResponse(
        status="healthy",
        total_diseases=len(diseases),
        species_count=len(species),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get(
    "/api/diseases/search",
    response_model=SearchResponse,
    tags=["Diseases"],
    summary="Search Diseases",
    responses={
        200: {"description": "Successfully retrieved search results"},
        400: {"description": "Invalid search parameters"}
    }
)
async def search_diseases(
    q: str = Query(..., min_length=1, description="Search query (case-insensitive)", example="diabetes"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results (max 100)", example=20),
    search_type: str = Query(
        "name",
        pattern="^(name|description|species)$",
        description="Search field: 'name' (disease name), 'description' (description text), or 'species' (animal species)",
        example="name"
    )
) -> SearchResponse:
    """
    Search diseases using full-text search across multiple fields.

    ### Query Parameters:
    - **q**: The search query string (case-insensitive)
    - **limit**: Maximum number of results to return (default: 20, max: 100)
    - **search_type**: Which field to search:
      - `name`: Search in disease names
      - `description`: Search in disease descriptions
      - `species`: Search for specific species (exact match)

    ### Returns:
    Search response with matching disease records and result count.

    ### Examples:
    - `/api/diseases/search?q=diabetes` - Search for diseases containing "diabetes"
    - `/api/diseases/search?q=feline&limit=50` - Search with custom limit
    - `/api/diseases/search?q=Cat&search_type=species` - Find all Cat diseases
    - `/api/diseases/search?q=infection&search_type=description` - Search descriptions

    ### Search Behavior:
    - Search is case-insensitive
    - For 'name' and 'description' types: substring matching
    - For 'species' type: exact match with species name
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


@app.get(
    "/api/diseases",
    response_model=PaginatedResponse,
    tags=["Diseases"],
    summary="List Diseases",
    responses={
        200: {"description": "Successfully retrieved disease list"},
        400: {"description": "Invalid query parameters"},
        404: {"description": "Page exceeds total pages"}
    }
)
async def list_diseases(
    page: int = Query(1, ge=1, description="Page number (1-indexed)", example=1),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)", example=20),
    species: Optional[str] = Query(None, description="Filter by species (e.g., 'Cat', 'Dog')", example="Cat")
) -> PaginatedResponse:
    """
    List all diseases with pagination and optional filtering.

    ### Query Parameters:
    - **page**: Page number starting from 1 (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **species**: Optional filter by species name

    ### Returns:
    Paginated response with disease records and pagination metadata.

    ### Examples:
    - `/api/diseases` - First page with 20 items
    - `/api/diseases?page=2&page_size=50` - Second page with 50 items
    - `/api/diseases?species=Cat` - All cat diseases
    - `/api/diseases?species=Horse&page=2&page_size=10` - Page 2 of horse diseases
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


@app.get(
    "/api/diseases/{disease_id}",
    response_model=DiseaseResponse,
    tags=["Diseases"],
    summary="Get Disease Details",
    responses={
        200: {"description": "Disease found and returned"},
        404: {"description": "Disease not found"}
    }
)
async def get_disease(
    disease_id: str = Query(..., description="Unique disease identifier", example="cat_0001")
) -> DiseaseResponse:
    """
    Retrieve comprehensive information about a specific disease.

    ### Path Parameters:
    - **disease_id**: The unique identifier of the disease

    ### Disease ID Format:
    Disease IDs follow the pattern: `{species_code}_{number}`
    - `cat_0001` - Cat disease #0001
    - `dog_0042` - Dog disease #0042
    - `horse_0015` - Horse disease #0015
    - `bird_0100` - Bird disease #0100
    - `rabbit_0050` - Rabbit disease #0050
    - `parakeet_0075` - Parakeet disease #0075

    ### Returns:
    Complete disease information including:
    - Basic info (name, species)
    - Pathophysiology and transmission
    - Clinical signs and diagnosis methods
    - Treatment options and prognosis
    - Japanese translations where available

    ### Examples:
    - `/api/diseases/cat_0001` - Get feline leukemia virus
    - `/api/diseases/horse_0100` - Get specific horse disease
    """
    index, _ = build_index()

    if disease_id not in index:
        raise HTTPException(
            status_code=404,
            detail=f"Disease with ID '{disease_id}' not found"
        )

    disease_data = index[disease_id]
    return DiseaseResponse(**disease_data)


@app.get(
    "/api/species",
    response_model=SpeciesResponse,
    tags=["Metadata"],
    summary="List Species",
    responses={
        200: {"description": "Successfully retrieved species list"}
    }
)
async def list_species() -> SpeciesResponse:
    """
    Get list of all available animal species in the database.

    ### Returns:
    - **total**: Number of unique species
    - **species**: Alphabetically sorted list of species names

    ### Available Species:
    The database currently includes diseases for:
    - **Bird** (Avian) - General bird diseases
    - **Cat** (Feline) - Domestic cat diseases
    - **Dog** (Canine) - Domestic dog diseases
    - **Horse** (Equine) - Horse and equine diseases
    - **Parakeet** (Psittacine) - Parakeet and parrot diseases
    - **Rabbit** (Lagomorph) - Rabbit diseases

    ### Usage:
    Use species names from this list to filter results in the diseases endpoint.
    """
    _, species = build_index()
    sorted_species = sorted(list(species))

    return SpeciesResponse(
        total=len(sorted_species),
        species=sorted_species
    )


@app.get(
    "/api/stats",
    response_model=StatsResponse,
    tags=["Metadata"],
    summary="Database Statistics",
    responses={
        200: {"description": "Successfully retrieved statistics"}
    }
)
async def get_statistics() -> StatsResponse:
    """
    Get comprehensive database statistics.

    ### Returns:
    - **total_diseases**: Total number of disease records in database
    - **total_species**: Number of unique animal species
    - **species_breakdown**: Disease count for each species
    - **timestamp**: When statistics were generated

    ### Statistics:
    This endpoint provides insights into database coverage across different species.

    ### Use Cases:
    - Monitor database growth
    - Understand disease coverage per species
    - Plan content expansion
    - Generate reports
    """
    diseases = load_diseases_data()
    index, species = build_index()

    # Count by species
    species_counts = {}
    for disease in diseases:
        sp = disease.get('species', 'Unknown')
        species_counts[sp] = species_counts.get(sp, 0) + 1

    return StatsResponse(
        total_diseases=len(diseases),
        total_species=len(species),
        species_breakdown=species_counts,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    responses={
        200: {"description": "API information and endpoints"}
    }
)
async def root():
    """
    VetDict API root endpoint.

    Provides API information and links to available endpoints.

    ### Getting Started:
    1. Read the [full API documentation](/api/docs)
    2. Check [ReDoc documentation](/api/redoc)
    3. Try the endpoints below

    ### Main Endpoints:
    - **Health**: `/api/health` - Service status
    - **Diseases**: `/api/diseases` - List and browse diseases
    - **Search**: `/api/diseases/search` - Full-text search
    - **Detail**: `/api/diseases/{id}` - Get disease details
    - **Species**: `/api/species` - Available species list
    - **Stats**: `/api/stats` - Database statistics
    """
    return JSONResponse({
        "name": "VetDict REST API",
        "version": "2.1.0",
        "description": "Multi-Species Veterinary Disease Database",
        "status": "operational",
        "documentation": {
            "swagger": "/api/docs",
            "redoc": "/api/redoc",
            "openapi": "/api/openapi.json"
        },
        "endpoints": {
            "health": {
                "method": "GET",
                "url": "/api/health",
                "description": "Service health check"
            },
            "list_diseases": {
                "method": "GET",
                "url": "/api/diseases",
                "description": "List all diseases with pagination"
            },
            "search_diseases": {
                "method": "GET",
                "url": "/api/diseases/search",
                "description": "Search diseases by name, description, or species"
            },
            "get_disease": {
                "method": "GET",
                "url": "/api/diseases/{disease_id}",
                "description": "Get specific disease details"
            },
            "list_species": {
                "method": "GET",
                "url": "/api/species",
                "description": "Get list of available species"
            },
            "statistics": {
                "method": "GET",
                "url": "/api/stats",
                "description": "Get database statistics"
            }
        },
        "examples": {
            "browse_diseases": "/api/diseases?page=1&page_size=20",
            "search": "/api/diseases/search?q=diabetes&limit=10",
            "filter_by_species": "/api/diseases?species=Cat",
            "get_specific_disease": "/api/diseases/cat_0001"
        }
    })


# ============================================================================
# Custom OpenAPI Schema
# ============================================================================

def custom_openapi():
    """Generate custom OpenAPI schema with extended documentation"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="VetDict REST API",
        version="2.1.0",
        description=app.description,
        routes=app.routes,
        contact=app.contact,
        license_info=app.license_info,
    )

    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.vetdict.example.com",
            "description": "Production server"
        }
    ]

    # Add common parameters
    openapi_schema["components"]["parameters"] = {
        "page": {
            "name": "page",
            "in": "query",
            "description": "Page number (1-indexed)",
            "required": False,
            "schema": {"type": "integer", "default": 1, "minimum": 1}
        },
        "page_size": {
            "name": "page_size",
            "in": "query",
            "description": "Items per page (max 100)",
            "required": False,
            "schema": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100}
        },
        "species": {
            "name": "species",
            "in": "query",
            "description": "Filter by species",
            "required": False,
            "schema": {"type": "string"}
        }
    }

    # Add tags with descriptions
    openapi_schema["tags"] = [
        {
            "name": "Health",
            "description": "Health check and service status endpoints"
        },
        {
            "name": "Diseases",
            "description": "Disease browsing, searching, and detail endpoints"
        },
        {
            "name": "Metadata",
            "description": "Database metadata and statistics endpoints"
        },
        {
            "name": "Root",
            "description": "API root and information endpoint"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


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
