## RISC-V 上的 Context Switch (以組合語言範例解說)

Context Switch 是在多工作業系統中很重要的一個概念，當 CPU 的時間輪轉到另外一個進程時，需要把當前進程的狀態存下來，以便在下一次時間片段時能夠恢復這個進程的狀態繼續執行。這個狀態包括 CPU 的通用目的暫存器、程式計數器、堆疊暫存器和其他暫存器等。

在 RISC-V 架構下，Context Switch 的實作方式和其它的 RISC-V 之相同。它也是依靠 naive 實作並且支援 S-mode user space 進行的，所以可以很好地簡化 Context Switch 的流程。

以下是一個簡單的 Context Switch 的組合語言範例：

```asm
    .section .text
    .globl __context_switch

# void __context_switch(uintptr_t* prev_sp, uintptr_t next_sp);
__context_switch:
    addi sp, sp, -16 * 8  # 開始需要 16 個通用暫存器的空間
    sd ra, sp, 0
    sd s0, sp, 1*8
    sd s1, sp, 2*8
    sd s2, sp, 3*8
    sd s3, sp, 4*8
    sd s4, sp, 5*8
    sd s5, sp, 6*8
    sd s6, sp, 7*8
    sd s7, sp, 8*8
    sd s8, sp, 9*8
    sd s9, sp, 10*8
    sd s10, sp, 11*8
    sd s11, sp, 12*8
    sd t0, sp, 13*8
    sd t1, sp, 14*8
    sd t2, sp, 15*8

    lw s0, 4(a0)  # 將 prev_sp 存到 s0，即將它存放在 Context（包含寄存器的區域）中
    sd ra, (s0)   # 將返回地址 ra 寄存器存到 prev_sp 所指向的位置
    sd sp, 8(a0)  # 將 SP 存到 prev_sp 所指向的位置 + 8 bytes 的位置，即儲存堆疊指標

    lw s0, 4(a1)  # 從 next_sp 中獲取 prev_sp
    ld ra, (s0)   # 從 next_sp 中獲取返回地址 ra，並將其放回它相應的寄存器中
    ld sp, 8(a1)  # 從 next_sp 中獲取堆疊指標 sp，並將其放回它相應的寄存器中

    ld s0, 1*8(sp)
    ld s1, 2*8(sp)
    ld s2, 3*8(sp)
    ld s3, 4*8(sp)
    ld s4, 5*8(sp)
    ld s5, 6*8(sp)
    ld s6, 7*8(sp)
    ld s7, 8*8(sp)
    ld s8, 9*8(sp)
    ld s9, 10*8(sp)
    ld s10, 11*8(sp)
    ld s11, 12*8(sp)
    ld t0, 13*8(sp)
    ld t1, 14*8(sp)
    ld t2, 15*8(sp)

    addi sp, sp, 16 * 8  # 恢復現場，釋放暫存器（開始 Context Switch）

    jr ra
```

以上是一段比較基本的 Context Switch 實現，大致流程如下：

- 暫停目前的任務執行，遵循最後一次存儲保存的 CPU 狀態上下文添加到數據中。
- 裝載新任務的 CPU 狀態上下文。
- 恢復堆棧指針，無損地回到新任務。
- 當到達下一個時間就會卸載任務並開始下一個 Context Switch。

在這個例子中，首先需要 16 個通用暫存器的空間。然後將存儲在 `uintptr_t* prev_sp` 上 `ra` 和 `s0` 通過 `lw` 從 `prev_sp` 中載入。下一步是將 `ra` 寄存器的值存到 `prev_sp` 的位置中，位移為 0，因此可以通過 `sd ra, (s0)` 來完成這一步。

接下來是 `sd sp, 8(a0)`，將 SP 存到 `prev_sp` 所指向的位置 + 8 bytes 的位置，即堆疊指標的位置也被 refresh，這也是當前程式體以 call 的方式回來時需要的。

之後，`lw s0, 4(a1)` 得到 `next_sp`，以此獲取 `"ra"`，然後存回 `"ra"` 寄存器中。同樣地，也獲取了 SP 寄存器，並已在將來使用。

最後，需要恢復通用暫存器。通過使用 `ld` 指令從参數中的地址中回復通用暫存器。"addi sp, sp, 16 * 8" 的作用是可以恢複現場，釋放所有已使用的暫存器。

完成這類的流程之後就可以回到 `ra` 寄存器指向的位置並且開始執行下一個 Context Switch。