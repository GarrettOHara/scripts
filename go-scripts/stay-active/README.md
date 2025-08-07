# Stay Active

A lightweight Go application that prevents your computer from going to sleep by automatically jiggling the mouse cursor when user inactivity is detected.

## Overview

Stay Active monitors global keyboard and mouse input events and automatically performs subtle mouse movements when the user has been inactive for a configurable period. This helps prevent screen savers, sleep mode, or automatic logouts during periods of inactivity while maintaining a non-intrusive user experience.

## Features

- **Global Activity Monitoring**: Tracks all keyboard and mouse events system-wide
- **Configurable Idle Timeout**: Set custom inactivity periods before mouse jiggling begins
- **Subtle Mouse Movement**: Performs minimal 1-pixel movements that are barely noticeable
- **Real-time Status Updates**: Provides detailed logging of activity detection and system status
- **Graceful Shutdown**: Clean exit with Ctrl+C
- **Thread-safe Operations**: Concurrent activity monitoring with mutex protection
- **Jiggle Cooldown**: 30-second intervals between mouse jiggles to prevent excessive movement

## Installation

### Prerequisites

- Go 1.16 or later
- macOS (uses robotgo and gohook libraries)

### Build

```bash
# Clone or download the source
cd stay-active

# Build the executable
make build
# or manually:
# go build -o build/stay-active main.go
```

## Usage

### Basic Usage

```bash
# Use default 2-minute idle timeout
./build/stay-active

# Set custom idle timeout (in minutes)
./build/stay-active -delay 0.1    # 6 seconds (0.1 minutes)
./build/stay-active -delay 5.0    # 5 minutes
./build/stay-active -delay 10     # 10 minutes
```

### Command Line Options

- `-delay <minutes>`: Set the idle timeout in minutes before mouse jiggling starts (default: 2.0)

### Example Output

```
✅ Service initialized. Will jiggle mouse after 0.1 minute(s) of inactivity.
👂 Listening for your keyboard and mouse input...
⏱️ [14:08:18] User active - 0.0s since last activity (need 6.0s)
🔍 [14:08:18] Activity detected - Kind: 1, Keycode: 0, X: 0, Y: 0
⏱️ [14:08:19] User active - 0.9s since last activity (need 6.0s)
⏱️ [14:08:24] User active - 6.0s since last activity (need 6.0s)
🏃 [2025-08-07 14:08:25] User idle for >0 mins. Jiggling mouse.
🔍 [14:08:25] Activity detected - Kind: 9, Keycode: 0, X: 583, Y: 467
```

## How It Works

1. **Initialization**: The service starts with the specified idle delay configuration
2. **Activity Monitoring**: Global hooks capture all keyboard and mouse events
3. **Idle Detection**: Continuously checks if time since last activity exceeds the configured delay
4. **Mouse Jiggling**: When idle threshold is reached, performs a 1-pixel movement and immediate return
5. **Cooldown Period**: Waits 30 seconds between jiggles to prevent excessive movement
6. **Status Reporting**: Provides real-time feedback on user activity and system state

## Activity Event Types

The application detects various input events, indicated by different "Kind" values in the logs:

- **Kind 1**: Keyboard key press
- **Kind 3-5**: Keyboard events (press/release cycles)
- **Kind 9**: Mouse movement
- **Other kinds**: Various input device events

## Use Cases

- **Remote Work**: Prevent automatic logout during video calls or long meetings
- **Presentations**: Keep screen active during lengthy presentations
- **Long Tasks**: Maintain session during file transfers, downloads, or processing
- **Development**: Prevent sleep during long compilation or testing processes

## Technical Details

- **Language**: Go
- **Dependencies**: 
  - `github.com/go-vgo/robotgo` - Cross-platform mouse/keyboard automation
  - `github.com/robotn/gohook` - Global input event hooks
- **Concurrency**: Uses goroutines for non-blocking activity monitoring
- **Thread Safety**: Mutex-protected shared state for activity timestamps
- **Platform**: Currently optimized for macOS

## Stopping the Application

Press `Ctrl+C` to gracefully shutdown the application:

```
^C👋 Exiting stay-active.
```

## Building from Source

```bash
# Install dependencies
go mod tidy

# Build executable
go build -o build/stay-active main.go

# Or use the provided Makefile
make build
```

## License

This project is provided as-is for personal and educational use.

## Troubleshooting

- **Permission Issues**: On macOS, you may need to grant accessibility permissions to your terminal application
- **High CPU Usage**: The application is designed to be lightweight, but frequent logging can impact performance
- **Mouse Sensitivity**: The 1-pixel jiggle is designed to be minimal and should not interfere with normal usage
