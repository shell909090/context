/* @(#)t_thread.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <pthread.h>

static void * thread_main(void *arg)
{
	return NULL;
}

int main(int argc, char *argv[])
{
	int i, n;
	int st;
	pthread_attr_t attr;
	pthread_t tid;

	if (argc < 2) {
		printf("t_thread times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	st = pthread_attr_init(&attr);
	if (st != 0) {
		perror("pthread_attr_init");
		return -1;
	}

	for (i = 0; i < n; i++) {
		st = pthread_create(&tid, &attr, thread_main, NULL);
		if (st != 0) {
			printf("i: %d.\n", i);
			perror("pthread_create");
			return -1;
		}
		/* 注意，这就是优先执行子进程模式。 */
		st = pthread_join(tid, NULL);
		if (st != 0) {
			perror("pthread_join");
			return -1;
		}
	}
	return 0;
}
