/* @(#)s_jmp.c
 */

#include <stdio.h>
#include <setjmp.h>

int i = 0;

int main(int argc, char *argv[])
{
	int n;
	jmp_buf buf;

	if (argc < 2) {
		printf("s_jmp times.\n");
		return -1;
	}
	n = atoi(argv[1]);

	setjmp(buf);
	if (i < n) {
		i++;
		longjmp(buf, 1);
	}
	
	return 0;
}
