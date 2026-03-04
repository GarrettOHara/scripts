package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

// LicenseInfo represents the cached license information
type LicenseInfo struct {
	ID        string    `json:"id"`
	UserID    string    `json:"user_id"`
	IssuedAt  time.Time `json:"issued_at"`
	ExpiresAt time.Time `json:"expires_at"`
	IsActive  bool      `json:"is_active"`
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

// LicenseGenerationRequest represents a license generation request
type LicenseGenerationRequest struct {
	UserID string `json:"user_id"`
}

// LicenseGenerationResponse represents a license generation response
type LicenseGenerationResponse struct {
	License LicenseInfo `json:"license"`
	Message string      `json:"message"`
}

const (
	defaultLicenseServer = "http://localhost:8080"
	licenseCacheFile     = ".stay-active-license.json"
)

// getLicenseCachePath returns the path to the license cache file
func getLicenseCachePath() string {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return licenseCacheFile
	}
	return filepath.Join(homeDir, licenseCacheFile)
}

// loadCachedLicense loads the license from the cache file
func loadCachedLicense() (*LicenseInfo, error) {
	cachePath := getLicenseCachePath()
	data, err := os.ReadFile(cachePath)
	if err != nil {
		return nil, err
	}

	var license LicenseInfo
	if err := json.Unmarshal(data, &license); err != nil {
		return nil, err
	}

	return &license, nil
}

// saveLicenseToCache saves the license to the cache file
func saveLicenseToCache(license *LicenseInfo) error {
	cachePath := getLicenseCachePath()
	data, err := json.Marshal(license)
	if err != nil {
		return err
	}

	return os.WriteFile(cachePath, data, 0600)
}

// validateLicenseWithServer validates the license with the remote server
func validateLicenseWithServer(licenseID string) (*ValidationResponse, error) {
	serverURL := os.Getenv("STAY_ACTIVE_LICENSE_SERVER")
	if serverURL == "" {
		serverURL = defaultLicenseServer
	}

	reqBody := ValidationRequest{LicenseID: licenseID}
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return nil, err
	}

	resp, err := http.Post(
		serverURL+"/v1/license/validate",
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var validationResp ValidationResponse
	if err := json.Unmarshal(body, &validationResp); err != nil {
		return nil, err
	}

	return &validationResp, nil
}

// generateLicenseFromServer requests a new license from the server
func generateLicenseFromServer(userID string) (*LicenseInfo, error) {
	serverURL := os.Getenv("STAY_ACTIVE_LICENSE_SERVER")
	if serverURL == "" {
		serverURL = defaultLicenseServer
	}

	reqBody := LicenseGenerationRequest{UserID: userID}
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return nil, err
	}

	resp, err := http.Post(
		serverURL+"/v1/license/generate",
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		return nil, fmt.Errorf("server returned status %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var genResp LicenseGenerationResponse
	if err := json.Unmarshal(body, &genResp); err != nil {
		return nil, err
	}

	return &genResp.License, nil
}

// promptForUserID prompts the user to enter their user ID
func promptForUserID() string {
	fmt.Print("📝 Please enter your user ID (email or username): ")
	var userID string
	fmt.Scanln(&userID)
	return userID
}

// checkLicense validates the license and handles first-time setup
func checkLicense() error {
	fmt.Println("🔐 Checking license...")

	// Try to load cached license
	cachedLicense, err := loadCachedLicense()
	if err != nil {
		// No cached license, this is first run
		fmt.Println("📋 No license found. Setting up for first time...")
		
		userID := promptForUserID()
		if userID == "" {
			return fmt.Errorf("user ID is required")
		}

		fmt.Println("🔄 Generating license...")
		license, err := generateLicenseFromServer(userID)
		if err != nil {
			return fmt.Errorf("failed to generate license: %v", err)
		}

		// Save to cache
		if err := saveLicenseToCache(license); err != nil {
			fmt.Printf("⚠️  Warning: Could not cache license: %v\n", err)
		}

		fmt.Printf("✅ License generated successfully! Expires: %s\n", 
			license.ExpiresAt.Format("2006-01-02 15:04:05"))
		return nil
	}

	// Validate cached license with server
	fmt.Printf("🔍 Validating license %s...\n", cachedLicense.ID[:8]+"...")
	
	validation, err := validateLicenseWithServer(cachedLicense.ID)
	if err != nil {
		return fmt.Errorf("failed to validate license: %v", err)
	}

	if !validation.Valid {
		fmt.Printf("❌ License is invalid or expired: %s\n", validation.Message)
		
		// Try to generate a new license
		fmt.Println("🔄 Attempting to renew license...")
		userID := promptForUserID()
		if userID == "" {
			return fmt.Errorf("user ID is required for license renewal")
		}

		license, err := generateLicenseFromServer(userID)
		if err != nil {
			return fmt.Errorf("failed to renew license: %v", err)
		}

		// Save new license to cache
		if err := saveLicenseToCache(license); err != nil {
			fmt.Printf("⚠️  Warning: Could not cache renewed license: %v\n", err)
		}

		fmt.Printf("✅ License renewed successfully! Expires: %s\n", 
			license.ExpiresAt.Format("2006-01-02 15:04:05"))
		return nil
	}

	fmt.Printf("✅ License is valid! Expires: %s\n", 
		validation.ExpiresAt.Format("2006-01-02 15:04:05"))
	return nil
}
