#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_CHAIRS 5
#define NUM_CUSTOMERS 10

sem_t mutex;
sem_t customer_comes;
sem_t barber_ready;

int available_chairs = NUM_CHAIRS;
int barber_running = 1; // Flag for barber thread

void *barber(void *arg) {
    while (barber_running) {
        if (sem_wait(&customer_comes) != 0) {
            break; // Exit if sem_wait fails (likely due to cancellation)
        }
        
        sem_wait(&mutex);
        available_chairs++;
        printf("Barber: Calls a customer in, %d chair(s) left.\n", available_chairs);
        sem_post(&barber_ready);
        sem_post(&mutex);
        
        printf("Barber: Cutting hair...\n");
        sleep(3);
        printf("Barber: Haircut finished.\n");
    }
    pthread_exit(0);
}

void *customer(void *arg) {
    int id = *(int *)arg;
    sleep(rand() % 3);
    printf("Customer %d: Arrived\n", id);
    
    sem_wait(&mutex);
    if (available_chairs > 0) {
        available_chairs--;
        printf("Customer %d: Waiting, %d chair(s) left.\n", id, available_chairs);
        sem_post(&customer_comes);
        sem_post(&mutex);
        
        sem_wait(&barber_ready);
        printf("Customer %d: Entered\n", id);
    } else {
        sem_post(&mutex);
        printf("Customer %d: No chairs available, left the barber\n", id);
    }
    pthread_exit(0);
}

int main() {
    pthread_t barber_thread;
    pthread_t customer_threads[NUM_CUSTOMERS];
    int customer_ids[NUM_CUSTOMERS];
    
    if (sem_init(&mutex, 0, 1) != 0 ||
        sem_init(&customer_comes, 0, 0) != 0 ||
        sem_init(&barber_ready, 0, 0) != 0) {
        perror("Semaphore initialization failed");
        return 1;
    }
    
    if (pthread_create(&barber_thread, NULL, barber, NULL) != 0) {
        perror("Barber thread creation failed");
        return 1;
    }
    
    for (int i = 0; i < NUM_CUSTOMERS; i++) {
        customer_ids[i] = i + 1;
        if (pthread_create(&customer_threads[i], NULL, customer, &customer_ids[i]) != 0) {
            perror("Customer thread creation failed");
            return 1;
        }
        sleep(1);
    }
    
    for (int i = 0; i < NUM_CUSTOMERS; i++) {
        if (pthread_join(customer_threads[i], NULL) != 0) {
            perror("Customer thread join failed");
            return 1;
        }
    }
    
    barber_running = 0; // Signal barber to exit
    sem_post(&customer_comes); // In case barber is waiting.
    if (pthread_join(barber_thread, NULL) != 0) {
        perror("Barber thread join failed");
        return 1;
    }
    
    if (sem_destroy(&mutex) != 0 ||
        sem_destroy(&customer_comes) != 0 ||
        sem_destroy(&barber_ready) != 0) {
        perror("Semaphore destruction failed");
        return 1;
    }
    
    return 0;
}