#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define MAX_NAME_LEN 3
#define MAX_LINE_LEN 50
#define TIME_SLICE 1
#define HIGH_PRIORITY_QUEUE 3

typedef enum {
    READY,
    FINISHED
} ProcessState;

typedef struct PCB {
    char name[MAX_NAME_LEN + 1];
    int required_time;
    int priority;
    int executed_time;
    ProcessState state;
    struct PCB *next;
} PCB;

typedef struct {
    PCB *head;
    PCB *tail;
    int count;
} Queue;

void initQueue(Queue *q) {
    q->head = q->tail = NULL;
    q->count = 0;
}

void enqueue(Queue *q, PCB *pcb) {
    if (q->head == NULL) {
        q->head = q->tail = pcb;
        pcb->next = pcb;
    } else {
        pcb->next = q->head;
        q->tail->next = pcb;
        q->tail = pcb;
    }
    q->count++;
}

PCB *dequeue(Queue *q) {
    if (q->head == NULL) return NULL;
    
    PCB *pcb = q->head;
    if (q->head == q->tail) {
        q->head = q->tail = NULL;
    } else {
        q->head = q->head->next;
        q->tail->next = q->head;
    }
    q->count--;
    return pcb;
}

PCB *createPCB(const char *name, int required_time, int priority) {
    PCB *pcb = (PCB *)malloc(sizeof(PCB));
    if (!pcb) {
        perror("Failed to allocate memory for PCB");
        exit(EXIT_FAILURE);
    }
    strncpy(pcb->name, name, MAX_NAME_LEN);
    pcb->name[MAX_NAME_LEN] = '\0';
    pcb->required_time = required_time;
    pcb->priority = priority;
    pcb->executed_time = 0;
    pcb->state = READY;
    pcb->next = NULL;
    return pcb;
}

void printQueue(Queue *q, const char *queueName) {
    printf("%s Queue (%d processes): ", queueName, q->count);
    if (q->head) {
        PCB *current = q->head;
        do {
            printf("(%s, P:%d, T:%d/%d) -> ", 
                  current->name, current->priority,
                  current->executed_time, current->required_time);
            current = current->next;
        } while (current != q->head);
    }
    printf("...\n");
}

int readProcessesFromCSV(Queue *highQueue, Queue *lowQueue, const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Failed to open CSV file");
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINE_LEN];
    int process_count = 0;

    while (fgets(line, sizeof(line), file)) {
        char name[MAX_NAME_LEN + 1];
        int required_time, priority;

        if (sscanf(line, "%3[^,],%d,%d", name, &required_time, &priority) == 3) {
            PCB *pcb = createPCB(name, required_time, priority);
            if (priority >= HIGH_PRIORITY_QUEUE) {
                enqueue(highQueue, pcb);
            } else {
                enqueue(lowQueue, pcb);
            }
            process_count++;
        }
    }

    fclose(file);
    return process_count;
}

int main() {
    Queue highPriorityQueue, lowPriorityQueue;
    initQueue(&highPriorityQueue);
    initQueue(&lowPriorityQueue);

    int total_processes = readProcessesFromCSV(&highPriorityQueue, &lowPriorityQueue, "processes.csv");

    printf("Initial Queues:\n");
    printQueue(&highPriorityQueue, "High Priority");
    printQueue(&lowPriorityQueue, "Low Priority");

    printf("\nProcessor Scheduling Begins:\n");

    int finished_processes = 0;
    PCB *current_process = NULL;
    Queue *current_queue = NULL;

    while (finished_processes < total_processes) {
        if (highPriorityQueue.head) {
            current_queue = &highPriorityQueue;
            current_process = dequeue(current_queue);
            
            printf("\nSelected Process (High Priority): %s\n", current_process->name);
            current_process->executed_time++;
            current_process->priority--;

            printf("After Execution: (%s, P:%d, T:%d/%d, State: ",
                  current_process->name, current_process->priority,
                  current_process->executed_time, current_process->required_time);

            if (current_process->executed_time >= current_process->required_time) {
                current_process->state = FINISHED;
                printf("FINISHED)\n");
                finished_processes++;
                free(current_process);
            } else {
                printf("READY)\n");
                enqueue(current_queue, current_process);
            }
        } 

        else if (lowPriorityQueue.head) {
            current_queue = &lowPriorityQueue;
            current_process = dequeue(current_queue);
            
            // Round bin scheduling for low priority
            printf("\nSelected Process (Low Priority): %s\n", current_process->name);
            current_process->executed_time += TIME_SLICE;

            printf("After Execution: (%s, P:%d, T:%d/%d, State: ",
                  current_process->name, current_process->priority,
                  current_process->executed_time, current_process->required_time);

            if (current_process->executed_time >= current_process->required_time) {
                current_process->state = FINISHED;
                printf("FINISHED)\n");
                finished_processes++;
                free(current_process);
            } else {
                printf("READY)\n");
                enqueue(current_queue, current_process);
            }
        }

        printf("Current Queues State:\n");
        printQueue(&highPriorityQueue, "High Priority");
        printQueue(&lowPriorityQueue, "Low Priority");
    }

    printf("\nAll processes have finished execution.\n");
    return 0;
}
