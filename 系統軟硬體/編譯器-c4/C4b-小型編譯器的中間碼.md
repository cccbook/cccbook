# C4b-小型編譯器的中間碼

### ccc: 以下是一個小型編譯器的中間碼解譯程式，請說明之

```cpp
#include "ir.h"

IR ir[IR_MAX];
int irTop = 0;
extern int L[]; // label => address

void irNew(IR p) {
  ir[irTop++] = p;
}

void irEmitCall(char *fname, int t1) {
  irNew((IR) {.type=IrCall, .op=fname, .t1=t1});
}

void irEmitArg(int t1) {
  irNew((IR) {.type=IrArg, .t1=t1});
}

void irEmitAssignTs(int t, char *s) {
  irNew((IR) {.type=IrAssignTs, .op="t=s", .t=t, .s=s});
}

void irEmitAssignSt(char *s, int t) {
  irNew((IR) {.type=IrAssignSt, .op="s=t", .t=t, .s=s});
}

void irEmitOp2(int t, int t1, char *op, int t2) {
  irNew((IR) {.type=IrOp2, .op=op, .t=t, .t1=t1, .t2=t2});
}

void irEmitLabel(int label) {
  // L[label] = irTop;
  irNew((IR) {.type=IrLabel, .op="label", .label=label});
}

void irEmitGoto(int label) {
  irNew((IR) {.type=IrGoto, .op="goto", .label=label});
}

void irEmitIfGoto(int t, int label) {
  irNew((IR) {.type=IrIfGoto, .op="if-goto", .t=t, .label=label});
}

void irEmitIfNotGoto(int t, int label) {
  irNew((IR) {.type=IrIfNotGoto, .op="ifnot-goto", .t=t, .label=label});
}

void irPrint(IR *p) {
  switch (p->type) {
    case IrCall: printf("call %s %d", p->op, p->t1); break;
    case IrArg:  printf("arg t%d", p->t1); break;
    case IrAssignSt: printf("%s = t%d", p->s, p->t); break;
    case IrAssignTs: printf("t%d = %s", p->t, p->s); break;
    case IrLabel: printf("(L%d)", p->label); break;
    case IrGoto: printf("goto L%d", p->label); break;
    case IrIfGoto: printf("if t%d goto L%d", p->t, p->label); break;
    case IrIfNotGoto: printf("ifnot t%d goto L%d", p->t, p->label); break;
    case IrOp2: printf("t%d = t%d %s t%d", p->t, p->t1, p->op, p->t2); break;
    default: error("ir.type %d not found!", p->type);
  }
  printf("\n");
}

void irDump() {
  printf("=======irDump()==========\n");
  for (int i=0; i<irTop; i++) {
    printf("%02d: ", i);
    irPrint(&ir[i]);
  }
}

void irPass2() {
  for (int i=0; i<irTop; i++) {
    int label = ir[i].label, type = ir[i].type;
    if (type == IrLabel) {
      assert(label != 0);
      L[label] = i;
    }
  }
}

```

這是一個編譯器的中間碼解譯程式，它是用 C 語言編寫的。這段程式碼的作用是讀取一個中間碼數組 ir，然後按照指定的順序執行每個指令。這個中間碼數組的元素是一個結構體 IR，它包含了指令的操作符 op、操作數 s、t、t1、t2、label 等信息。其中：

* op：表示指令的操作符，如 "+"、"="、"if-goto"、"goto" 等。
* s：表示指令的源操作數，可能是一個變量名稱，也可能是一個常數。
* t：表示指令的目的操作數，也就是計算結果要存儲的位置，它可能是一個暫存變量的索引。
* t1、t2：表示指令的其他操作數，例如 "t1 + t2"。
* label：表示指令的標籤，用於 "goto"、"if-goto"、"ifnot-goto" 等指令。

這段程式碼使用了一些全局變量，包括：

* varList：一個 Pair 數組，用於存儲變量名和它們在 varMap 中的索引。
* varMap：一個 Map，用於實現變量名和其值的映射。
* L：一個整型數組，用於存儲標籤對應的中間碼指令的索引。
* v：一個整型數組，用於存儲變量的值。
* t：一個整型數組，用於存儲暫存變量的值，初始值都為 0。

這段程式碼還定義了一些函數，包括：

* varLookup(char *name)：用於查找變量名 name 對應的值在 v 數組中的位置。
* varAdd(char *name)：用於向 varMap 中添加一個變量名，初始值為 0。
* irOp2(int a, char *op, int b)：用於計算 a 和 b 之間的運算結果，操作符由 op 指定。
* irExec(int i)：用於執行 ir 中第 i 個指令。
* irRun()：用於遍歷 ir 數組，按照順序執行每個指令。

總體來說，這個程序是一個簡單的中間碼解譯器，它可以執行一個編譯器生成的中間碼程序。在運行過程中，它會創建一個變量映射 varMap，用於存儲變量名和變量值之間的對應關係。它還使用數組 t 存放計算結果。通過解析中間碼指令，它可以實現變量賦值、算術運算、條件判斷等基本操作，從而完成中間碼程序的執行。





