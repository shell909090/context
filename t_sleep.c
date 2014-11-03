/* @(#)t_sleep.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct counter {
	long max;
};

static void * thread_local(void *arg)
{
	int i;
	struct counter *c = (struct counter *) arg;
	for (i = 0; i < c->max; i++){
		/* usleep底层使用的是nanosleep内核调用，而后者在do_nanosleep中最终会调用schedule */
		/* 但是整个过程链条很长，当前任务会被标记为TASK_INTERRUPTIBLE，然后挂到timer等待队列上 */
		/* 因此usleep产生的调度开销会比yield高出很多 */
		usleep(0);
	}
	return NULL;
}

int main(int argc, char *argv[])
{
	int i, n, k;
	int st;
	pthread_attr_t attr;
	pthread_t *tid;
	struct counter c;

	if (argc < 3) {
		printf("perf_cs threads times.\n");
		return -1;
	}
	n = atoi(argv[1]);
	k = atoi(argv[2]);

	tid = malloc(sizeof(pthread_t) * k);

	st = pthread_attr_init(&attr);
	if (st != 0) {
		perror("pthread_attr_init");
		return -1;
	}

	c.max = n;

	for (i = 0; i < k; i++) {
		st = pthread_create(tid+i, &attr, thread_local, &c);
		if (st != 0) {
			printf("i: %d.\n", i);
			perror("pthread_create");
			return -1;
		}
	}

	for (i = 0; i < k; i++) {
		st = pthread_join(tid[i], NULL);
		if (st != 0) {
			perror("pthread_join");
			return -1;
		}
	}

	free(tid);
	return 0;
}
