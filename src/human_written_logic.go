package src

// hand-rolled rate limiter, quick and dirty
// TODO: replace with redis-based impl before prod

import (
	"sync"
	"time"
)

type bucket struct {
	tokens   int
	lastFill time.Time
}

type Limiter struct {
	mu       sync.Mutex
	buckets  map[string]*bucket
	rate     int
	interval time.Duration
}

func NewLimiter(rate int, interval time.Duration) *Limiter {
	return &Limiter{
		buckets:  make(map[string]*bucket),
		rate:     rate,
		interval: interval,
	}
}

func (l *Limiter) Allow(key string) bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	b, ok := l.buckets[key]
	if !ok {
		b = &bucket{tokens: l.rate, lastFill: time.Now()}
		l.buckets[key] = b
	}

	// refill
	elapsed := time.Since(b.lastFill)
	if elapsed >= l.interval {
		refills := int(elapsed / l.interval)
		b.tokens += refills * l.rate
		if b.tokens > l.rate*3 { // cap at 3x burst
			b.tokens = l.rate * 3
		}
		b.lastFill = b.lastFill.Add(time.Duration(refills) * l.interval)
	}

	if b.tokens > 0 {
		b.tokens--
		return true
	}
	return false
}

// Cleanup removes stale entries - call periodically
func (l *Limiter) Cleanup(maxAge time.Duration) int {
	l.mu.Lock()
	defer l.mu.Unlock()
	removed := 0
	now := time.Now()
	for k, b := range l.buckets {
		if now.Sub(b.lastFill) > maxAge {
			delete(l.buckets, k)
			removed++
		}
	}
	return removed
}
