	.file	"main.c"
	.section	.rodata
.LC0:
	.string	"head_a: "
.LC1:
	.string	"[%ld,%ld] "
.LC2:
	.string	"\n"
.LC3:
	.string	"head_b: "
.LC4:
	.string	"add: "
.LC5:
	.string	"sub: "
.LC6:
	.string	"mul: "
.LC7:
	.string	"div: "
	.text
	.globl	main
	.type	main, @function
main:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$208, %rsp
	movl	%edi, -196(%rbp)
	movq	%rsi, -208(%rbp)
	movq	$0, -160(%rbp)
	movq	$0, -152(%rbp)
	movq	$1, -144(%rbp)
	movq	$6, -136(%rbp)
	movq	$7, -128(%rbp)
	movq	$9, -120(%rbp)
	movq	$11, -112(%rbp)
	movq	$13, -104(%rbp)
	movq	$14, -96(%rbp)
	movq	$19, -88(%rbp)
	movq	$0, -80(%rbp)
	movq	$0, -72(%rbp)
	movq	$1, -64(%rbp)
	movq	$2, -56(%rbp)
	movq	$2, -48(%rbp)
	movq	$2, -40(%rbp)
	movq	$2, -32(%rbp)
	movq	$2, -24(%rbp)
	movq	$14, -16(%rbp)
	movq	$17, -8(%rbp)
	movq	$0, -184(%rbp)
	movq	-160(%rbp), %rdx
	movq	-152(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -176(%rbp)
	movq	-80(%rbp), %rdx
	movq	-72(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -168(%rbp)
	movq	-96(%rbp), %rdx
	movq	-88(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-176(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-112(%rbp), %rdx
	movq	-104(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-176(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-128(%rbp), %rdx
	movq	-120(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-176(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-144(%rbp), %rdx
	movq	-136(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-176(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-176(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
	movl	$.LC0, %edi
	movl	$0, %eax
	call	printf
	jmp	.L2
.L3:
	movq	-192(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-192(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movq	-192(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
.L2:
	cmpq	$0, -192(%rbp)
	jne	.L3
	movl	$.LC2, %edi
	movl	$0, %eax
	call	printf
	movq	-16(%rbp), %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-168(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-32(%rbp), %rdx
	movq	-24(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-168(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-48(%rbp), %rdx
	movq	-40(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-168(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-64(%rbp), %rdx
	movq	-56(%rbp), %rax
	movq	%rdx, %rdi
	movq	%rax, %rsi
	call	make_node
	movq	%rax, -192(%rbp)
	movq	-192(%rbp), %rdx
	movq	-168(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert_node
	movq	-168(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
	movl	$.LC3, %edi
	movl	$0, %eax
	call	printf
	jmp	.L4
.L5:
	movq	-192(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-192(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movq	-192(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
.L4:
	cmpq	$0, -192(%rbp)
	jne	.L5
	movl	$.LC2, %edi
	movl	$0, %eax
	call	printf
	movq	-168(%rbp), %rcx
	movq	-176(%rbp), %rax
	movl	$1, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	set_set_arithmetic
	movq	%rax, -184(%rbp)
	movq	-184(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
	movl	$.LC4, %edi
	movl	$0, %eax
	call	printf
	jmp	.L6
.L7:
	movq	-192(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-192(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movq	-192(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
.L6:
	cmpq	$0, -192(%rbp)
	jne	.L7
	movl	$.LC2, %edi
	movl	$0, %eax
	call	printf
	movq	-168(%rbp), %rcx
	movq	-176(%rbp), %rax
	movl	$2, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	set_set_arithmetic
	movq	%rax, -184(%rbp)
	movq	-184(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
	movl	$.LC5, %edi
	movl	$0, %eax
	call	printf
	jmp	.L8
.L9:
	movq	-192(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-192(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movq	-192(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
.L8:
	cmpq	$0, -192(%rbp)
	jne	.L9
	movl	$.LC2, %edi
	movl	$0, %eax
	call	printf
	movq	-168(%rbp), %rcx
	movq	-176(%rbp), %rax
	movl	$3, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	set_set_arithmetic
	movq	%rax, -184(%rbp)
	movq	-184(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
	movl	$.LC6, %edi
	movl	$0, %eax
	call	printf
	jmp	.L10
.L11:
	movq	-192(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-192(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movq	-192(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
.L10:
	cmpq	$0, -192(%rbp)
	jne	.L11
	movl	$.LC2, %edi
	movl	$0, %eax
	call	printf
	movq	-168(%rbp), %rcx
	movq	-176(%rbp), %rax
	movl	$4, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	set_set_arithmetic
	movq	%rax, -184(%rbp)
	movq	-184(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
	movl	$.LC7, %edi
	movl	$0, %eax
	call	printf
	jmp	.L12
.L13:
	movq	-192(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-192(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	movl	$.LC1, %edi
	movl	$0, %eax
	call	printf
	movq	-192(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -192(%rbp)
.L12:
	cmpq	$0, -192(%rbp)
	jne	.L13
	movl	$.LC2, %edi
	movl	$0, %eax
	call	printf
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
