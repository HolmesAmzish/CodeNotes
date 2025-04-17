#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define MAX_NAME_LEN 3
#define MAX_LINE_LEN 50
#define TIME_SLICE 1

typedef struct PCB {
    char name[MAX_NAME_LEN + 1];
    int required_time;
    int executed_time;
    char state; // 'R' - Ready, 'E' - Finished
    struct PCB* next;
} PCB;

PCB* create_pcb(const char* name, int required_time) {
    PCB* new_pcb = (PCB*)malloc(sizeof(PCB));
    if (!new_pcb) {
        perror("Failed to allocate memory for PCB");
        exit(EXIT_FAILURE);
    }
    strncpy(new_pcb->name, name, MAX_NAME_LEN);
    new_pcb->name[MAX_NAME_LEN] = '\0';
    new_pcb->required_time = required_time;
    new_pcb->executed_time = 0;
    new_pcb->state = 'R';
    new_pcb->next = NULL;
    return new_pcb;
}

/**
 * Read processes info from csv file
 * @param head Pointer to the head of the PCB linked list
 * @return Number of processes read
 */
int readProcessesFromCSV(PCB** head, const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        perror("Failed to open CSV file");
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINE_LEN];
    int process_count = 0;
    PCB* tail = NULL;

    while (fgets(line, sizeof(line), file)) {
        char name[MAX_NAME_LEN + 1];
        int required_time, priority;

        if (sscanf(line, "%3[^,],%d,%d", name, &required_time, &priority) == 3) {
            PCB* new_pcb = create_pcb(name, required_time);
            if (*head == NULL) {
                *head = new_pcb;
                tail = new_pcb;
            } else {
                tail->next = new_pcb;
                tail = new_pcb;
            }
            tail->next = *head; // Make it circular
            process_count++;
        }
    }

    fclose(file);
    return process_count;
}

void print_queue_state(PCB* current, PCB* running_process) {
    printf("Queue: ");
    PCB* temp = current;
    if (temp) {
        do {
            printf("(%s, T:%d/%d, S:%c) -> ", 
                  temp->name, temp->executed_time, 
                  temp->required_time, temp->state);
            temp = temp->next;
        } while (temp != current);
    }
    printf("...\n");
}

int main() {
    PCB* ready_queue = NULL;
    int process_count = readProcessesFromCSV(&ready_queue, "processes.csv");

    printf("Initial Process Queue:\n");
    print_queue_state(ready_queue, NULL);

    printf("\nProcessor Scheduling Begins (Time Slice = %d)\n", TIME_SLICE);

    PCB* current_process = ready_queue;
    PCB* previous_process = NULL;
    int completed_processes = 0;

    while (completed_processes < process_count) {
        if (current_process->state == 'R') {
            printf("\nSelected Process: %s\n", current_process->name);
            printf("Before Execution: (%s, T:%d/%d, State: READY)\n",
                  current_process->name, current_process->executed_time,
                  current_process->required_time);

            current_process->executed_time += TIME_SLICE;

            printf("After Execution: (%s, T:%d/%d, State: ",
                  current_process->name, current_process->executed_time,
                  current_process->required_time);

            if (current_process->executed_time >= current_process->required_time) {
                current_process->state = 'E';
                printf("FINISHED)\n");
                completed_processes++;

                // Remove finished process from circular queue
                if (current_process == ready_queue) {
                    if (current_process->next == current_process) {
                        ready_queue = NULL;
                    } else {
                        PCB* temp = current_process;
                        while (temp->next != ready_queue) {
                            temp = temp->next;
                        }
                        temp->next = ready_queue->next;
                        ready_queue = ready_queue->next;
                    }
                } else {
                    previous_process->next = current_process->next;
                }
            } else {
                printf("READY)\n");
            }

            printf("Current Process Queue State:\n");
            print_queue_state(ready_queue ? ready_queue : current_process->next, NULL);
        }

        previous_process = current_process;
        current_process = current_process->next;

        if (ready_queue == NULL) break;
    }

    printf("\nAll processes have finished execution.\n");
    return 0;
}
