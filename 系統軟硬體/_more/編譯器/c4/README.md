# C4 -- 500 行的 C 語言編譯器 

C in four functions (陳鍾誠獨立出一個 vm 函數，於是變五個函數)

* 修改者 -- 陳鍾誠
* 作者 -- https://github.com/rswier/
* 來源 -- https://github.com/rswier/c4
* 原理說明 -- [doc](doc)

## 使用方式


```

$ gcc -w c4.c -o c4


$ ./c4 test/hello.c
hello, world
exit(0) cycle = 9


$ ./c4 test/sum.c
sum(10)=55
exit(0) cycle = 303
```

## 印出組合語言 (堆疊機)

```

$ ./c4 -s test/sum.c
1: #include <stdio.h>
2:
3: // sum(n) = 1+2+...+n
4: int sum(int n) {
5:   int s;
6:   int i;
7:   s=0;
 4653208     ENT  2
 4653224     LEA  -1
 4653240     PSH
 4653248     IMM  0
 4653264     SI
8:   i=1;
 4653272     LEA  -2
 4653288     PSH
 4653296     IMM  1
 4653312     SI
9:   while (i <= n) {
 4653320     LEA  -2
 4653336     LI
 4653344     PSH
 4653352     LEA  2
 4653368     LI
 4653376     LE
 4653384     BZ   0
10:     s = s + i;
 4653400     LEA  -1
 4653416     PSH
 4653424     LEA  -1
 4653440     LI
 4653448     PSH
 4653456     LEA  -2
 4653472     LI
 4653480     ADD
 4653488     SI
11:     i ++;
 4653496     LEA  -2
 4653512     PSH
 4653520     LI
 4653528     PSH
 4653536     IMM  1
 4653552     ADD
 4653560     SI
 4653568     PSH
 4653576     IMM  1
 4653592     SUB
12:   }
13:   return s;
 4653600     JMP  4653320
 4653616     LEA  -1
 4653632     LI
 4653640     LEV
14: }
 4653648     LEV
15:
16: int main() {
17:   printf("sum(10)=%d\n", sum(10));
 4653656     ENT  0
 4653672     ADDR 4915360
 4653688     PSH
 4653696     IMM  10
 4653712     PSH
 4653720     JSR  4653208
 4653736     ADJ  1
 4653752     PSH
 4653760     PRTF
 4653768     ADJ  2
18:   return 0;
 4653784     IMM  0
 4653800     LEV
19: }
 4653808     LEV
```

## 自我編譯

```

$ ./c4 c4.c test/sum.c
sum(10)=55
exit(0) cycle = 303
exit(0) cycle = 90964


$ ./c4 c4.c c4.c test/sum.c
sum(10)=55
exit(0) cycle = 303
exit(0) cycle = 90964
exit(0) cycle = 17230772
```

## Linux 使用

```
$ gcc -m32 c4.c -o c4
$ ./c4 test/hello.c
hello, world
exit(0) cycle = 9
```
