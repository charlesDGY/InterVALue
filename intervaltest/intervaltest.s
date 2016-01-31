	.file	"intervaltest.c"
	.section	.rodata
.LC0:
	.string	"\n"
	.text
	.globl	add
	.type	add, @function
add:
.LFB2:
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
	movl	-8(%rbp), %eax
	movl	-4(%rbp), %edx
	addl	%edx, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	add, .-add
	.globl	sub
	.type	sub, @function
sub:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	-24(%rbp), %eax
	movl	-20(%rbp), %edx
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	sub, .-sub
	.section	.rodata
.LC1:
	.string	"%d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB4:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$272, %rsp
	movl	%edi, -260(%rbp)
	movl	$12, -252(%rbp)
	movl	$6, -248(%rbp)
	movl	$32767, -256(%rbp)
	movl	-248(%rbp), %eax
	movl	-252(%rbp), %edx
	addl	%edx, %eax
	imull	-248(%rbp), %eax
	subl	-252(%rbp), %eax
	movl	%eax, -256(%rbp)
	cmpl	$0, -260(%rbp)
	jle	.L6
	movl	-256(%rbp), %eax
	cmpl	$49, %eax
	jg	.L6
	jmp	.L7
.L8:
	movl	-256(%rbp), %eax
	addl	$5, %eax
	movl	%eax, -256(%rbp)
.L7:
	movl	-256(%rbp), %eax
	cmpl	$99, %eax
	jle	.L8
	jmp	.L9
.L6:
	movl	-256(%rbp), %eax
	subl	$1, %eax
	movl	%eax, -256(%rbp)
.L9:
	cmpl	$5, -252(%rbp)
	jne	.L10
	addl	$1, -252(%rbp)
	movl	-252(%rbp), %eax
	cltd
	shrl	$31, %edx
	addl	%edx, %eax
	andl	$1, %eax
	subl	%edx, %eax
	movl	%eax, -248(%rbp)
.L10:
	movl	$100, -168(%rbp)
	movl	$23, -52(%rbp)
	movl	-168(%rbp), %eax
	cmpl	$100, %eax
	jne	.L11
	movl	$3, -80(%rbp)
.L11:
	movl	$16, %edi
	call	malloc
	movq	%rax, -232(%rbp)
	movq	-232(%rbp), %rax
	movl	$5, (%rax)
	movq	-232(%rbp), %rax
	movl	$10, 4(%rax)
	movl	$4, %edi
	call	malloc
	movq	%rax, -224(%rbp)
	leaq	-256(%rbp), %rax
	movq	%rax, -224(%rbp)
	movq	-224(%rbp), %rax
	movq	%rax, -216(%rbp)
	movq	-216(%rbp), %rax
	movl	(%rax), %eax
	cmpl	$5, %eax
	je	.L12
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
.L12:
	movl	$5, -244(%rbp)
	movl	$10, -240(%rbp)
	cmpl	$4, -236(%rbp)
	jne	.L13
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
.L13:
	movl	-256(%rbp), %edx
	movl	-260(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	add
	movl	-252(%rbp), %edx
	movl	%edx, %esi
	movl	%eax, %edi
	call	sub
	movl	%eax, -252(%rbp)
	jmp	.L14
.L19:
	movl	-252(%rbp), %eax
	cmpl	$3, %eax
	je	.L16
	cmpl	$8, %eax
	je	.L17
	jmp	.L21
.L16:
	movl	-256(%rbp), %edx
	movl	-260(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	sub
	jmp	.L18
.L17:
	movl	-256(%rbp), %edx
	movl	-260(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	add
	movl	$6, -256(%rbp)
	jmp	.L18
.L21:
	movl	$0, -260(%rbp)
.L18:
	subl	$1, -260(%rbp)
.L14:
	cmpl	$0, -260(%rbp)
	jg	.L19
	movl	-256(%rbp), %eax
	movl	%eax, %esi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
