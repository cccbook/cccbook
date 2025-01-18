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
#define OP_HALT 6

// 定義指令結構體
struct instruction {
    int opcode;
    int operand;
};

// 定義程序
struct instruction program[] = {
    { OP_PUSH, 2 },
    { OP_PUSH, 3 },
    { OP_ADD, 0 },
    { OP_PUSH, 4 },
    { OP_MUL, 0 },
    { OP_HALT, 0 },
};

// 虛擬機的運行函數
void run() {
    int ip = 0; // 指令指針
    struct instruction current;

    while (1) {
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
            case OP_HALT:
                return; // 執行 HALT 操作，終止程序
            default:
                printf("Unknown opcode: %d\n", current.opcode);
                return;
        }
    }
}

int main() {
    run(); // 運行虛擬機

    printf("Result: %d\n", stack[sp]); // 輸出計算結果

    return 0;
}
