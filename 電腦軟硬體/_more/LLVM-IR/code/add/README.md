
```
$ clang -S -emit-llvm add.c

$ clang add.ll main.c -o main

$ ./main
add(3,5)=8

```