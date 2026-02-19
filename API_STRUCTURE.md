# API Structure - Phase 3

## Endpoints Overview

### Root Endpoints
- `GET /` - API information
- `GET /health` - Health check

### Upload Endpoints (`/api/v1/upload`)
- `POST /api/v1/upload/user-image` - Upload user photo
- `POST /api/v1/upload/clothing-image` - Upload clothing image
- `POST /api/v1/upload/batch` - Batch upload multiple images

### Try-On Endpoints (`/api/v1/tryon`)
- `POST /api/v1/tryon/try-on` - Process virtual try-on
- `GET /api/v1/tryon/status/{job_id}` - Check processing status

### Documentation
- `GET /docs` - Interactive Swagger UI
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

## Request/Response Models

### Upload Response
```json
{
  "filename": "user_photo.jpg",
  "file_id": "user_abc123",
  "message": "Upload successful",
  "url": "/storage/uploads/user_abc123.jpg"
}
```

### Try-On Request
```json
{
  "user_image_id": "user_abc123",
  "clothing_image_id": "cloth_xyz789",
  "options": {
    "quality": "high",
    "preserve_background": true
  }
}
```

### Try-On Response
```json
{
  "job_id": "job_def456",
  "status": "processing",
  "result_url": null,
  "processing_time": null,
  "message": "Processing started"
}
```

## Error Handling

All errors return consistent format:
```json
{
  "detail": "Error message",
  "error_code": "ErrorType"
}
```

### Custom Exceptions
- `VTOException` - Base exception
- `ImageProcessingError` - Image processing failures
- `InvalidImageError` - Invalid image format/size
- `ModelInferenceError` - ML model errors

## Validation

### Image Upload Validation
- Allowed formats: JPG, PNG
- Max file size: 10MB
- Min dimensions: 256x256px
- Max dimensions: 4096x4096px

### Request Validation
- Automatic via Pydantic models
- Field-level validators
- Type checking
- Required field enforcement

## Middleware

### CORS
- Configured origins from settings
- Allows credentials
- All methods and headers allowed

### Request Logging
- Logs all requests/responses
- Tracks processing time
- Adds X-Process-Time header

### Error Handling
- Catches all exceptions
- Returns consistent error format
- Logs errors for debugging

## Testing

Run the test script:
```bash
# Start server
python run.py

# In another terminal
python test_api.py
```

Or use the interactive docs:
```
http://localhost:8000/docs
```

## Next Phase

Phase 4 will implement:
- Actual file upload handling
- File storage management
- Image preprocessing
- File validation with actual image reading
