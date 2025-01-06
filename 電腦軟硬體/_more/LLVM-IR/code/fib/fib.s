	.text
	.def	 @feat.00;
	.scl	3;
	.type	0;
	.endef
	.globl	@feat.00
.set @feat.00, 0
	.file	"fib.c"
	.def	 fib;
	.scl	2;
	.type	32;
	.endef
	.globl	fib                             # -- Begin function fib
	.p2align	4, 0x90
fib:                                    # @fib
.seh_proc fib
# %bb.0:
	subq	$56, %rsp
	.seh_stackalloc 56
	.seh_endprologue
	movl	%ecx, 48(%rsp)
	cmpl	$0, 48(%rsp)
	je	.LBB0_2
# %bb.1:
	cmpl	$1, 48(%rsp)
	jne	.LBB0_3
.LBB0_2:
	movl	$1, 52(%rsp)
	jmp	.LBB0_4
.LBB0_3:
	movl	48(%rsp), %eax
	subl	$1, %eax
	movl	%eax, %ecx
	callq	fib
	movl	48(%rsp), %ecx
	subl	$2, %ecx
	movl	%eax, 44(%rsp)                  # 4-byte Spill
	callq	fib
	movl	44(%rsp), %ecx                  # 4-byte Reload
	addl	%eax, %ecx
	movl	%ecx, 52(%rsp)
.LBB0_4:
	movl	52(%rsp), %eax
	addq	$56, %rsp
	retq
	.seh_handlerdata
	.text
	.seh_endproc
                                        # -- End function
	.addrsig
	.addrsig_sym fib
