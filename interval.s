	.file	"interval.c"
	.text
	.globl	interval_add
	.type	interval_add, @function
interval_add:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$40, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L2
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	add_inf
	movq	-40(%rbp), %rdx
	movq	%rax, (%rdx)
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	add_inf
	movq	-40(%rbp), %rdx
	movq	%rax, 8(%rdx)
	jmp	.L1
.L2:
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L4
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	jne	.L5
.L4:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	jne	.L6
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L5
.L6:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	jne	.L7
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L5
.L7:
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	add_inf
	movq	-40(%rbp), %rdx
	movq	%rax, (%rdx)
	movq	-40(%rbp), %rax
	movabsq	$9223372036854775807, %rcx
	movq	%rcx, 8(%rax)
	jmp	.L1
.L5:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L8
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	jne	.L9
.L8:
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	jne	.L10
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L9
.L10:
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	jne	.L11
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L9
.L11:
	movq	-40(%rbp), %rax
	movabsq	$-9223372036854775808, %rbx
	movq	%rbx, (%rax)
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	add_inf
	movq	-40(%rbp), %rdx
	movq	%rax, 8(%rdx)
	jmp	.L1
.L9:
	movq	-40(%rbp), %rax
	movabsq	$-9223372036854775808, %rcx
	movq	%rcx, (%rax)
	movq	-40(%rbp), %rax
	movabsq	$9223372036854775807, %rbx
	movq	%rbx, 8(%rax)
.L1:
	addq	$40, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	interval_add, .-interval_add
	.globl	interval_sub
	.type	interval_sub, @function
interval_sub:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$40, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L13
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	sub_inf
	movq	-40(%rbp), %rdx
	movq	%rax, (%rdx)
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	sub_inf
	movq	-40(%rbp), %rdx
	movq	%rax, 8(%rdx)
	jmp	.L12
.L13:
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L15
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	jne	.L16
.L15:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	jne	.L17
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L16
.L17:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	jne	.L18
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L16
.L18:
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	sub_inf
	movq	-40(%rbp), %rdx
	movq	%rax, (%rdx)
	movq	-40(%rbp), %rax
	movabsq	$9223372036854775807, %rcx
	movq	%rcx, 8(%rax)
	jmp	.L12
.L16:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L19
	movq	-32(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	jne	.L20
.L19:
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	jne	.L21
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L20
.L21:
	movq	-24(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	jne	.L22
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L20
.L22:
	movq	-40(%rbp), %rax
	movabsq	$-9223372036854775808, %rbx
	movq	%rbx, (%rax)
	movq	-32(%rbp), %rax
	movq	(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	sub_inf
	movq	-40(%rbp), %rdx
	movq	%rax, 8(%rdx)
	jmp	.L12
.L20:
	movq	-40(%rbp), %rax
	movabsq	$-9223372036854775808, %rcx
	movq	%rcx, (%rax)
	movq	-40(%rbp), %rax
	movabsq	$9223372036854775807, %rbx
	movq	%rbx, 8(%rax)
.L12:
	addq	$40, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	interval_sub, .-interval_sub
	.globl	interval_mul
	.type	interval_mul, @function
interval_mul:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	jns	.L24
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jg	.L25
.L24:
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	jns	.L26
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	js	.L25
.L26:
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jle	.L27
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jg	.L25
.L27:
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jle	.L28
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	js	.L25
.L28:
	movq	-56(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-56(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-56(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-56(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L29
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L29
.L25:
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rax, %rbx
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_min
	movq	%rax, -40(%rbp)
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rax, %rbx
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_min
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rdx
	movq	-40(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	interval_value_min
	movq	%rax, -40(%rbp)
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rax, %rbx
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_max
	movq	%rax, -24(%rbp)
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rax, %rbx
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	mul_inf
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_max
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rdx
	movq	-24(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	interval_value_max
	movq	%rax, -24(%rbp)
	movq	-72(%rbp), %rax
	movq	-40(%rbp), %rdx
	movq	%rdx, (%rax)
	movq	-72(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	%rdx, 8(%rax)
	jmp	.L23
.L29:
	movq	-72(%rbp), %rax
	movabsq	$-9223372036854775808, %rcx
	movq	%rcx, (%rax)
	movq	-72(%rbp), %rax
	movabsq	$9223372036854775807, %rcx
	movq	%rcx, 8(%rax)
.L23:
	addq	$72, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	interval_mul, .-interval_mul
	.globl	interval_div
	.type	interval_div, @function
interval_div:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$72, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	-64(%rbp), %rax
	movq	(%rax), %rdx
	movabsq	$-9223372036854775808, %rax
	cmpq	%rax, %rdx
	je	.L32
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	js	.L33
.L32:
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jle	.L34
	movq	-64(%rbp), %rax
	movq	8(%rax), %rdx
	movabsq	$9223372036854775807, %rax
	cmpq	%rax, %rdx
	je	.L34
.L33:
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	floor
	cvttsd2siq	%xmm0, %rbx
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	floor
	cvttsd2siq	%xmm0, %rax
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_min
	movq	%rax, -40(%rbp)
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	floor
	cvttsd2siq	%xmm0, %rbx
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	floor
	cvttsd2siq	%xmm0, %rax
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_min
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rdx
	movq	-40(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	interval_value_min
	movq	%rax, -40(%rbp)
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	ceil
	cvttsd2siq	%xmm0, %rbx
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	ceil
	cvttsd2siq	%xmm0, %rax
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_max
	movq	%rax, -24(%rbp)
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	ceil
	cvttsd2siq	%xmm0, %rbx
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	cvtsi2sdq	%rax, %xmm0
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm1, %xmm0
	call	ceil
	cvttsd2siq	%xmm0, %rax
	movq	%rbx, %rsi
	movq	%rax, %rdi
	call	interval_value_max
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rdx
	movq	-24(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	interval_value_max
	movq	%rax, -24(%rbp)
	movq	-72(%rbp), %rax
	movq	-40(%rbp), %rdx
	movq	%rdx, (%rax)
	movq	-72(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	%rdx, 8(%rax)
	jmp	.L31
.L34:
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jg	.L36
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	js	.L36
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	jns	.L36
	movq	-72(%rbp), %rax
	movabsq	$-9223372036854775808, %rcx
	movq	%rcx, (%rax)
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	negq	%rax
	movq	%rax, %rdx
	movq	-72(%rbp), %rax
	movq	%rdx, 8(%rax)
	jmp	.L31
.L36:
	movq	-64(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jg	.L37
	movq	-64(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	js	.L37
	movq	-56(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jle	.L37
	movq	-56(%rbp), %rax
	movq	8(%rax), %rax
	negq	%rax
	movq	%rax, %rdx
	movq	-72(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-72(%rbp), %rax
	movabsq	$9223372036854775807, %rcx
	movq	%rcx, 8(%rax)
	jmp	.L31
.L37:
	movq	-72(%rbp), %rax
	movabsq	$-9223372036854775808, %rcx
	movq	%rcx, (%rax)
	movq	-72(%rbp), %rax
	movabsq	$9223372036854775807, %rcx
	movq	%rcx, 8(%rax)
.L31:
	addq	$72, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	interval_div, .-interval_div
	.ident	"GCC: (Ubuntu 4.8.2-19ubuntu1) 4.8.2"
	.section	.note.GNU-stack,"",@progbits
