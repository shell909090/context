/* @(#)s_syscall.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <sys/syscall.h>

int main(int argc, char *argv[])
{
	int i, n;
	pid_t pid;

	if (argc < 2) {
		printf("s_syscall times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	for (i = 0; i < n; i++) {
		pid = syscall(SYS_getpid);
		/* pid = getpid(); */
	}
	
	return 0;
}
