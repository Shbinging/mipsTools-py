init:beq $0, $0, main
//$23 a
//$22 b
//$21 s
//$20 i
multi:addi $21, $0, 0
    addi $20, $0, 0
    lpi:addi $21, $23, 0
        addi $20, $20, 1
        bne $22, $20, lpi
    beq $0, $0, gIdx

//$29 i
//$28 j
//$27 k1
//$26 k2
//$25 k3
//$24 k4
//$23 back
gIdx:addi $27, $29, 2
    addi $26, $29, -1
    addi $23, $29, 2
    addi $22, $28, -1
    beq $0, $0, multi
    addi $25, $21, 0
    srl $25, $0, $25, 1
    add $24, $25, $28
    jalr $0, $23, $0
    

//$1 n
//$2 i
//$3 j
//$4 c1
//$5 c2
//$6 c3
//$31 tmpi = n + 1
//$30 tmpj = i + 1
main:addi $1, $0, 3 //n = 3
    addi $31, $1, 1
    addi $2, $0, 1 // i = 0
    lpI:addi $3, $0, 0 //j = 0
            addi $30, $2, 1
            lpJ:subi $4, $2, 1
                subi $5, $3, 0
                sub $6, $3, $2
                
                addi $3, $3, 1
                bne $3, $30, lpJ

        addi $2, $2, 1
        bne $1, $31, lpI
