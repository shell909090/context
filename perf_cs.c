/* @(#)perf_cs.c
 */

#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <pthread.h>

int main(int argc, char *argv[])
{
	int i, n;
	int st;

	if (argc < 2) {
		printf("perf_cs times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	return 0;
}
