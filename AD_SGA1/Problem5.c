/*
 * Problem 5: Job Sequencing with Deadlines - GREEDY strategy
 * ----------------------------------------------------------
 * Strategy: Greedy by decreasing profit, with latest-slot placement.
 *
 * Why greedy is correct:
 *   Each job takes one unit of time. Considering jobs from highest profit
 *   downward, and scheduling each as LATE as possible (at the latest free
 *   slot on or before its deadline) keeps earlier slots open for other
 *   jobs with tighter deadlines. An exchange argument shows this never
 *   loses profit, so the greedy schedule is optimal.
 *
 * Time complexity:
 *   O(n log n) to sort by profit + O(n * maxDeadline) for slot search
 *   = O(n^2) in the worst case with linear slot scanning.
 * Space complexity: O(maxDeadline) for the time-slot table.
 */

#include <stdio.h>

typedef struct {
    char name[8];
    int  deadline;
    int  profit;
} Job;

/* Sort jobs by DECREASING profit (selection sort). */
void sortByProfitDesc(Job jobs[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int best = i;
        for (int j = i + 1; j < n; j++)
            if (jobs[j].profit > jobs[best].profit) best = j;
        if (best != i) {
            Job tmp = jobs[i];
            jobs[i] = jobs[best];
            jobs[best] = tmp;
        }
    }
}

int main(void) {
    /* Given jobs. */
    Job jobs[] = {
        {"J1", 2, 100},
        {"J2", 1,  19},
        {"J3", 2,  27},
        {"J4", 1,  25},
        {"J5", 3,  15}
    };
    int n = (int)(sizeof(jobs) / sizeof(jobs[0]));

    /* Step 1: sort jobs by decreasing profit. */
    sortByProfitDesc(jobs, n);

    /* Find the maximum deadline to size the time-slot table. */
    int maxDeadline = 0;
    for (int i = 0; i < n; i++)
        if (jobs[i].deadline > maxDeadline) maxDeadline = jobs[i].deadline;

    /* slot[t] holds the index of the job scheduled in time unit t (1-based),
       or -1 if the slot is free. */
    int slot[maxDeadline + 1];
    for (int t = 1; t <= maxDeadline; t++) slot[t] = -1;

    int totalProfit = 0;

    /* Step 2: place each job in the LATEST free slot <= its deadline. */
    for (int i = 0; i < n; i++) {
        for (int t = jobs[i].deadline; t >= 1; t--) {
            if (slot[t] == -1) {
                slot[t] = i;
                totalProfit += jobs[i].profit;
                break;
            }
        }
    }

    /* Step 3: report the schedule. */
    printf("Time slot -> Job (profit):\n");
    for (int t = 1; t <= maxDeadline; t++) {
        if (slot[t] != -1)
            printf("  Slot %d : %s (profit %d)\n",
                   t, jobs[slot[t]].name, jobs[slot[t]].profit);
        else
            printf("  Slot %d : (idle)\n", t);
    }

    printf("\nFinal job sequence: ");
    for (int t = 1; t <= maxDeadline; t++)
        if (slot[t] != -1) printf("%s ", jobs[slot[t]].name);
    printf("\n");

    printf("Total profit: %d\n", totalProfit);
    /* Expected: sequence J3, J1, J5 with total profit 142. */
    return 0;
}
