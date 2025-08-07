package main

import (
	"flag"
	"fmt"
	"os"
	"os/signal"
	"sync"
	"time"

	"github.com/go-vgo/robotgo"
	hook "github.com/robotn/gohook"
)

// activeService holds the state and configuration for our service.
type activeService struct {
	lastActivityTime time.Time
	mu               sync.Mutex // Protects lastActivityTime from concurrent access
	idleDelay        time.Duration
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

// startListeners runs in a goroutine to listen for global input events.
func (s *activeService) startListeners() {
	fmt.Println("👂 Listening for your keyboard and mouse input...")
	events := hook.Start()
	defer hook.End()

	for e := range events {
		// Any event (mouse move, click, key press, etc.) counts as activity.
		if e.Kind > 0 {
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
}

func main() {
	// 1. Define and parse the command-line flag for idle delay.
	delayMinutes := flag.Float64("delay", 2.0, "The user idle time in minutes before the mouse starts jiggling.")
	flag.Parse()

	// 2. Create and configure the service instance.
	service := &activeService{
		lastActivityTime: time.Now(),
		idleDelay:        time.Duration(*delayMinutes * float64(time.Minute)),
	}

	fmt.Printf("✅ Service initialized. Will jiggle mouse after %.1f minute(s) of inactivity.\n", *delayMinutes)

	// 3. Set up graceful shutdown handling.
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		<-c
		fmt.Println("👋 Exiting stay-active.")
		os.Exit(0)
	}()

	// 4. Start listening for user activity in the background.
	go service.startListeners()

	// 5. Run the main loop to check for idleness.
	jiggleInterval := 30 * time.Second
	for {
		if service.isUserIdle() {
			service.jiggleMouse()
			// After jiggling, wait for the full interval before checking again.
			time.Sleep(jiggleInterval)
		} else {
			// If the user is active, check again in a second to be responsive.
			time.Sleep(1 * time.Second)
		}
	}
}
