/* @(#)s_context.c
 */

#include <stdio.h>
#include <ucontext.h>

int i = 0;

int main(int argc, char *argv[])
{
	int n;
	ucontext_t context;

	if (argc < 2) {
		printf("s_context times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	getcontext(&context);
	if (i < n) {
		i++;
		setcontext(&context);
	}

	return 0;
}
