#include<bits/stdc++.h> 
int dataMem[64];
int n = 5;
int multi(int a, int b)
{
    int s = 0;
    for (int i = 1; i <= b; i++){
        s = s + a;
    }
    return s;
}

int getIndex(int i, int j)
{
    int k1 = i + 2;
    int k2 = i - 1;
    int k3 = multi(i + 2, i - 1);
    k3 = k3 >> 1;
    int k4 = k3 + j;
    return k4;
}

int main()
{
    for (int i = 1; i <= n; i++)
    {
        for (int j = 0; j <= i; j++)
        {
            int c1 = (i == 1);
            int c2 = (j == 0);
            int c3 = (j == i);
            c3 |= c1;
            c3 |= c2;
            int curIndex = getIndex(i, j);
            int preIndex1, preIndex2;
            if (c3 == 1){
                dataMem[curIndex] = 1;
            }else{
                preIndex1 = getIndex(i - 1, j);
                preIndex2 = getIndex(i - 1, j - 1);
                dataMem[curIndex] += dataMem[preIndex1];
                dataMem[curIndex] += dataMem[preIndex2];
            }
        }
    }
    for(int i = 0; i < 30; i++){
    	printf("%d ", dataMem[i]);
	}
}
