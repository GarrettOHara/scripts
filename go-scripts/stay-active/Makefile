# Makefile for cross-platform compilation of stay-active

# Binary name
BINARY_NAME=stay-active

# Version (can be overridden)
VERSION?=1.0.0

# Build directory
BUILD_DIR=build

# Go build flags
LDFLAGS=-ldflags "-X main.version=$(VERSION)"

# Note: This project uses CGO dependencies (robotgo, gohook) that require
# platform-specific system libraries. Cross-compilation is not supported.
# Build on the target platform for best results.

# Default target
.PHONY: all
all: clean build

# Clean build directory
.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)

# Build for current platform
.PHONY: build
build:
	go build $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) .

# Build for current platform (recommended due to CGO dependencies)
.PHONY: build-native
build-native: build

# Docker-based cross-compilation (alternative approach)
.PHONY: build-docker-linux
build-docker-linux:
	@echo "Building Linux binary using Docker..."
	docker run --rm -v "$(PWD):/workspace" -w /workspace golang:1.21 \
		sh -c "apt-get update && apt-get install -y libx11-dev libxtst-dev libxinerama-dev libxrandr-dev libxss-dev libxkbcommon-dev && go build $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-amd64 ."

.PHONY: build-docker-windows
build-docker-windows:
	@echo "Note: Windows cross-compilation requires a Windows environment or complex setup"
	@echo "Consider building on a Windows machine or using GitHub Actions"

# GitHub Actions workflow suggestion
.PHONY: setup-ci
setup-ci:
	@echo "For multi-platform builds, consider using GitHub Actions."
	@echo "Create .github/workflows/build.yml with platform-specific runners:"
	@echo "- ubuntu-latest for Linux builds"
	@echo "- windows-latest for Windows builds"
	@echo "- macos-latest for macOS builds"

# Development targets
.PHONY: run
run:
	go run . -delay=1

.PHONY: test
test:
	go test ./...

.PHONY: fmt
fmt:
	go fmt ./...

.PHONY: vet
vet:
	go vet ./...

.PHONY: mod-tidy
mod-tidy:
	go mod tidy

.PHONY: mod-download
mod-download:
	go mod download

# Install dependencies
.PHONY: deps
deps: mod-download

# Create release archives
.PHONY: release
release: build
	cd $(BUILD_DIR) && \
	for file in $(BINARY_NAME)*; do \
		if [[ "$$file" == *.exe ]]; then \
			zip "$${file%.*}.zip" "$$file"; \
		else \
			tar -czf "$$file.tar.gz" "$$file"; \
		fi; \
	done

# List all available targets
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all              - Clean and build for current platform"
	@echo "  build            - Build for current platform"
	@echo "  build-native     - Same as build (recommended)"
	@echo "  build-docker-linux - Build Linux binary using Docker"
	@echo "  clean            - Remove build directory"
	@echo "  run              - Run the application with 1-minute delay"
	@echo "  test             - Run tests"
	@echo "  fmt              - Format code"
	@echo "  vet              - Run go vet"
	@echo "  deps             - Download dependencies"
	@echo "  release          - Create release archives"
	@echo "  setup-ci         - Show GitHub Actions setup info"
	@echo "  help             - Show this help message"
	@echo ""
	@echo "Note: This project uses CGO dependencies that require platform-specific"
	@echo "system libraries. Cross-compilation is not supported. Build on the target"
	@echo "platform or use Docker/CI for multi-platform builds."
