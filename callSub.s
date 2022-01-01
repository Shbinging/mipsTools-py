init:addi $esp, $0, 252
    beq $0, $0, main

func:sw $30, $esp, 0
    lw $5, $esp, 8 // $5 == 1
    lw $6, $esp, 4 //$6 == 2
    sub $30, $5, $6
    lw $5, $esp, 0
    jalr $0, $5, $0


main:addi $1, $0, 1
    addi $2, $0, 2
    sw $1, $esp, 0
    sw $2, $esp, -4
    addi $esp, $esp, -8
    addi $3, $0, func
    jalr $30, $3, $0
    addi $esp, $esp, 8
    addi $4, $30, 0
