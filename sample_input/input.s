	.data
result0:	.word	0x00000000
result1:	.word	0
	.text
main:
	addi	$8, $0, 1
	addi	$9, $0, -4
    addi    $11, $0, 4
    addu    $11, $11, -2
    subu    $11, $11, -2
	addu	$16, $0, $8
	addiu	$16, $16, 32767
	subu	$16, $16, $9
	subiu	$16, $16, -32768
    la  $10, result0
	sw	$16, 0($10)
