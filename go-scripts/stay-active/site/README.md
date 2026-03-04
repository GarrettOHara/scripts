# Stay Active Website API

A simple Golang API server that serves a website to distribute the Stay Active productivity tool.

## Features

- **Clean API Design**: RESTful endpoints with `/v1/` prefix following best practices
- **Minimal Dependencies**: Uses only Go standard library
- **Beautiful UI**: Modern, responsive design for the homepage
- **Modular Templates**: HTML templates separated from Go code for maintainability
- **Health Monitoring**: Built-in health check endpoint

## Project Structure

```
site/
├── main.go              # API server code
├── templates/
│   └── index.html       # Homepage HTML template
├── go.mod              # Go module file
└── README.md           # This file
```

## API Endpoints

- `GET /v1/` - Serves the main website homepage
- `GET /v1/health` - Returns API health status in JSON format
- `POST /v1/license/generate` - Generates a new monthly license for a user
- `POST /v1/license/validate` - Validates an existing license

## Running the Server

```bash
# Start the server (default port 8080)
go run main.go

# Or specify a custom port
PORT=3000 go run main.go
```

## Building for Production

```bash
# Build the binary
go build -o stay-active-site main.go

# Run the binary
./stay-active-site
```

## Environment Variables

- `PORT` - Server port (default: 8080)

## API Response Examples

### Health Check
```bash
curl http://localhost:8080/v1/health
```

Response:
```json
{
  "status": "healthy",
  "message": "Stay Active API is running"
}
```

### Homepage
```bash
curl http://localhost:8080/v1/
```

Returns a beautiful HTML page showcasing the Stay Active tool with download links and feature descriptions.

### License Generation
```bash
curl -X POST http://localhost:8080/v1/license/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user@example.com"}'
```

Response:
```json
{
  "license": {
    "id": "e645697e37ca1d242c60f92cb3e4b6be",
    "user_id": "user@example.com",
    "issued_at": "2025-10-15T22:39:50.489698-07:00",
    "expires_at": "2025-11-15T22:39:50.489698-08:00",
    "is_active": true
  },
  "message": "License generated successfully"
}
```

### License Validation
```bash
curl -X POST http://localhost:8080/v1/license/validate \
  -H "Content-Type: application/json" \
  -d '{"license_id": "e645697e37ca1d242c60f92cb3e4b6be"}'
```

Response (Valid):
```json
{
  "valid": true,
  "expires_at": "2025-11-15T22:39:50.489698-08:00",
  "message": "License is valid"
}
```

Response (Invalid):
```json
{
  "valid": false,
  "message": "License is invalid or expired"
}
```

## License System

The Stay Active binary includes an integrated license system:

- **Monthly Licenses**: Each license expires after 30 days
- **Automatic Generation**: First-time users are prompted to generate a license
- **Local Caching**: Licenses are cached in `~/.stay-active-license.json`
- **Server Validation**: License validity is checked on each startup
- **Automatic Renewal**: Expired licenses prompt for renewal

### Environment Variables

- `STAY_ACTIVE_LICENSE_SERVER` - License server URL (default: http://localhost:8080)
