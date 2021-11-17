//init
addi $1, $0, 1 //a
addi $2, $0, 1 //b
addi $4, $0, 3 //n
//if n < 3
addi $5, $0, 3 //$5 = 3
slt $5, $4, $5 //if (n < 3) $5 == 1
bne $5, $0, ans1 //if n < 3 goto ans1
//if n >= 3
//for(int i = n - 3; i; i --)
addi $6, $4, -1// i($6) == n - 3
branch:bltz $6, $0, end
//tmp = a + b; a = b; b = tmp;
add $7, $1, $2 //tmp($7) = a + b
addi $1, $2, 0 // a = b
addi $2, $7, 0 // b = tmp

beq $0, $0, branch//goto branch

//if n < 3
ans1:addi $10, $0, $1 //ans($10) = 1
beq $0, $0, end
//terminate
end:halt