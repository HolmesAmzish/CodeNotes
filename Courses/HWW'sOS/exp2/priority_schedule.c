#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define MAX_NAME_LEN 3
#define MAX_LINE_LEN 50

typedef enum {
    READY,
    FINISHED
} ProcessState;

typedef struct PCB {
    char name[MAX_NAME_LEN + 1];
    int required_time;
    int priority;
    ProcessState state;
    struct PCB *next;
} PCB;

PCB *head = NULL;

PCB *createPCB(const char *name, int required_time, int priority) {
    PCB *newPCB = (PCB *)malloc(sizeof(PCB));
    if (newPCB == NULL) {
        perror("Failed to allocate memory for PCB");
        exit(EXIT_FAILURE);
    }
    strncpy(newPCB->name, name, MAX_NAME_LEN);
    newPCB->name[MAX_NAME_LEN] = '\0';
    newPCB->required_time = required_time;
    newPCB->priority = priority;
    newPCB->state = READY;
    newPCB->next = NULL;
    return newPCB;
}

void insertPCB(PCB *newPCB) {
    if (head == NULL || newPCB->priority > head->priority) {
        newPCB->next = head;
        head = newPCB;
    } else {
        PCB *current = head;
        while (current->next != NULL && current->next->priority >= newPCB->priority) {
            current = current->next;
        }
        newPCB->next = current->next;
        current->next = newPCB;
    }
}

PCB *removeHeadPCB() {
    if (head == NULL) {
        return NULL;
    }
    PCB *temp = head;
    head = head->next;
    return temp;
}

void printQueue() {
    printf("Queue: ");
    PCB *current = head;
    while (current != NULL) {
        printf("(%s, P:%d, T:%d) -> ", current->name, current->priority, current->required_time);
        current = current->next;
    }
    printf("NULL\n");
}

int readProcessesFromCSV(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Failed to open CSV file");
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINE_LEN];
    int process_count = 0;

    while (fgets(line, sizeof(line), file)) {
        char name[MAX_NAME_LEN + 1];
        int required_time, priority;

        if (sscanf(line, "%3[^,],%d,%d", name, &required_time, &priority) == 3) {
            PCB *newPCB = createPCB(name, required_time, priority);
            insertPCB(newPCB);
            process_count++;
        }
    }

    fclose(file);
    return process_count;
}

int main() {
    int process_count = readProcessesFromCSV("processes.csv");

    printf("Initial Process Queue:\n");
    printQueue();

    printf("\nProcessor Scheduling Begins:\n");

    int finished_count = 0;
    while (head != NULL) {
        PCB *current_process = removeHeadPCB();

        printf("\nSelected Process: %s\n", current_process->name);
        printf("Before Execution: (%s, P:%d, T:%d, State: READY)\n", 
               current_process->name, current_process->priority, current_process->required_time);

        current_process->priority--;
        current_process->required_time--;

        printf("After Execution: (%s, P:%d, T:%d, State: ", 
               current_process->name, current_process->priority, current_process->required_time);

        if (current_process->required_time > 0) {
            printf("READY)\n");
            insertPCB(current_process);
        } else {
            current_process->state = FINISHED;
            printf("FINISHED)\n");
            finished_count++;
            free(current_process);
        }

        printf("Current Process Queue State:\n");
        printQueue();

        if (finished_count == process_count) {
            printf("\nAll processes have finished execution.\n");
            break;
        }
    }

    return 0;
}
