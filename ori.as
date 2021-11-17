//init
addi $1, $0, 0 //a
addi $2, $0, 1 //b
addi $4, $0, 10 //n
//if n < 3
addi $5, $0, 3 //$5 = 3
slt $5, $4, $5 //if (n < 3) $5 == 1
bne $5, $0, ans1 //if n < 3 goto ans1
//if n >= 3
//for(int i = n - 3; i; i --)
addi $6, $4, -3// i($6) == n - 3
branch:bltz $0, $6, end
//tmp = a + b; a = b; b = tmp;
add $7, $1, $2 //tmp($7) = a + b
addi $1, $2, 0 // a = b
addi $2, $7, 0 // b = tmp

addi $6, $6, -1//i = i - 1
beq $0, $0, branch//goto branch

ans1:addi $5, $4, -2
bltz $0, $5, ans0
addi $2, $0, 1
beq $0, $0, end

ans0:addi $2, $0, 0
//terminate
end:halt
//ans is in $2