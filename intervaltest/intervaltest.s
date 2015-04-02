	.file	"intervaltest.c"
	.section	.rodata
.LC0:
	.string	"\n"
	.text
	.globl	add
	.type	add, @function
add:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	add, .-add
	.section	.rodata
.LC1:
	.string	"%d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$64, %rsp
	movl	%edi, -52(%rbp)
	movl	$12, -48(%rbp)
	movl	$6, -40(%rbp)
	movl	$32767, -44(%rbp)
	movl	-40(%rbp), %eax
	movl	-48(%rbp), %edx
	addl	%edx, %eax
	imull	-40(%rbp), %eax
	subl	-48(%rbp), %eax
	movl	%eax, -44(%rbp)
	cmpl	$0, -52(%rbp)
	jle	.L3
	cmpl	$49, -44(%rbp)
	jg	.L3
	jmp	.L4
.L5:
	addl	$5, -44(%rbp)
.L4:
	cmpl	$99, -44(%rbp)
	jle	.L5
	jmp	.L6
.L3:
	subl	$1, -44(%rbp)
.L6:
	cmpl	$5, -48(%rbp)
	jne	.L7
	addl	$1, -48(%rbp)
	movl	-48(%rbp), %eax
	cltd
	shrl	$31, %edx
	addl	%edx, %eax
	andl	$1, %eax
	subl	%edx, %eax
	movl	%eax, -40(%rbp)
.L7:
	movq	$0, -24(%rbp)
	movq	-24(%rbp), %rax
	movl	$5, (%rax)
	movq	-24(%rbp), %rax
	movl	$10, 4(%rax)
	movl	$4, %edi
	movl	$0, %eax
	call	malloc
	cltq
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movl	(%rax), %eax
	cmpl	$5, %eax
	je	.L8
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
.L8:
	movl	$5, -36(%rbp)
	movl	$10, -32(%rbp)
	cmpl	$4, -28(%rbp)
	jne	.L9
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
.L9:
	movl	-44(%rbp), %edx
	movl	-52(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	add
	movl	-48(%rbp), %edx
	movl	%edx, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	sub
	movl	%eax, -48(%rbp)
	jmp	.L10
.L14:
	movl	-48(%rbp), %eax
	cmpl	$3, %eax
	je	.L12
	cmpl	$8, %eax
	je	.L13
	jmp	.L16
.L12:
	movl	-44(%rbp), %edx
	movl	-52(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	sub
	jmp	.L10
.L13:
	movl	-44(%rbp), %edx
	movl	-52(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	add
	movl	$6, -44(%rbp)
	jmp	.L10
.L16:
	movl	$5, -52(%rbp)
.L10:
	cmpl	$0, -52(%rbp)
	jg	.L14
	movl	-44(%rbp), %eax
	movl	%eax, %esi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
