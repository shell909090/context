/* @(#)s_context.c
 */

#include <stdio.h>
#include <ucontext.h>

int max = 0;
static ucontext_t uctx_main, uctx_local;

static void context_local()
{
	int i;
	for (i = 0; i < max; i++) {
		swapcontext(&uctx_local, &uctx_main);
		/* printf("swap local: %d.\n", i); */
	}
	/* printf("local return.\n"); */
	max = 0;
	swapcontext(&uctx_local, &uctx_main);
}

int main(int argc, char *argv[])
{
	char local_stack[16384];

	if (argc < 2) {
		printf("s_context times.\n");
		return -1;
	}
	max = atoi(argv[1]);

	if (getcontext(&uctx_local) == -1) {
		perror("getcontext");
		return -1;
	}
	uctx_local.uc_stack.ss_sp = local_stack;
	uctx_local.uc_stack.ss_size = sizeof(local_stack);
	uctx_local.uc_link = &uctx_main;
	makecontext(&uctx_local, context_local, 0);
	/* printf("makecontext.\n"); */

	while (max) {
		if (swapcontext(&uctx_main, &uctx_local) == -1) {
			perror("swapcontext");
			return -1;
		}
		/* printf("swap main.\n"); */
	}

	/* printf("quit.\n"); */
	return;
}
