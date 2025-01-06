#include <stdio.h>
#include <stdlib.h>

// 定義虛擬機的堆疊
#define STACK_SIZE 256
int stack[STACK_SIZE];
int sp = -1;

// 定義指令集
#define OP_PUSH 0
#define OP_POP 1
#define OP_ADD 2
#define OP_SUB 3
#define OP_MUL 4
#define OP_DIV 5
#define OP_JMP 6
#define OP_JNZ 7
#define OP_HALT 8

// 定義指令結構體
struct instruction {
    int opcode;
    int operand;
};

// 定義程序
struct instruction program[] = {
    { OP_PUSH, 0 },
    { OP_PUSH, 1 },
    { OP_ADD, 0 },
    { OP_PUSH, 2 },
    { OP_PUSH, 10 },
    { OP_JNZ, 3 },
    { OP_HALT, 0 },
};

// 虛擬機的運行函數
void run() {
    int ip = 0; // 指令指針
    struct instruction current;

    while (1) {
        printf("ip=%d\n", ip);
        current = program[ip++]; // 獲取當前指令
        switch (current.opcode) {
            case OP_PUSH:
                stack[++sp] = current.operand; // 執行 PUSH 操作
                break;
            case OP_POP:
                sp--; // 執行 POP 操作
                break;
            case OP_ADD:
                stack[sp - 1] += stack[sp]; // 執行 ADD 操作
                sp--;
                break;
            case OP_SUB:
                stack[sp - 1] -= stack[sp]; // 執行 SUB 操作
                sp--;
                break;
            case OP_MUL:
                stack[sp - 1] *= stack[sp]; // 執行 MUL 操作
                sp--;
                break;
            case OP_DIV:
                stack[sp - 1] /= stack[sp]; // 執行 DIV 操作
                sp--;
                break;
            case OP_JMP:
                ip = current.operand; // 執行 JMP 操作
                break;
            case OP_JNZ:
                if (stack[sp] != 0) {
                    ip = current.operand; // 執行 JNZ 操作
                } else {
                    sp--;
                }
                break;
            case OP_HALT:
                return; // 執行 HALT 操作，終止程序
            default:
                printf("Unknown opcode: %d\n", current.opcode);
                return;
        }
    }
}

int main() {
    // program[0].operand = (int)&program[3]; // 設置 PUSH 0 的操作數為 program[3] 的地址
    // program[5].operand = (int)&program[2]; // 設置 JNZ 的操作數為 program[2] 的地址
    // program[0].operand = 3; // 設置 PUSH 0 的操作數為 program[3] 的地址
    // program[5].operand = 2; // 設置 JNZ 的操作數為 program[2] 的地址

    run(); // 運行虛擬機

    printf("Result: %d\n", stack[sp]); // 輸出計算結果

    return 0;
}
