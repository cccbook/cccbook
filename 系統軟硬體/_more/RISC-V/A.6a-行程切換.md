## RISC-V 上的行程切換(以組合語言範例解說)

在 RISC-V 架構中，使用者空間使用的是虛擬位址(Virtual Address, VA)，而非實際的物理位址。當一個行程需要在不同的時間點執行，或在多個處理器(CPU)上執行時，就需要進行行程切換(Process Switching)。RISC-V 架構提供了一些機制，可以在不同行程之間進行切換。在本篇文章中，將會以組合語言的範例，說明 RISC-V 上的行程切換。

在 RISC-V 架構中，行程切換主要涉及到以下三個重要組件：

1. 虛擬位址空間
2. 上下文切換(Context Switching)
3. 暫存器(Registers)

### 虛擬位址空間

在 RISC-V 架構中，每個行程都擁有自己的虛擬位址空間。一個行程看到的地址，可能與其他行程看到的地址不同，這是因為虛擬位址空間是獨立的。當一個行程要切換時，需要將該行程的虛擬位址空間轉換為實際的物理位址空間(Physical Address Space)，然後再切換到下一個行程。這種轉換的方法稱為分頁(Paging)。

在 RISC-V 中，每個虛擬位址空間都由多個分頁(Page)組成。每個分頁的大小為 4KB，每個分頁都有一個唯一的虛擬位址(Page Virtual Address, PVA)。為了實現分頁，RISC-V 架構提供了一個稱為分頁表(Page Table)的數據結構。分頁表是一個大小為 4KB 的頁，它包含了多個分頁表表項(Page Table Entry, PTE)。

### 上下文切換

在 RISC-V 架構中，上下文切換主要涉及到兩件事情：

1. 切換虛擬位址空間
2. 切換暫存器

在 RISC-V 中，每個行程都獨立擁有一組暫存器集合。這些暫存器主要用於保存行程的狀態和資訊。當切換行程時，需要將當前行程的暫存器集合保存到該行程的 PCB(Process Control Block) 中，並加載下一個行程的暫存器集合到 RISC-V 處理器的物理暫存器中。這就是上下文切換。

### 暫存器

在 RISC-V 架構中，暫存器主要用於存儲 RISC-V 處理器的狀態、資訊和計算中的暫存資料。RISC-V 架構中，有 32 個通用暫存器通過 mnemonic 名稱定義。其中 x0 暫存器總是為 0，被用作固定值暫存器(ZERO)。其他 31 個暫存器的數據和用途都是相同的，但具體的內容因行程而異。此外，還有一個 PC(Program Counter) 暫存器和一個 SP(Stack Pointer) 暫存器。

在 RISC-V 中，暫存器的使用是相當靈活的。例如，可以使用 x1 寄存器當作鏈接寄存器(LR)，用於保存函數返回地址；也可以使用 x5 和 x6 寄存器當作減法器中的算數暫存器。

下面以一個簡單的範例來說明 RISC-V 上的行程切換：

```
.global main

.section .text

main:
    # 設置虛擬分頁表
    li   a5, ppage                            # 設置 PPA 的值，這是一個鏈接器定義的符號。
    csrw satp, a5                             # 設置 satp 寄存器，使它指向設置的虛擬分頁表。
    
    # 創建一個新行程
    mv   a6, sp                               # 保存當前棧指針
    addi sp, sp, -64                          # 申請新的棧空間
    la   a7, new_proc                          # 設置新行程的入口地址
    sw   a6, 0(sp)                            # 保存當前棧指針到新行程的 PCB 中
    sw   ra, 4(sp)                            # 保存當前 ra 指針到新行程的 PCB 中
    sw   a7, 8(sp)                            # 保存新行程的入口地址到新行程的 PCB 中
    lui  a6, %pcrel_hi(new_proc)              # 設置 k0，這裡我們使用 %pcrel_hi 來計算符號的頁面地址
    addi a6, a6, %pcrel_lo(new_proc)          # 設置 k0，這裡我們使用 %pcrel_lo 來計算符號的偏移量
    jalr a7, a6, 0                            # 運行新行程
    
    # 結束執行
    la a0, 10
    li a7, 93
    ecall

new_proc:
    # 創建新分頁表
    la sp, start
    la a1, end
    la t0, page_table
1:
    li t1, (1<<6) | 8                        # 設置分頁表的權限和大小
    sw t0, 0(t0)                             # 設置 PTE 計入分頁表
    addi t0, t0, 8                            # 移動到下一個 PTE 位置
    addi a0, a0, 4                            # 移動到下一個虛擬頁面
    blt a0, a1, 1b                            # 是否設置完畢
    
    # 設置 PC
    auipc ra, %pcrel_hi(main)                  # 設置 ra，使用 auipc 訪問相對於 PC 上的符號，直到 PC 的 12 位為 0。
    addi ra, ra, %pcrel_lo(main)              # 設置 ra，使用 addi 訪問符號的偏移量
    jal ra, 0                                 # 跳轉到 main 函數
    
    # 結束行程
    ret
    
    .section .data
    
start:
    .fill 2048, 4                             # 記憶體起始地址
end:
    .fill 4096, 4                            # 記憶體結束地址
page_table:
    .fill 4096/8, 8                           # 分頁表

```

在這個範例中，我們首先設置了一個虛擬分頁表。然後，我們創建了一個新的行程，設置了一個新的分頁表，並跳轉到了新的行程入口地址。在新的行程中，我們執行了一些操作，然後返回到了 main 函數並結束了行程。

在本範例中，暫存器的使用非常基本，仅仅使用了 a5、a6、a7、sp、ra 和 t0 等幾個暫存器，實際的 RISC-V 實現中，暫存器的使用視複雜度不同而異，更複雜的程式可能需要使用更多的暫存器。