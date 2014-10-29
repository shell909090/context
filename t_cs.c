/* @(#)t_cs.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct counter {
	long cur;
	long max;
};

static void * thread_main(void *arg)
{
	struct counter *c = (struct counter *) arg;
	for (; c->cur < c->max; c->cur++){
		/* pthread_yield(); */
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

	c.cur = 0;
	c.max = n;

	for (i = 0; i < k; i++) {
		st = pthread_create(tid+i, &attr, thread_main, &c);
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
