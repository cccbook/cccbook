### A2 - Verilog HDL 代碼範例

Verilog 是一種硬體描述語言（HDL），常用於數位電路設計中。它允許設計者以結構化、模組化的方式描述數位邏輯系統。以下是一些基本的 Verilog HDL 代碼範例，涵蓋了簡單的邏輯閘、加法器、觸發器等設計。

#### 1. **簡單的與閘（AND Gate）**

這個範例展示了如何使用 Verilog 描述一個基本的與閘（AND Gate）。

```verilog
module AND_Gate (
    input wire A,    // 輸入 A
    input wire B,    // 輸入 B
    output wire Y    // 輸出 Y
);
    assign Y = A & B;  // 進行與運算
endmodule
```

在這段代碼中，我們定義了一個名為 `AND_Gate` 的模組，它有兩個輸入 `A` 和 `B`，並且輸出 `Y`。`assign` 語句將輸入信號進行與運算，並將結果賦值給輸出 `Y`。

#### 2. **簡單的或閘（OR Gate）**

接下來是一個或閘的範例，這個邏輯運算在輸入為 1 時就會輸出 1。

```verilog
module OR_Gate (
    input wire A,    // 輸入 A
    input wire B,    // 輸入 B
    output wire Y    // 輸出 Y
);
    assign Y = A | B;  // 進行或運算
endmodule
```

這段代碼的運行原理和與閘類似，只是使用了 `|` 符號來表示或運算。

#### 3. **半加器（Half Adder）**

半加器是處理兩個二進位數的加法器，不考慮進位輸入。這是半加器的 Verilog 代碼範例。

```verilog
module Half_Adder (
    input wire A,    // 輸入 A
    input wire B,    // 輸入 B
    output wire Sum, // 輸出總和
    output wire Carry // 輸出進位
);
    assign Sum = A ^ B;    // 總和由異或運算得來
    assign Carry = A & B;  // 進位由與運算得來
endmodule
```

在這裡，`Sum` 是兩個二進位數字 `A` 和 `B` 的總和（通過異或運算得到），而 `Carry` 是進位（通過與運算得到）。

#### 4. **全加器（Full Adder）**

全加器考慮三個輸入：兩個加數和進位輸入。它會輸出總和和進位。

```verilog
module Full_Adder (
    input wire A,    // 輸入 A
    input wire B,    // 輸入 B
    input wire Cin,  // 進位輸入
    output wire Sum, // 輸出總和
    output wire Cout // 輸出進位
);
    wire Sum_AB;  // 用來儲存 A 和 B 的總和
    wire Carry_AB; // 用來儲存 A 和 B 的進位

    // 計算 A 和 B 的總和與進位
    assign Sum_AB = A ^ B;  
    assign Carry_AB = A & B;

    // 計算最終總和與進位
    assign Sum = Sum_AB ^ Cin;  // 進行總和計算
    assign Cout = Carry_AB | (Sum_AB & Cin);  // 進行進位計算
endmodule
```

這個範例中，我們計算了 `A` 和 `B` 的總和 `Sum_AB`，並且根據 `Cin`（進位輸入）來計算最終的總和和進位。這裡使用了異或運算和與運算來實現這些操作。

#### 5. **D型觸發器（D Flip-Flop）**

這是一個基本的 D型觸發器，它根據時鐘信號的變化來更新輸出。

```verilog
module D_Flip_Flop (
    input wire D,       // 輸入 D
    input wire CLK,     // 時鐘信號
    input wire Reset,   // 重置信號
    output reg Q        // 輸出 Q
);
    always @(posedge CLK or posedge Reset) begin
        if (Reset) begin
            Q <= 0;  // 當重置信號為高時，Q 輸出為 0
        end else begin
            Q <= D;  // 否則，Q 輸出等於 D 輸入
        end
    end
endmodule
```

在這段代碼中，我們使用了 `always` 區塊來描述觸發器的行為。當時鐘信號的上升沿到來時，`Q` 的值會更新為 `D` 的值。如果 `Reset` 為高電位，則 `Q` 被設置為 0。

#### 6. **4 位元計數器（4-bit Counter）**

下面是一個簡單的 4 位元計數器，它會根據時鐘信號進行計數。

```verilog
module Counter (
    input wire CLK,       // 時鐘信號
    input wire Reset,     // 重置信號
    output reg [3:0] Q    // 4 位元計數器輸出
);
    always @(posedge CLK or posedge Reset) begin
        if (Reset) begin
            Q <= 4'b0000;  // 當重置信號為高時，計數器重置為 0
        end else begin
            Q <= Q + 1;    // 否則，計數器加 1
        end
    end
endmodule
```

這個計數器在每次時鐘的上升沿增加計數值，並且當 `Reset` 訊號為高時，計數器會重置為 0。

#### 總結

這些 Verilog 代碼範例展示了如何描述基本的數位邏輯元件。Verilog 使設計者可以以模組化的方式進行數位系統設計，這些範例涵蓋了從基本邏輯閘、加法器到觸發器和計數器等常見元件的設計。在實際的硬體設計過程中，這些元件可以用來構建更複雜的數位系統。