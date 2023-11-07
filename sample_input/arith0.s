	.data
result0:	.word	0x00000000
result1:	.word	0
	.text
main:
	addi	$8, $0, 1
	addi	$9, $0, -4
	add	$16, $0, $8
	addi	$16, $16, 2
	sub	$16, $16, $9
	subi	$16, $16, -8
    la  $10, result0
	sw	$16, 0($10)
