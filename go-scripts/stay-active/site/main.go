package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"html/template"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

// HealthResponse represents the health check response
type HealthResponse struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

// License represents a user license
type License struct {
	ID        string    `json:"id"`
	UserID    string    `json:"user_id"`
	IssuedAt  time.Time `json:"issued_at"`
	ExpiresAt time.Time `json:"expires_at"`
	IsActive  bool      `json:"is_active"`
}

// LicenseRequest represents a license generation request
type LicenseRequest struct {
	UserID string `json:"user_id"`
}

// LicenseResponse represents a license generation response
type LicenseResponse struct {
	License License `json:"license"`
	Message string  `json:"message"`
}

// ValidationRequest represents a license validation request
type ValidationRequest struct {
	LicenseID string `json:"license_id"`
}

// ValidationResponse represents a license validation response
type ValidationResponse struct {
	Valid     bool      `json:"valid"`
	ExpiresAt time.Time `json:"expires_at,omitempty"`
	Message   string    `json:"message"`
}

// In-memory license store (in production, use a proper database)
var (
	licenses = make(map[string]License)
	mu       sync.RWMutex
)

// generateLicenseID creates a random license ID
func generateLicenseID() string {
	bytes := make([]byte, 16)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}

// generateLicense creates a new license for a user
func generateLicense(userID string) License {
	now := time.Now()
	license := License{
		ID:        generateLicenseID(),
		UserID:    userID,
		IssuedAt:  now,
		ExpiresAt: now.AddDate(0, 1, 0), // 1 month from now
		IsActive:  true,
	}
	
	mu.Lock()
	licenses[license.ID] = license
	mu.Unlock()
	
	return license
}

// validateLicense checks if a license is valid
func validateLicense(licenseID string) (bool, License) {
	mu.RLock()
	license, exists := licenses[licenseID]
	mu.RUnlock()
	
	if !exists {
		return false, License{}
	}
	
	if !license.IsActive {
		return false, license
	}
	
	if time.Now().After(license.ExpiresAt) {
		// License expired, deactivate it
		mu.Lock()
		license.IsActive = false
		licenses[licenseID] = license
		mu.Unlock()
		return false, license
	}
	
	return true, license
}


// homeHandler serves the main webpage
func homeHandler(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/index.html")
	if err != nil {
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		log.Printf("Template parsing error: %v", err)
		return
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := tmpl.Execute(w, nil); err != nil {
		log.Printf("Template execution error: %v", err)
	}
}

// healthHandler returns the health status of the API
func healthHandler(w http.ResponseWriter, r *http.Request) {
	response := HealthResponse{
		Status:  "healthy",
		Message: "Stay Active API is running",
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("JSON encoding error: %v", err)
	}
}

// licenseGenerateHandler generates a new license for a user
func licenseGenerateHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req LicenseRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if req.UserID == "" {
		http.Error(w, "User ID is required", http.StatusBadRequest)
		return
	}

	license := generateLicense(req.UserID)
	response := LicenseResponse{
		License: license,
		Message: "License generated successfully",
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("JSON encoding error: %v", err)
	}

	log.Printf("Generated license %s for user %s", license.ID, req.UserID)
}

// licenseValidateHandler validates a license
func licenseValidateHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ValidationRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if req.LicenseID == "" {
		http.Error(w, "License ID is required", http.StatusBadRequest)
		return
	}

	valid, license := validateLicense(req.LicenseID)
	
	var response ValidationResponse
	if valid {
		response = ValidationResponse{
			Valid:     true,
			ExpiresAt: license.ExpiresAt,
			Message:   "License is valid",
		}
		w.WriteHeader(http.StatusOK)
	} else {
		response = ValidationResponse{
			Valid:   false,
			Message: "License is invalid or expired",
		}
		w.WriteHeader(http.StatusUnauthorized)
	}

	w.Header().Set("Content-Type", "application/json")
	
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("JSON encoding error: %v", err)
	}

	log.Printf("Validated license %s: valid=%t", req.LicenseID, valid)
}

// setupRoutes configures all API routes with /v1/ prefix
func setupRoutes() *http.ServeMux {
	mux := http.NewServeMux()
	
	// API routes with /v1/ prefix
	mux.HandleFunc("/v1/", homeHandler)
	mux.HandleFunc("/v1/health", healthHandler)
	mux.HandleFunc("/v1/license/generate", licenseGenerateHandler)
	mux.HandleFunc("/v1/license/validate", licenseValidateHandler)
	
	return mux
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	mux := setupRoutes()
	
	log.Printf("🚀 Stay Active API server starting on port %s", port)
	log.Printf("📍 Routes available:")
	log.Printf("   GET  /v1/                  - Homepage")
	log.Printf("   GET  /v1/health            - Health check")
	log.Printf("   POST /v1/license/generate  - Generate license")
	log.Printf("   POST /v1/license/validate  - Validate license")
	
	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatalf("❌ Server failed to start: %v", err)
	}
}
