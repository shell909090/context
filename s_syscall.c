/* @(#)perf_syscall.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
	int i, n;
	pid_t pid;

	if (argc < 2) {
		printf("perf_getpid times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	for (i = 0; i < n; i++) {
		pid = getpid();
	}
	
	return 0;
}
