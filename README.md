# Gender Classifier API

A FastAPI-based web service that predicts gender based on first names using the [Genderize.io](https://genderize.io) API. The service provides confidence scoring and detailed analytics for gender predictions.

Here is the link to the live repo: https://gender-classifier-production-0c78.up.railway.app/docs

## Features

- **Gender Prediction**: Classify names by predicted gender using Genderize.io API
- **Confidence Scoring**: Returns probability and confidence levels for predictions
- **Input Validation**: Validates names to ensure they contain only alphabetic characters
- **Error Handling**: Comprehensive error handling with meaningful HTTP status codes
- **CORS Support**: Enabled cross-origin requests for browser-based clients
- **Async Processing**: Built with async/await for efficient request handling
- **ISO Timestamps**: Returns standardized UTC timestamps in ISO 8601 format

## Tech Stack

- **Framework**: FastAPI 0.135.3
- **HTTP Client**: httpx (async HTTP requests)
- **Python**: 3.10+
- **CORS**: FastAPI CORS Middleware

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Oredelight/gender-classifier
cd gender-classifier
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Start the FastAPI development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Classify Name

**Endpoint**: `GET /api/classify`

**Query Parameters**:
- `name` (string, required): The first name to classify

**Example Request**:
```bash
curl "http://localhost:8000/api/classify?name=Alice"
```

**Success Response** (200):
```json
{
  "status": "success",
  "data": {
    "name": "Alice",
    "gender": "female",
    "probability": 0.99,
    "sample_size": 50000,
    "is_confident": true,
    "processed_at": "2026-04-14T10:30:45Z"
  }
}
```

**Error Responses**:

- **400 Bad Request**: Missing name parameter or name is empty
```json
{
  "status": "error",
  "message": "Name query parameter is required"
}
```

- **422 Unprocessable Entity**: Name contains non-alphabetic characters
```json
{
  "status": "error",
  "message": "Name must be a string"
}
```

- **502 Bad Gateway**: External API error
```json
{
  "status": "error",
  "message": "External API error"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The input name that was classified |
| `gender` | string | Predicted gender (`male` or `female`) |
| `probability` | float | Confidence probability (0.0 - 1.0) |
| `sample_size` | integer | Number of data samples used for prediction |
| `is_confident` | boolean | High confidence indicator (probability ≥ 0.7 AND sample_size ≥ 100) |
| `processed_at` | string | ISO 8601 timestamp of when the request was processed |

## Configuration

### CORS Settings

Currently configured to allow all origins:
- `allow_origins`: `["*"]`
- `allow_credentials`: `true`
- `allow_methods`: `["*"]`
- `allow_headers`: `["*"]`

### Timeout

HTTP client timeout is set to 5 seconds for external API calls.

## Project Structure

```
gender-classifier/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── transport/
│   └── routes.py       # API route definitions
```

## Development

### Running Tests

To test the API endpoint:
```bash
python -c "import httpx; import asyncio; print(asyncio.run(httpx.AsyncClient().get('http://localhost:8000/api/classify?name=John')))"
```

Or use the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

The API implements the following error handling:

1. **Validation Errors**: Input validation for empty or non-alphabetic names
2. **External API Errors**: Handles failures from Genderize.io API
3. **Timeout Handling**: 5-second timeout to prevent hanging requests
4. **Structured Error Responses**: All errors return JSON with status and message fields
