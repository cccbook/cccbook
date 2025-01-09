## RISC-V 上的 mutex 實作 (以組合語言範例解說)

在 RISC-V 上，我們可以利用 x86 架構上所使用的 Test-and-Set 指令來實現一個簡單的 mutex，或者使用 load-reserved/store-conditional (LR/SC) 來實現一個更加高效的 mutex。

下面我們先概括一下 mutex 的幾個重要特性：(1) 一次只有一個執行緒可以進入 mutex 保護區塊；(2) 任何一個要進入 mutex 保護區塊的執行緒必須首先獲取並持有這個 mutex；(3) 持有 mutex 的執行緒必須釋放它，以供其他執行緒使用。

在 RISC-V 上，我們可以使用 LR/SC 指令序列實現一個 mutex。

mutex 的實現需要一個變數來指示這個 mutex 的狀態。對於一個非常簡單的 mutex，我們可以使用一個整數變數 lock 來表示狀態。lock = 1 時，表示 mutex 已經被持有；lock = 0 時，表示 mutex 可以被獲取。

#### 使用 LR/SC 指令來實現 mutex

使用 LR/SC 的方式實現 mutex 需要經歷以下的步驟：

1. 呼叫 load-reserved (LR) 指令來載入 lock 變數到暫存器中。
2. 如果 LR 指令成功執行，表示 lock 變數的值已經載入暫存器。
3. 接著，我們可以編輯 lock 變數。
4. 調用 store-conditional (SC) 指令，存儲在 lock 變數上的新值。如果 store-conditional 指令成功存儲了新值，表示獲取 mutex 成功；否則，表示 mutex 已經被其他執行緒獲取了，需要重新從步驟 1 開始。

下面是一個使用 LR/SC 指令實現 mutex 的示例，以組合語言的形式呈現：

```asm
    .align 2                # 雙字對齊，以便作為空間分隔選項
    .globl mutex            # 全域可見
mutex:
    .word 0                 # 定義一個空的 32 位無符號整數變數
    .text
    .align 2                # 調整指令在記憶體中的對齊方式
    .globl acquire_mutex    # 全域可見
acquire_mutex:
    li t0, 1
    lr.w t1, (mutex)        # 載入mutex變數到暫存器t1中，同時設置`load-locked`bit位
wait_for_lock:
    beq t1, t0, wait_for_lock  # 向前跳轉（Branch Forward）到 wait_for_lock，如果 t1 與 t0 相等
    sc.w t2, t0, (mutex)    # 存儲當前錚書(t0)到mutex變數，如果操作成功，則t2被置位，否則t2將為0（也就是不成功）
    beqz t2, wait_for_lock  # 如果成功就保持已獲取狀態，否則回到第一步重新獲取鎖

    ret                     # 退出函數

    .align 2
    .globl release_mutex    # 全域可見
release_mutex:
    # 釋放 mutex 之前需要關閉中斷

    sw zero, (mutex)        # 清零 mutex 變數
    # 開啟中斷

    ret                     # 退出函數
```

這其中的關鍵指令就是 `lr.w` 和 `sc.w`，第一條指令負責載入 mutex 變數到暫存器 t1 中，同時設置 load-locked bit 位，第二條指令則是嘗試將獲取 lock 的值 (t0) 儲存到 mutex 變數中，同時設置成功標準位。如果成功，成功標準位將會被置位；反之則不會，此時必須返回到第一條指令的位置重新嘗試使用 `lr.w` 指令重新獲取 mutex 變數的值。

總體而言，此處提供的 LR/SC 方案僅為您提供了 mutex 的工作原理。實際應用場景中，您需要確定可能要避免使用這種特定方法的情況，如過多的資源競爭和不必要的 lock-hold 時間等。