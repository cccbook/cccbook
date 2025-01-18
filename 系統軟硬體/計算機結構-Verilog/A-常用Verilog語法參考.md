### 附錄 A：常用 Verilog 語法參考

這一部分提供了 Verilog 語言中常用的語法與範例，幫助讀者快速參考和掌握常見的設計結構和語法規則。

---

#### 1. **模組定義 (Module Definition)**

Verilog 中的設計單位是模組 (Module)，它可以包含輸入 (input)、輸出 (output)、以及內部信號 (wire 或 reg)。

```verilog
module adder (
    input [3:0] A,     // 4-bit 輸入 A
    input [3:0] B,     // 4-bit 輸入 B
    output [4:0] sum   // 5-bit 輸出 sum
);

    assign sum = A + B;  // 加法運算

endmodule
```

---

#### 2. **數據類型 (Data Types)**

- **reg**：用來描述儲存型信號，可以在過程中賦值。
- **wire**：用來描述連接型信號，通常連接兩個模組之間。
  
```verilog
reg clk;        // 用於儲存的信號
wire rst;       // 用於連接的信號
```

---

#### 3. **運算符 (Operators)**

- **邏輯運算符**：
  - `&`：與運算 (AND)
  - `|`：或運算 (OR)
  - `~`：非運算 (NOT)
  - `^`：異或運算 (XOR)

- **算術運算符**：
  - `+`：加法
  - `-`：減法
  - `*`：乘法
  - `/`：除法

- **比較運算符**：
  - `==`：等於
  - `!=`：不等於
  - `>`：大於
  - `<`：小於

```verilog
assign result = A & B;  // AND 運算
assign sum = A + B;     // 加法運算
assign equal = (A == B); // 比較 A 是否等於 B
```

---

#### 4. **流程控制 (Control Statements)**

Verilog 支援 `if`、`else`、`case` 等條件語句，還有 `for`、`while` 迴圈。

- **if-else 範例**：

```verilog
always @ (posedge clk) begin
    if (reset)
        out <= 0;  // 如果重置信號為高，輸出為 0
    else
        out <= in; // 否則輸出等於輸入
end
```

- **case 範例**：

```verilog
always @ (opcode) begin
    case (opcode)
        2'b00: out = A + B;
        2'b01: out = A - B;
        2'b10: out = A * B;
        default: out = 0;
    endcase
end
```

---

#### 5. **時序邏輯 (Sequential Logic)**

- **always 敘述**：
  用來描述時序邏輯，通常與時鐘信號一起使用。

```verilog
always @ (posedge clk or posedge reset) begin
    if (reset)
        q <= 0;
    else
        q <= d;
end
```

- **非阻塞賦值 (`<=`)**：
  用於時序邏輯中，確保在同一時鐘週期內執行賦值操作。

```verilog
always @ (posedge clk) begin
    q <= d;  // 非阻塞賦值
end
```

- **阻塞賦值 (`=`)**：
  用於組合邏輯中，賦值操作會立即執行。

```verilog
always @ (a or b) begin
    sum = a + b;  // 阻塞賦值
end
```

---

#### 6. **事件控制 (Event Control)**

- **@ 符號**：
  用於觸發事件，當某信號發生變化時觸發相關的邏輯。

```verilog
always @ (posedge clk) begin
    // 只在時鐘上升沿觸發
end

always @ (negedge reset) begin
    // 只在重置信號下降沿觸發
end
```

---

#### 7. **模擬與測試 (Testbench)**

Verilog 中，測試平台 (Testbench) 用於模擬和驗證設計，通常包含兩個主要部分：設計單元 (DUT) 和測試環境。

```verilog
module tb_adder;
    reg [3:0] A, B;  // 測試用的輸入
    wire [4:0] sum;   // 測試用的輸出

    // 實例化被測模組
    adder uut (
        .A(A),
        .B(B),
        .sum(sum)
    );

    // 初始化信號並提供測試向量
    initial begin
        A = 4'b0000;
        B = 4'b0001;
        #10 A = 4'b0100;
        #10 B = 4'b1010;
    end

    // 觀察結果
    initial begin
        $monitor("At time %t, A = %b, B = %b, sum = %b", $time, A, B, sum);
    end
endmodule
```

---

#### 8. **延遲與時間控制 (Delay and Timing Control)**

- **# 延遲語句**：
  用來引入延遲，通常用於模擬中來觀察訊號變化。

```verilog
#5 A = 1;  // 延遲 5 時間單位後設置 A = 1
```

- **$display 和 $monitor**：
  用於顯示訊號的值，通常用於模擬輸出的監控。

```verilog
$display("Signal value at time %t: %b", $time, A);
$monitor("At time %t, A = %b, B = %b, sum = %b", $time, A, B, sum);
```

---

#### 9. **參數與常數 (Parameters and Constants)**

Verilog 支援使用參數來定義可調整的常數，這些參數在模組實例化時可以被賦值。

```verilog
module adder #(parameter WIDTH = 4) (
    input [WIDTH-1:0] A, B,
    output [WIDTH:0] sum
);
    assign sum = A + B;
endmodule
```

---

這些是 Verilog 中的一些基礎語法，能夠幫助設計師開始撰寫和理解硬體描述語言。在實際設計中，這些語法將結合使用來實現複雜的硬體邏輯。