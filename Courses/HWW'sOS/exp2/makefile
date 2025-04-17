# Compiler and flags
CC = gcc
CFLAGS = -Wall -g

# Source files and output binaries
SRC1 = priority_schedule.c
SRC2 = round_robin_schedule.c
BIN1 = priority_schedule.out
BIN2 = round_robin_schedule.out

# Default target
all: $(BIN1) $(BIN2) run

# Build the first program
$(BIN1): $(SRC1)
	$(CC) $(CFLAGS) -o $@ $<

# Build the second program
$(BIN2): $(SRC2)
	$(CC) $(CFLAGS) -o $@ $<

# Run the programs and redirect output
run: $(BIN1) $(BIN2)
	./$(BIN1) > output0.txt
	./$(BIN2) > output1.txt

# Clean up generated files
clean:
	rm -f $(BIN1) $(BIN2) output0.txt output1.txt