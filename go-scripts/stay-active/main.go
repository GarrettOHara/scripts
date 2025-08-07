package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"os/signal"
	"strings"
	"sync"
	"time"

	"github.com/go-vgo/robotgo"
	hook "github.com/robotn/gohook"
)

// activeService holds the state and configuration for our service.
type activeService struct {
	lastActivityTime  time.Time
	lastJiggleTime    time.Time
	idleDelay         time.Duration
	verboseMode       bool
	workWindowStart   int // Hour in 24h format (e.g., 7 for 7am)
	workWindowEnd     int // Hour in 24h format (e.g., 15 for 3pm)
	timeWindowEnabled bool
	mu                sync.Mutex
}

// updateLastActivity safely sets the last activity time to now.
func (s *activeService) updateLastActivity() {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.lastActivityTime = time.Now()
}

// isUserIdle checks if the user has been idle longer than the configured delay.
func (s *activeService) isUserIdle() bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	return time.Since(s.lastActivityTime) > s.idleDelay
}

// isWithinWorkWindow checks if the current time is within the configured work window.
func (s *activeService) isWithinWorkWindow() bool {
	if !s.timeWindowEnabled {
		return true
	}
	now := time.Now()
	currentHour := now.Hour()
	return currentHour >= s.workWindowStart && currentHour < s.workWindowEnd
}

// promptUserToContinue asks the user if they want to continue outside work hours.
func promptUserToContinue() bool {
	fmt.Print("⚠️  You're starting outside work hours (7am-3pm). Continue anyway? (y/n): ")
	reader := bufio.NewReader(os.Stdin)
	response, _ := reader.ReadString('\n')
	response = strings.TrimSpace(strings.ToLower(response))
	return response == "y" || response == "yes"
}

// startListeners runs in a goroutine to listen for global input events.
func (s *activeService) startListeners() {
	fmt.Println("👂 Listening for your keyboard and mouse input...")
	events := hook.Start()
	defer hook.End()

	for e := range events {
		// Any event (mouse move, click, key press, etc.) counts as activity.
		if e.Kind > 0 {
			// Debug: Log what type of event was detected (only in debug mode)
			if s.verboseMode {
				fmt.Printf(
					"🔍 [%s] Activity detected - Kind: %d, Keycode: %d, X: %d, Y: %d\n",
					time.Now().Format("15:04:05"),
					e.Kind,
					e.Keycode,
					e.X,
					e.Y,
				)
			}
			s.updateLastActivity()
		}
	}
}

// jiggleMouse performs a small, non-disruptive mouse movement.
func (s *activeService) jiggleMouse() {
	fmt.Printf(
		"🏃 [%s] User idle for >%.0f mins. Jiggling mouse.\n",
		time.Now().Format("2006-01-02 15:04:05"),
		s.idleDelay.Minutes(),
	)
	// Move a tiny amount and then move back.
	robotgo.MoveRelative(1, 1)
	time.Sleep(100 * time.Millisecond)
	robotgo.MoveRelative(-1, -1)

	// Track when we jiggled
	s.mu.Lock()
	s.lastJiggleTime = time.Now()
	s.mu.Unlock()
}

func main() {
	// 1. Set up custom usage message
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "stay-active - Keep your computer active by jiggling the mouse\n\n")
		fmt.Fprintf(os.Stderr, "Usage: %s [options]\n\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "Options:\n")
		flag.PrintDefaults()
		fmt.Fprintf(os.Stderr, "\nExamples:\n")
		fmt.Fprintf(os.Stderr, "  %s                                # Run with defaults (2min delay, 7am-3pm window)\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "  %s --delay 5.0                    # Jiggle after 5 minutes of inactivity\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "  %s --verbose                      # Show detailed activity logs\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "  %s --work-start 9 --work-end 17   # Custom work hours (9am-5pm)\n", os.Args[0])
	}

	// 2. Define and parse the command-line flags.
	delayMinutes := flag.Float64("delay", 2.0, "Idle time in minutes before mouse jiggling (default: 2.0)")
	verboseMode := flag.Bool("verbose", false, "Show detailed activity and countdown logs")
	workStart := flag.Int("work-start", 7, "Work window start hour in 24h format (default: 7 for 7am)")
	workEnd := flag.Int("work-end", 15, "Work window end hour in 24h format (default: 15 for 3pm)")
	flag.Parse()

	// 2. Create and configure the service instance.
	service := &activeService{
		lastActivityTime:  time.Now(),
		lastJiggleTime:    time.Time{}, // Zero time means never jiggled
		idleDelay:         time.Duration(*delayMinutes * float64(time.Minute)),
		verboseMode:       *verboseMode,
		workWindowStart:   *workStart,
		workWindowEnd:     *workEnd,
		timeWindowEnabled: true,
	}

	// 3. Check if we're starting within work hours
	if !service.isWithinWorkWindow() {
		if !promptUserToContinue() {
			fmt.Println("👋 Exiting stay-active.")
			os.Exit(0)
		}
		// User chose to continue, disable time window
		service.timeWindowEnabled = false
		fmt.Println("⚠️  Time window disabled for this session.")
	}

	fmt.Printf("✅ Service initialized. Will jiggle mouse after %.1f minute(s) of inactivity.\n", *delayMinutes)

	// 4. Set up graceful shutdown handling.
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		<-c
		fmt.Println("👋 Exiting stay-active.")
		os.Exit(0)
	}()

	// 5. Start listening for user activity in the background.
	go service.startListeners()

	// 6. Run the main loop to check for idleness.
	jiggleInterval := 30 * time.Second
	for {
		// Check if we're still within work hours (if enabled)
		if !service.isWithinWorkWindow() {
			fmt.Println("🕐 Work window ended. Exiting stay-active.")
			os.Exit(0)
		}

		service.mu.Lock()
		timeSinceActivity := time.Since(service.lastActivityTime)
		timeSinceJiggle := time.Since(service.lastJiggleTime)
		isIdle := timeSinceActivity > service.idleDelay
		canJiggle := service.lastJiggleTime.IsZero() || timeSinceJiggle > jiggleInterval
		service.mu.Unlock()

		if isIdle && canJiggle {
			service.jiggleMouse()
		} else if service.verboseMode {
			// Show countdown only in debug mode - either for activity or for next jiggle
			if isIdle && !canJiggle {
				// User is idle but we're in jiggle cooldown
				timeUntilNextJiggle := jiggleInterval - timeSinceJiggle
				fmt.Printf("⏳ [%s] Idle but cooling down - %.1fs until next jiggle\n",
					time.Now().Format("15:04:05"),
					timeUntilNextJiggle.Seconds())
			} else {
				// User is active - show normal countdown
				fmt.Printf(
					"⏱️ [%s] User inactive - %.1fs since "+
						"last activity (need %.1fs)\n",
					time.Now().Format("15:04:05"),
					timeSinceActivity.Seconds(),
					service.idleDelay.Seconds())
			}
		}

		// Always check again in a second to be responsive
		time.Sleep(1 * time.Second)
	}
}
