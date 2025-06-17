CC = gcc
CFLAGS = -Wall -Wextra -O2 -g

TARGETS = page_faults tlb_effects cow thrashing

all: $(TARGETS)

page_faults: page_faults.c
	$(CC) $(CFLAGS) -o $@ $<

tlb_effects: tlb_effects.c
	$(CC) $(CFLAGS) -o $@ $<

cow: cow.c
	$(CC) $(CFLAGS) -o $@ $<

thrashing: thrashing.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS)

test: all
	@echo "=== Testing Page Faults ==="
	/usr/bin/time -v ./page_faults
	@echo ""
	@echo "=== Testing TLB Effects ==="
	@echo "Note: perf may require sudo or special permissions"
	./tlb_effects
	@echo ""
	@echo "=== Testing Copy-On-Write ==="
	./cow
	@echo ""
	@echo "=== Testing Thrashing (Ctrl+C to stop) ==="
	@echo "Warning: This may slow down your system!"
	./thrashing

.PHONY: all clean test
