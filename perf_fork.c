/* @(#)perf_fork.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sched.h>
#include <signal.h>

void sighandler_chld(int signum)
{
	int pid;
	if (signum != SIGCHLD) {
		return;
	}

	pid = wait(NULL);
	if (pid == -1 && errno != ECHILD) {
		perror("waitpid");
		exit(-1);
	}

	return;
}

int main(int argc, char *argv[])
{
	int i, n;
	int pid;

	if (argc < 2) {
		printf("perf_fork times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	/* signal(SIGCHLD, sighandler_chld); */

	for (i = 0; i < n; i++) {
		pid = fork();
		if (pid == 0) {
			return 0;
		}
		if (pid > 0) {
			/* 注意这一句，实际上是强迫优先执行子进程 */
			sched_yield();
			continue;
		}
		if (errno == 11) {
			do {
				pid = wait(NULL);
				if (pid == -1 && errno != ECHILD) {
					perror("waitpid");
					return -1;
				}
			} while (pid != -1 && errno != ECHILD);
			i -= 1;
			continue;
		}
		perror("fork");
		return -1;
	}
	return 0;
}
