# C4 原始碼解析

ccc: C4 是一個簡化後的 C 語言編譯器，接著我會一段一段貼上 C4 原始碼，請逐段解說

ChatGPT: 好的，我會盡力解釋每段 C4 原始碼的意思。

## 主程式

```cpp
int main(int argc, char **argv) // 主程式
{
  int fd, ty, poolsz, *idmain;
  int *pc, *bp, *sp;
  int i, *t;

  --argc; ++argv;
  if (argc > 0 && **argv == '-' && (*argv)[1] == 's') { src = 1; --argc; ++argv; }
  if (argc > 0 && **argv == '-' && (*argv)[1] == 'd') { debug = 1; --argc; ++argv; }
  if (argc < 1) { printf("usage: c4 [-s] [-d] file ...\n"); return -1; }

  if ((fd = open(*argv, 0)) < 0) { printf("could not open(%s)\n", *argv); return -1; }

  poolsz = 256*1024; // arbitrary size
  if (!(sym = malloc(poolsz))) { printf("could not malloc(%d) symbol area\n", poolsz); return -1; } // 符號段
  if (!(code0 = le = e = malloc(poolsz))) { printf("could not malloc(%d) text area\n", poolsz); return -1; } // 程式段
  if (!(data0 = data = malloc(poolsz))) { printf("could not malloc(%d) data area\n", poolsz); return -1; } // 資料段
  if (!(sp = malloc(poolsz))) { printf("could not malloc(%d) stack area\n", poolsz); return -1; }  // 堆疊段

  memset(sym,  0, poolsz);
  memset(e,    0, poolsz);
  memset(data, 0, poolsz);

  op = "LEA ,IMM ,ADDR,JMP ,JSR ,BZ  ,BNZ ,ENT ,ADJ ,LEV ,LI  ,LC  ,SI  ,SC  ,PSH ,"
                           "OR  ,XOR ,AND ,EQ  ,NE  ,LT  ,GT  ,LE  ,GE  ,SHL ,SHR ,ADD ,SUB ,MUL ,DIV ,MOD ,"
                           "OPEN,READ,CLOS,PRTF,MALC,FREE,MSET,MCMP,EXIT,";
  p = "char else enum if int return sizeof while "
      "open read close printf malloc free memset memcmp exit void main";
  i = Char; while (i <= While) { next(); id[Tk] = i++; } // add keywords to symbol table
  i = OPEN; while (i <= EXIT) { next(); id[Class] = Sys; id[Type] = INT; id[Val] = i++; } // add library to symbol table
  next(); id[Tk] = Char; // handle void type
  next(); idmain = id; // keep track of main

  if (!(lp = p = malloc(poolsz))) { printf("could not malloc(%d) source area\n", poolsz); return -1; }
  if ((i = read(fd, p, poolsz-1)) <= 0) { printf("read() returned %d\n", i); return -1; }
  p[i] = 0; // 設定程式 p 字串結束符號 \0
  close(fd);

  if (prog() == -1) return -1;

  if (!(pc = (int *)idmain[Val])) { printf("main() not defined\n"); return -1; }
  if (src) return 0;

  // setup stack
  bp = sp = (int *)((int)sp + poolsz);
  *--sp = EXIT;     // call exit if main returns
  *--sp = PSH; t = sp;
  *--sp = argc;     // 把 argc,argv 放入堆疊，這樣 main(argc,argv) 才能取得到
  *--sp = (int)argv; 
  *--sp = (int)t;   // 推入返回點，於是最後 RET 時會跳回 t=sp 指定的位址，接著呼叫 EXIT 離開。
  return run(pc, bp, sp);
}
```

這段程式碼是 C4 編譯器的主程式，用於解析命令列參數、讀取程式碼、建立執行環境並執行程式。

接下來這段程式碼在檢查使用者是否輸入了指令列引數，並且在必要時設定全域變數 src 和 debug 的值，以便在程式執行時作為選項使用。

接著，如果使用者未輸入檔案名稱或輸入錯誤，則顯示使用方式並結束程式。

```cpp
  --argc; ++argv;
  if (argc > 0 && **argv == '-' && (*argv)[1] == 's') { src = 1; --argc; ++argv; }
  if (argc > 0 && **argv == '-' && (*argv)[1] == 'd') { debug = 1; --argc; ++argv; }
  if (argc < 1) { printf("usage: c4 [-s] [-d] file ...\n"); return -1; }

```

接下來，程式開啟檔案並讀入檔案內容，並分配符號段、程式段、資料段和堆疊段的記憶體空間，這些段將在編譯期間用於存放符號表、目標程式碼、資料區域和執行時堆疊。如果記憶體分配失敗，則程式將顯示錯誤訊息並退出。

```cpp
  if ((fd = open(*argv, 0)) < 0) { printf("could not open(%s)\n", *argv); return -1; }

  poolsz = 256*1024; // arbitrary size
  if (!(sym = malloc(poolsz))) { printf("could not malloc(%d) symbol area\n", poolsz); return -1; } // 符號段
  if (!(code0 = le = e = malloc(poolsz))) { printf("could not malloc(%d) text area\n", poolsz); return -1; } // 程式段
  if (!(data0 = data = malloc(poolsz))) { printf("could not malloc(%d) data area\n", poolsz); return -1; } // 資料段
  if (!(sp = malloc(poolsz))) { printf("could not malloc(%d) stack area\n", poolsz); return -1; }  // 堆疊段

  memset(sym,  0, poolsz);
  memset(e,    0, poolsz);
  memset(data, 0, poolsz);

```

接下來呼叫 prog() 進行語法剖析 parse

```cpp

  if (prog() == -1) return -1; // 呼叫 prog() 開始編譯。

  if (!(pc = (int *)idmain[Val])) { printf("main() not defined\n"); return -1; }
  if (src) return 0;
```

最後就是設定好堆疊，然後用虛擬機去執行中間碼

```cpp

  // setup stack
  bp = sp = (int *)((int)sp + poolsz);
  *--sp = EXIT;     // call exit if main returns
  *--sp = PSH; t = sp;
  *--sp = argc;     // 把 argc,argv 放入堆疊，這樣 main(argc,argv) 才能取得到
  *--sp = (int)argv; 
  *--sp = (int)t;   // 推入返回點，於是最後 RET 時會跳回 t=sp 指定的位址，接著呼叫 EXIT 離開。
  return run(pc, bp, sp); // 用虛擬機執行中間碼
```

## next(): 詞彙掃描 Lexer

```cpp
void next() // 詞彙解析 lexer
{
  char *pp;

  while (tk = *p) {
    ++p;
    if (tk == '\n') { // 換行
      if (src) {
        printf("%d: %.*s", line, p - lp, lp); // 印出該行
        lp = p; // lp = p = 新一行的原始碼開頭
        while (le < e) { // 印出上一行的所有目的碼
          printf(" %d %8.4s", le, &op[*++le * 5]);
          if (*le <= ADJ) printf(" %d\n", *++le); else printf("\n"); // ADJ 之前有一個參數，之後沒有參數。
        }
      }
      ++line;
    }
    else if (tk == '#') { // 取得 #include <stdio.h> 這類的一整行
      while (*p != 0 && *p != '\n') ++p;
    }
    else if ((tk >= 'a' && tk <= 'z') || (tk >= 'A' && tk <= 'Z') || tk == '_') { // 取得變數名稱
      pp = p - 1;
      while ((*p >= 'a' && *p <= 'z') || (*p >= 'A' && *p <= 'Z') || (*p >= '0' && *p <= '9') || *p == '_')
        tk = tk * 147 + *p++;  // 計算雜湊值
      tk = (tk << 6) + (p - pp); // 符號表的雜湊位址 ??
      id = sym;
      while (id[Tk]) { // 檢查是否碰撞 ?
        if (tk == id[Hash] && !memcmp((char *)id[Name], pp, p - pp)) { tk = id[Tk]; return; } // 沒碰撞就傳回 token
        id = id + Idsz; // 碰撞，前進到下一格。
      }
      id[Name] = (int)pp; // id.Name = ptr(變數名稱)
      id[Hash] = tk; // id.Hash = 雜湊值
      tk = id[Tk] = Id; // token = id.Tk = Id
      return;
    }
    else if (tk >= '0' && tk <= '9') { // 取得數字串
      if (ival = tk - '0') { while (*p >= '0' && *p <= '9') ival = ival * 10 + *p++ - '0'; } // 十進位
      else if (*p == 'x' || *p == 'X') { // 十六進位
        while ((tk = *++p) && ((tk >= '0' && tk <= '9') || (tk >= 'a' && tk <= 'f') || (tk >= 'A' && tk <= 'F'))) // 16 進位
          ival = ival * 16 + (tk & 15) + (tk >= 'A' ? 9 : 0);
      }
      else { while (*p >= '0' && *p <= '7') ival = ival * 8 + *p++ - '0'; } // 八進位
      tk = Num; // token = Number
      return;
    }
    else if (tk == '/') {
      if (*p == '/') { // 註解
        ++p;
        while (*p != 0 && *p != '\n') ++p; // 略過註解
      }
      else { // 除法
        tk = Div;
        return;
      }
    }
    else if (tk == '\'' || tk == '"') { // 字元或字串
      pp = data;
      while (*p != 0 && *p != tk) {
        if ((ival = *p++) == '\\') {
          if ((ival = *p++) == 'n') ival = '\n'; // 處理 \n 的特殊情況
        }
        if (tk == '"') *data++ = ival; // 把字串塞到資料段裏
      }
      ++p;
      if (tk == '"') ival = (int)pp; else tk = Num; // (若是字串) ? (ival = 字串 (在資料段中的) 指標) : (字元值)
      return;
    } // 以下為運算元 =+-!<>|&^%*[?~, ++, --, !=, <=, >=, ||, &&, ~  ;{}()],:
    else if (tk == '=') { if (*p == '=') { ++p; tk = Eq; } else tk = Assign; return; }
    else if (tk == '+') { if (*p == '+') { ++p; tk = Inc; } else tk = Add; return; }
    else if (tk == '-') { if (*p == '-') { ++p; tk = Dec; } else tk = Sub; return; }
    else if (tk == '!') { if (*p == '=') { ++p; tk = Ne; } return; }
    else if (tk == '<') { if (*p == '=') { ++p; tk = Le; } else if (*p == '<') { ++p; tk = Shl; } else tk = Lt; return; }
    else if (tk == '>') { if (*p == '=') { ++p; tk = Ge; } else if (*p == '>') { ++p; tk = Shr; } else tk = Gt; return; }
    else if (tk == '|') { if (*p == '|') { ++p; tk = Lor; } else tk = Or; return; }
    else if (tk == '&') { if (*p == '&') { ++p; tk = Lan; } else tk = And; return; }
    else if (tk == '^') { tk = Xor; return; }
    else if (tk == '%') { tk = Mod; return; }
    else if (tk == '*') { tk = Mul; return; }
    else if (tk == '[') { tk = Brak; return; }
    else if (tk == '?') { tk = Cond; return; }
    else if (tk == '~' || tk == ';' || tk == '{' || tk == '}' || tk == '(' || tk == ')' || tk == ']' || tk == ',' || tk == ':') return;
  }
}
```

這是一個編譯器的詞彙掃描器（Lexer），它將原始程式碼解析為更小的詞彙。這個函數依次讀取源代碼的每個字符，並通過 switch 語句將其分類為不同的詞彙。

讀到換行符時，它會先輸出之前的那一行代碼，再輸出之前那一行所生成的目的碼（如果有的話），並且把行數增加 1。如果讀到井號字符（#），它會略過該行中的所有內容，直到讀到換行符。如果讀到字母或下劃線字符，它會把它視為變數名稱的開始，然後依次讀取更多的字符直到遇到不屬於變數名稱的字符為止。如果讀到數字字符，它會把它視為數字串的開始，然後依次讀取更多的數字字符直到遇到不屬於數字的字符為止。如果讀到斜線字符（/），它會判斷其後面是注釋還是除法運算符。如果讀到單引號或雙引號字符，它會把它視為字元或字符串的開始，然後依次讀取更多的字符直到讀到相同的引號字符為止。最後，如果讀到其他字符，它會判斷它是運算符還是標點符號。在每種情況下，它都會將所讀取的字符轉換成一個詞彙代碼（token code），然後將其存儲在全局變數 tk 中並返回。

## expr : 運算式編譯

```cpp
void expr(int lev) // 運算式 expression, 其中 lev 代表優先等級
{
  int t, *d;

  if (!tk) { printf("%d: unexpected eof in expression\n", line); exit(-1); } // EOF
  else if (tk == Num) { *++e = IMM; *++e = ival; next(); ty = INT; } // 數值
  else if (tk == '"') { // 字串
    *++e = ADDR; *++e = ival; next();
    while (tk == '"') next();
    data = (char *)((int)data + sizeof(int) & -sizeof(int)); ty = PTR; // 用 int 為大小對齊 ??
  }
  else if (tk == Sizeof) { // 處理 sizeof(type) ，其中 type 可能為 char, int 或 ptr
    next(); if (tk == '(') next(); else { printf("%d: open paren expected in sizeof\n", line); exit(-1); }
    ty = INT; if (tk == Int) next(); else if (tk == Char) { next(); ty = CHAR; }
    while (tk == Mul) { next(); ty = ty + PTR; }
    if (tk == ')') next(); else { printf("%d: close paren expected in sizeof\n", line); exit(-1); }
    *++e = IMM; *++e = (ty == CHAR) ? sizeof(char) : sizeof(int);
    ty = INT;
  }
  else if (tk == Id) { // 處理 id ...
    d = id; next();
    if (tk == '(') { // id (args) ，這是 call
      next();
      t = 0;
      while (tk != ')') { expr(Assign); *++e = PSH; ++t; if (tk == ',') next(); } // 推入 arg
      next();
      // d[Class] 可能為 Num = 128, Fun, Sys, Glo, Loc, ...
      if (d[Class] == Sys) *++e = d[Val]; // token 是系統呼叫 ???
      else if (d[Class] == Fun) { *++e = JSR; *++e = d[Val]; } // token 是自訂函數，用 JSR : jump to subroutine 指令呼叫
      else { printf("%d: bad function call\n", line); exit(-1); }
      if (t) { *++e = ADJ; *++e = t; } // 有參數，要調整堆疊  (ADJ : stack adjust)
      ty = d[Type];
    }
    else if (d[Class] == Num) { *++e = IMM; *++e = d[Val]; ty = INT; } // 該 id 是數值
    else {
      if (d[Class] == Loc) { *++e = LEA; *++e = loc - d[Val]; } // 該 id 是區域變數，載入區域變數 (LEA : load local address)
      else if (d[Class] == Glo) { *++e = IMM; *++e = d[Val]; }  // 該 id 是全域變數，載入該全域變數 (IMM : load global address or immediate 載入全域變數或立即值)
      else { printf("%d: undefined variable\n", line); exit(-1); }
      *++e = ((ty = d[Type]) == CHAR) ? LC : LI; // LI  : load int, LC  : load char
    }
  }
  else if (tk == '(') { // (E) : 有括號的運算式 ...
    next();
    if (tk == Int || tk == Char) {
      t = (tk == Int) ? INT : CHAR; next();
      while (tk == Mul) { next(); t = t + PTR; }
      if (tk == ')') next(); else { printf("%d: bad cast\n", line); exit(-1); }
      expr(Inc); // 處理 ++, -- 的情況
      ty = t;
    }
    else {
      expr(Assign); // 處理 (E) 中的 E      (E 運算式必須能處理 (t=x) op y 的情況，所以用 expr(Assign))
      if (tk == ')') next(); else { printf("%d: close paren expected\n", line); exit(-1); }
    }
  }
  else if (tk == Mul) { // * 乘法
    next(); expr(Inc);
    if (ty > INT) ty = ty - PTR; else { printf("%d: bad dereference\n", line); exit(-1); }
    *++e = (ty == CHAR) ? LC : LI;
  }
  else if (tk == And) { // & AND
    next(); expr(Inc);
    if (*e == LC || *e == LI) --e; else { printf("%d: bad address-of\n", line); exit(-1); }
    ty = ty + PTR;
  }
  else if (tk == '!') { next(); expr(Inc); *++e = PSH; *++e = IMM; *++e = 0; *++e = EQ; ty = INT; } // NOT
  else if (tk == '~') { next(); expr(Inc); *++e = PSH; *++e = IMM; *++e = -1; *++e = XOR; ty = INT; } // Logical NOT
  else if (tk == Add) { next(); expr(Inc); ty = INT; }
  else if (tk == Sub) {
    next(); *++e = IMM;
    if (tk == Num) { *++e = -ival; next(); } else { *++e = -1; *++e = PSH; expr(Inc); *++e = MUL; } // -Num or -E
    ty = INT;
  }
  else if (tk == Inc || tk == Dec) { // ++ or --
    t = tk; next(); expr(Inc);
    if (*e == LC) { *e = PSH; *++e = LC; }
    else if (*e == LI) { *e = PSH; *++e = LI; }
    else { printf("%d: bad lvalue in pre-increment\n", line); exit(-1); }
    *++e = PSH;
    *++e = IMM; *++e = (ty > PTR) ? sizeof(int) : sizeof(char);
    *++e = (t == Inc) ? ADD : SUB;
    *++e = (ty == CHAR) ? SC : SI;
  }
  else { printf("%d: bad expression\n", line); exit(-1); }
  // 參考: https://en.wikipedia.org/wiki/Operator-precedence_parser, https://www.cnblogs.com/rubylouvre/archive/2012/09/08/2657682.html https://web.archive.org/web/20151223215421/http://hall.org.ua/halls/wizzard/pdf/Vaughan.Pratt.TDOP.pdf
  while (tk >= lev) { // "precedence climbing" or "Top Down Operator Precedence" method
    t = ty;
    if (tk == Assign) {
      next();
      if (*e == LC || *e == LI) *e = PSH; else { printf("%d: bad lvalue in assignment\n", line); exit(-1); }
      expr(Assign); *++e = ((ty = t) == CHAR) ? SC : SI;
    }
    else if (tk == Cond) {
      next();
      *++e = BZ; d = ++e;
      expr(Assign);
      if (tk == ':') next(); else { printf("%d: conditional missing colon\n", line); exit(-1); }
      *d = (int)(e + 3); *++e = JMP; d = ++e;
      expr(Cond);
      *d = (int)(e + 1);
    }
    else if (tk == Lor) { next(); *++e = BNZ; d = ++e; expr(Lan); *d = (int)(e + 1); ty = INT; }
    else if (tk == Lan) { next(); *++e = BZ;  d = ++e; expr(Or);  *d = (int)(e + 1); ty = INT; }
    else if (tk == Or)  { next(); *++e = PSH; expr(Xor); *++e = OR;  ty = INT; }
    else if (tk == Xor) { next(); *++e = PSH; expr(And); *++e = XOR; ty = INT; }
    else if (tk == And) { next(); *++e = PSH; expr(Eq);  *++e = AND; ty = INT; }
    else if (tk == Eq)  { next(); *++e = PSH; expr(Lt);  *++e = EQ;  ty = INT; }
    else if (tk == Ne)  { next(); *++e = PSH; expr(Lt);  *++e = NE;  ty = INT; }
    else if (tk == Lt)  { next(); *++e = PSH; expr(Shl); *++e = LT;  ty = INT; }
    else if (tk == Gt)  { next(); *++e = PSH; expr(Shl); *++e = GT;  ty = INT; }
    else if (tk == Le)  { next(); *++e = PSH; expr(Shl); *++e = LE;  ty = INT; }
    else if (tk == Ge)  { next(); *++e = PSH; expr(Shl); *++e = GE;  ty = INT; }
    else if (tk == Shl) { next(); *++e = PSH; expr(Add); *++e = SHL; ty = INT; }
    else if (tk == Shr) { next(); *++e = PSH; expr(Add); *++e = SHR; ty = INT; }
    else if (tk == Add) {
      next(); *++e = PSH; expr(Mul);
      if ((ty = t) > PTR) { *++e = PSH; *++e = IMM; *++e = sizeof(int); *++e = MUL;  }
      *++e = ADD;
    }
    else if (tk == Sub) {
      next(); *++e = PSH; expr(Mul);
      if (t > PTR && t == ty) { *++e = SUB; *++e = PSH; *++e = IMM; *++e = sizeof(int); *++e = DIV; ty = INT; }
      else if ((ty = t) > PTR) { *++e = PSH; *++e = IMM; *++e = sizeof(int); *++e = MUL; *++e = SUB; }
      else *++e = SUB;
    }
    else if (tk == Mul) { next(); *++e = PSH; expr(Inc); *++e = MUL; ty = INT; }
    else if (tk == Div) { next(); *++e = PSH; expr(Inc); *++e = DIV; ty = INT; }
    else if (tk == Mod) { next(); *++e = PSH; expr(Inc); *++e = MOD; ty = INT; }
    else if (tk == Inc || tk == Dec) {
      if (*e == LC) { *e = PSH; *++e = LC; }
      else if (*e == LI) { *e = PSH; *++e = LI; }
      else { printf("%d: bad lvalue in post-increment\n", line); exit(-1); }
      *++e = PSH; *++e = IMM; *++e = (ty > PTR) ? sizeof(int) : sizeof(char);
      *++e = (tk == Inc) ? ADD : SUB;
      *++e = (ty == CHAR) ? SC : SI;
      *++e = PSH; *++e = IMM; *++e = (ty > PTR) ? sizeof(int) : sizeof(char);
      *++e = (tk == Inc) ? SUB : ADD;
      next();
    }
    else if (tk == Brak) {
      next(); *++e = PSH; expr(Assign);
      if (tk == ']') next(); else { printf("%d: close bracket expected\n", line); exit(-1); }
      if (t > PTR) { *++e = PSH; *++e = IMM; *++e = sizeof(int); *++e = MUL;  }
      else if (t < PTR) { printf("%d: pointer type expected\n", line); exit(-1); }
      *++e = ADD;
      *++e = ((ty = t - PTR) == CHAR) ? LC : LI;
    }
    else { printf("%d: compiler error tk=%d\n", line, tk); exit(-1); }
  }
}

```

這是一個編譯器的程式碼，以下是對 expr 函數的說明：

函數 expr(int lev) 的作用是編譯運算式，其中 lev 代表優先級，且 expr 函數會將編譯結果存入全域變數 e 中。

expr 函數的主要工作為判斷 token 的類型，並根據其類型編譯成相應的指令，其中可能的 token 類型包括數值、字串、變數、運算符等等。此外，expr 函數還會遞迴調用自己，以處理運算符的優先級。

此外，該編譯器支援的語言中還有一些特殊的構造，例如 sizeof(type) 用於計算變量的大小、(type)expr 用於顯式類型轉換、id(args) 用於函數調用等等。expr 函數也會對這些構造進行編譯。

## stmt 陳述式編譯

```cpp
void stmt() // 陳述 statement
{
  int *a, *b;

  if (tk == If) { // if 語句
    next();
    if (tk == '(') next(); else { printf("%d: open paren expected\n", line); exit(-1); }
    expr(Assign);
    if (tk == ')') next(); else { printf("%d: close paren expected\n", line); exit(-1); }
    *++e = BZ; b = ++e;
    stmt();
    if (tk == Else) { // else 語句
      *b = (int)(e + 3); *++e = JMP; b = ++e;
      next();
      stmt();
    }
    *b = (int)(e + 1);
  }
  else if (tk == While) { // while 語句
    next();
    a = e + 1;
    if (tk == '(') next(); else { printf("%d: open paren expected\n", line); exit(-1); }
    expr(Assign);
    if (tk == ')') next(); else { printf("%d: close paren expected\n", line); exit(-1); }
    *++e = BZ; b = ++e;
    stmt();
    *++e = JMP; *++e = (int)a;
    *b = (int)(e + 1);
  }
  else if (tk == Return) { // return 語句
    next();
    if (tk != ';') expr(Assign);
    *++e = LEV;
    if (tk == ';') next(); else { printf("%d: semicolon expected\n", line); exit(-1); }
  }
  else if (tk == '{') { // 區塊 {...}
    next();
    while (tk != '}') stmt();
    next();
  }
  else if (tk == ';') { // ; 空陳述
    next();
  }
  else { // 指定 assign
    expr(Assign);
    if (tk == ';') next(); else { printf("%d: semicolon expected\n", line); exit(-1); }
  }
}

```

這段程式碼定義了一個 stmt() 函式，負責編譯 C 語言中的各種陳述式 (statement)，包括 if、while、return、區塊和指定等。

在 if 陳述式中，先檢查是否符合語法，如果是的話就編譯表達式和子陳述式，並且加入跳轉指令 (JMP) 和條件跳轉指令 (BZ)。

在 while 陳述式中，先記錄目前指令位置，再檢查是否符合語法，如果是的話就編譯表達式和子陳述式，並且加入跳轉指令 (JMP) 和條件跳轉指令 (BZ)，以實現循環。

在 return 陳述式中，先檢查是否符合語法，如果有返回值則編譯表達式，最後加入終止指令 (LEV)。

在區塊中，使用 while 迴圈逐一編譯所有子陳述式，直到遇到結束標記 ('}')。

在最後一個 else 中，編譯指定 (assign) 陳述式，先編譯表達式，再加入終止指令 (LEV)。

整個 stmt() 函式的目的是編譯一個 C 語言的陳述式，並且生成相應的指令序列，以供虛擬機執行。

## prog: 完整程式編譯

```cpp

int prog() { // 編譯整個程式 Program
  int bt, i;
  line = 1;
  next();
  while (tk) {
    bt = INT; // basetype
    if (tk == Int) next();
    else if (tk == Char) { next(); bt = CHAR; }
    else if (tk == Enum) { // enum Id? {... 列舉
      next();
      if (tk != '{') next(); // 略過 Id
      if (tk == '{') {
        next();
        i = 0; // 紀錄 enum 的目前值
        while (tk != '}') {
          if (tk != Id) { printf("%d: bad enum identifier %d\n", line, tk); return -1; }
          next();
          if (tk == Assign) { // 有 Id=Num 的情況
            next();
            if (tk != Num) { printf("%d: bad enum initializer\n", line); return -1; }
            i = ival;
            next();
          }
          id[Class] = Num; id[Type] = INT; id[Val] = i++;
          if (tk == ',') next();
        }
        next();
      }
    }
    while (tk != ';' && tk != '}') { // 掃描直到區塊結束
      ty = bt;
      while (tk == Mul) { next(); ty = ty + PTR; }
      if (tk != Id) { printf("%d: bad global declaration\n", line); return -1; }
      if (id[Class]) { printf("%d: duplicate global definition\n", line); return -1; } // id.Class 已經存在，重複宣告了！
      next();
      id[Type] = ty;
      if (tk == '(') { // function 函數定義 ex: int f( ...
        id[Class] = Fun;
        id[Val] = (int)(e + 1);
        next(); i = 0;
        while (tk != ')') { // 掃描參數直到 ...)
          ty = INT;
          if (tk == Int) next();
          else if (tk == Char) { next(); ty = CHAR; }
          while (tk == Mul) { next(); ty = ty + PTR; }
          if (tk != Id) { printf("%d: bad parameter declaration\n", line); return -1; }
          if (id[Class] == Loc) { printf("%d: duplicate parameter definition\n", line); return -1; } // 這裡的 id 會指向 hash 搜尋過的 symTable 裏的那個 (在 next 裏處理的)，所以若是該 id 已經是 Local，那麼就重複了！
          // 把 id.Class, id.Type, id.Val 暫存到 id.HClass, id.HType, id.Hval ，因為 Local 優先於 Global
          id[HClass] = id[Class]; id[Class] = Loc;
          id[HType]  = id[Type];  id[Type] = ty;
          id[HVal]   = id[Val];   id[Val] = i++;
          next();
          if (tk == ',') next();
        }
        next();
        if (tk != '{') { printf("%d: bad function definition\n", line); return -1; } // BODY 開始 {...
        loc = ++i;
        next();
        while (tk == Int || tk == Char) { // 宣告
          bt = (tk == Int) ? INT : CHAR;
          next();
          while (tk != ';') {
            ty = bt;
            while (tk == Mul) { next(); ty = ty + PTR; }
            if (tk != Id) { printf("%d: bad local declaration\n", line); return -1; }
            if (id[Class] == Loc) { printf("%d: duplicate local definition\n", line); return -1; }
            // 把 id.Class, id.Type, id.Val 暫存到 id.HClass, id.HType, id.Hval ，因為 Local 優先於 Global
            id[HClass] = id[Class]; id[Class] = Loc;
            id[HType]  = id[Type];  id[Type] = ty;
            id[HVal]   = id[Val];   id[Val] = ++i;
            next();
            if (tk == ',') next();
          }
          next();
        }
        *++e = ENT; *++e = i - loc;
        while (tk != '}') stmt();
        *++e = LEV;
        id = sym; // unwind symbol table locals (把被區域變數隱藏掉的那些 Local id 還原，恢復全域變數的符號定義)
        while (id[Tk]) {
          if (id[Class] == Loc) {
            id[Class] = id[HClass];
            id[Type] = id[HType];
            id[Val] = id[HVal];
          }
          id = id + Idsz;
        }
      }
      else {
        id[Class] = Glo;
        id[Val] = (int)data;
        data = data + sizeof(int);
      }
      if (tk == ',') next();
    }
    next();
  }
  return 0;
}

```

這段程式是一個用來編譯 C 語言程式的主程式，下面是它的工作原理：

1. 首先初始化一些變數，如行號 line 和下一個 token tk。
掃描程式中的每一個 token，根據 token 的類型來執行相應的動作。
 
2. 如果是整數或字符型變數的宣告，則記錄其類型（bt）。

3. 如果是枚舉（Enum）的宣告，則將其定義為一個整數，並將其值加 1，直到枚舉的最後一個值。

4. 如果是函數的定義，則將其類型設置為“函數”（Fun），將其地址記錄為 e+1（e 是一個指向虛擬機器指令序列的指針），並開始掃描函數的參數列表和函數體。

5. 如果是局部變數的宣告，則記錄其類型和值，並將其定義為一個局部變數（Loc）。

6. 掃描函數體，將所有語句編譯成虛擬機器指令，將其添加到指令序列中。

7. 編譯完成後，將所有被區域變數隱藏的 Local 變量還原，恢復它們在全局作用域中的符號定義。

總體來說，這段程式是一個編譯器前端，用來將源代碼編譯成一個虛擬機器指令序列，以供虛擬機器後端使用。它的主要工作包括掃描程式碼、處理變量和函數的定義，並將它們轉換成虛擬機器指令序列。

## run: 虛擬機執行

```cpp

int run(int *pc, int *bp, int *sp) { // 虛擬機 => pc: 程式計數器, sp: 堆疊暫存器, bp: 框架暫存器
  int a, cycle; // a: 累積器, cycle: 執行指令數
  int i, *t;    // temps

  cycle = 0;
  while (1) {
    i = *pc++; ++cycle;
    if (debug) {
      printf("%d> %d %.4s", cycle, pc, &op[i * 5]);
      if (i <= ADJ) printf(" %d\n", *pc); else printf("\n");
    }
    if      (i == LEA) a = (int)(bp + *pc++);                             // load local address 載入區域變數
    else if (i == IMM) a = *pc++;                                         // load immediate 載入立即值
    else if (i == ADDR) { a = *pc; pc++; }                                // load address 載入位址
    else if (i == JMP) pc = (int *)*pc;                                   // jump               躍躍指令
    else if (i == JSR) { *--sp = (int)(pc + 1); pc = (int *)*pc; }        // jump to subroutine 跳到副程式
    else if (i == BZ)  pc = a ? pc + 1 : (int *)*pc;                      // branch if zero     if (a==0) goto m[pc]
    else if (i == BNZ) pc = a ? (int *)*pc : pc + 1;                      // branch if not zero if (a!=0) goto m[pc]
    else if (i == ENT) { *--sp = (int)bp; bp = sp; sp = sp - *pc++; }     // enter subroutine   進入副程式
    else if (i == ADJ) sp = sp + *pc++;                                   // stack adjust       調整堆疊
    else if (i == LEV) { sp = bp; bp = (int *)*sp++; pc = (int *)*sp++; } // leave subroutine   離開副程式
    else if (i == LI)  a = *(int *)a;                                     // load int           載入整數
    else if (i == LC)  a = *(char *)a;                                    // load char          載入字元
    else if (i == SI)  *(int *)*sp++ = a;                                 // store int          儲存整數
    else if (i == SC)  a = *(char *)*sp++ = a;                            // store char         儲存字元
    else if (i == PSH) *--sp = a;                                         // push               推入堆疊

    else if (i == OR)  a = *sp++ |  a; // a = a OR *sp
    else if (i == XOR) a = *sp++ ^  a; // a = a XOR *sp
    else if (i == AND) a = *sp++ &  a; // ...
    else if (i == EQ)  a = *sp++ == a;
    else if (i == NE)  a = *sp++ != a;
    else if (i == LT)  a = *sp++ <  a;
    else if (i == GT)  a = *sp++ >  a;
    else if (i == LE)  a = *sp++ <= a;
    else if (i == GE)  a = *sp++ >= a;
    else if (i == SHL) a = *sp++ << a;
    else if (i == SHR) a = *sp++ >> a;
    else if (i == ADD) a = *sp++ +  a;
    else if (i == SUB) a = *sp++ -  a;
    else if (i == MUL) a = *sp++ *  a;
    else if (i == DIV) a = *sp++ /  a;
    else if (i == MOD) a = *sp++ %  a;

    else if (i == OPEN) a = open((char *)sp[1], *sp); // 開檔
    else if (i == READ) a = read(sp[2], (char *)sp[1], *sp); // 讀檔
    else if (i == CLOS) a = close(*sp); // 關檔
    else if (i == PRTF) { t = sp + pc[1]; a = printf((char *)t[-1], t[-2], t[-3], t[-4], t[-5], t[-6]); } // printf("....", a, b, c, d, e)
    else if (i == MALC) a = (int)malloc(*sp); // 分配記憶體
    else if (i == FREE) free((void *)*sp); // 釋放記憶體
    else if (i == MSET) a = (int)memset((char *)sp[2], sp[1], *sp); // 設定記憶體
    else if (i == MCMP) a = memcmp((char *)sp[2], (char *)sp[1], *sp); // 比較記憶體
    else if (i == EXIT) { printf("exit(%d) cycle = %d\n", *sp, cycle); return *sp; } // EXIT 離開
    else { printf("unknown instruction = %d! cycle = %d\n", i, cycle); return -1; } // 錯誤處理
  }
}
```


這個虛擬機執行程式可以執行一種簡化的組合語言，並且可以模擬一個簡單的電腦系統。主要的控制程式碼是一個無窮迴圈，其中 `i` 變數為當前要執行的指令，根據 `i` 的值，虛擬機會執行不同的操作。

以下是虛擬機所支援的指令集：

- `LEA`：載入區域變數的地址。
- `IMM`：載入立即值。
- `ADDR`：載入位址。
- `JMP`：跳躍指令，跳到給定的位址。
- `JSR`：跳到副程式。
- `BZ`：如果累積器的值為零，則跳轉到給定的位址。
- `BNZ`：如果累積器的值不為零，則跳轉到給定的位址。
- `ENT`：進入副程式，將當前的堆疊暫存器指標 `sp` 儲存到框架暫存器 `bp` 中，並且分配一個新的堆疊區域。
- `ADJ`：調整堆疊大小。
- `LEV`：離開副程式，恢復堆疊指標、框架指標和程式計數器。
- `LI`：載入整數值。
- `LC`：載入字元值。
- `SI`：儲存整數值。
- `SC`：儲存字元值。
- `PSH`：將值推入堆疊中。

另外，該虛擬機還支援以下運算：

- `OR`：按位或運算。
- `XOR`：按位互斥或運算。
- `AND`：按位與運算。
- `EQ`：相等比較。
- `NE`：不等比較。
- `LT`：小於比較。
- `GT`：大於比較。
- `LE`：小於等於比較。
- `GE`：大於等於比較。
- `SHL`：左移運算。
- `SHR`：右移運算。
- `ADD`：加法運算。
- `SUB`：減法運算。
- `MUL`：乘法運算。
- `DIV`：除法運算。
- `MOD`：取模運算。



更詳細的虛擬機指令請參考

* [C4的堆疊虛擬機](C5c-C4的堆疊虛擬機.md)
