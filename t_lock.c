/* @(#)t_lock.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct counter {
	pthread_mutex_t lock;
	long max;
};

static void * thread_local(void *arg)
{
	int i;
	struct counter *c = (struct counter *) arg;

	pthread_mutex_lock(&c->lock);
	for (i = 0; i < c->max; i++){
		pthread_mutex_unlock(&c->lock);
		pthread_mutex_lock(&c->lock);
	}
	pthread_mutex_unlock(&c->lock);
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
	if (pthread_mutex_init(&c.lock, NULL) != 0)
	{
		perror("pthread_mutex_init");
		return 1;
	}

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

	pthread_mutex_destroy(&c.lock);
	free(tid);
	return 0;
}
