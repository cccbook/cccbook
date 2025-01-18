### xv6：一個簡單的、類似 Unix 的教學作業系統

Russ Cox Frans Kaashoek Robert Morris

8月31， 2024

內容
--

*   1 操作系統介面
*   1.1 進程和記憶體
*   1.2 I/O and File descriptors
*   1.3 管道
*   1.4 檔案系統
*   1.5 Real world
*   1.6 Exercises
*   2 Operating system organization
*   2.1 抽象物理資源
*   2.2 User mode, supervisor mode, and system calls
*   2.3 Kernel organization
*   2.4 Code: xv6 organization
*   2.5 流程概述
*   2.6 代碼：啟動 xv6，第一個進程和系統調用
*   2.7 安全模型
*   2.8 Real world
*   2.9 Exercises
*   3 頁表
*   3.1 Paging hardware
*   3.2 Kernel address space
*   3.3 代碼：創建位址空間
*   3.4 物理記憶體分配
*   3.5 代碼：物理記憶體分配器
*   3.6 Process address space
*   3.7 Code: sbrk
*   3.8 Code: exec
*   3.9 Real world
*   3.10 Exercises
*   4 陷阱和系統調用
*   4.1 RISC-V trap machinery
*   4.2 來自用戶空間的陷阱
*   4.3 Code: Calling system calls
*   4.4 代碼：系統調用參數
*   4.5 來自內核空間的陷阱
*   4.6 頁面錯誤異常
*   4.7 Real world
*   4.8 Exercises
*   5 中斷和設備驅動程式
*   5.1 Code: Console input
*   5.2 代碼：主控台輸出
*   5.3 驅動程式中的併發
*   5.4 Timer interrupts
*   5.5 Real world
*   5.6 Exercises
*   6 Locking
*   6.1 Races
*   6.2 Code: Locks
*   6.3 Code: Using locks
*   6.4 Deadlock and lock ordering
*   6.5 Re-entrant locks
*   6.6 Locks and interrupt handlers
*   6.7 指令和記憶體排序
*   6.8 Sleep locks
*   6.9 Real world
*   6.10 Exercises
*   7 Scheduling
*   7.1 Multiplexing
*   7.2 代碼：上下文切換
*   7.3 Code: Scheduling
*   7.4 Code: mycpu and myproc
*   7.5 Sleep and wakeup
*   7.6 Code: Sleep and wakeup
*   7.7 代碼：管道
*   7.8 代碼：Wait、exit 和 kill
*   7.9 Process Locking
*   7.10 Real world
*   7.11 Exercises
*   8 檔案系統
*   8.1 概述
*   8.2 Buffer cache layer
*   8.3 Code: Buffer cache
*   8.4 Logging layer
*   8.5 Log design
*   8.6 Code: logging
*   8.7 Code: Block allocator
*   8.8 Inode layer
*   8.9 Code: Inodes
*   8.10 Code: Inode content
*   8.11 代碼：directory layer
*   8.12 Code: Path names
*   8.13 File descriptor layer
*   8.14 Code: System calls
*   8.15 Real world
*   8.16 Exercises
*   9併發性再論
*   9.1 Locking patterns
*   9.2 Lock-like patterns
*   9.3 No locks at all
*   9.4 並行度
*   9.5 Exercises
*   10 Summary

前言和致謝
=====

這是一篇針對操作系統課程的草稿文本。它通過研究名為 xv6 的範例內核來解釋操作系統的主要概念。Xv6 以 Dennis Ritchie 和 Ken Thompson 的 Unix 版本 6 （v6） \[17\] 為模型。Xv6 鬆散地遵循 v6 的結構和風格，但在 ANSI C \[7\] 中實現，用於多核 RISC-V \[15\]。本文應與 xv6 的原始程式碼一起閱讀，這種方法的靈感來自 John Li- ons 的 UNIX 第 6 版評論 \[11\];該文本包含指向原始程式碼的超連結，網址為 https://://github.com/mit-pdos/xv6-riscv。請參閱 [https://pdos.csail.mit.edu/6](https://pdos.csail.mit.edu/6)。有關指向 V6 和 Xv6 在線資源的其他指標，包括使用 Xv6 的多個練習作業。我們在 6.828 和 6.1810 中用過這個文本，這是 MIT 的操作系統類。我們感謝那些班級的教師、助教和學生，他們都直接或間接地為 xv6 做出了貢獻。我們特別要感謝 Adam Belay、Austin Clements 和 Nickolai Zeldovich。最後，我們要感謝通過電子郵件向我們發送文本中的錯誤或改進建議的人：Abutalib Aghayev、Sebastian Boehm、brandb97、Anton Burtsev、Raphael Car- valho、Tej Chajed、Brendan Davidson、Rasit Eskicioglu、Color Fuzzy、Wojciech Gac、Giuseppe、Tao Guo、Haibo Hao、Naoki Hayama、Chris Henderson、Robert Hilderman、Eden Hochbaum、Wolfgang Keller、Paweł Kraszewski、Henry Laih、 Jin Li， Austin Liew， [lyazj@github.com](mailto:lyazj@github.com)， Pavan Maddamsetti， Jacek Masiulaniec， Michael McConville， m3hm00d， miguelgvieira， Mark Morrissey， Muhammed Mourad， Harry Pan， Harry Porter， 錢思源， 喬哲峰， Askar Safin， Salman Shah， Huang Sha， Vikram Shenoy， Adeodato Simó， Ruslan Savchenko， Pawel Szczurko， Warren Toomey， tyfkda， tzerbib， Vanush Vaswani， 習 Wang， 鄒昌偉， Sam Whitlock， Qiongsi Wu， LucyShawYang， [ykf1114@gmail.com](mailto:ykf1114@gmail.com)和 Meng 周如果您發現錯誤或有改進建議，請發送電子郵件至 Frans Kaashoek 和 Robert Morris （kaashoek,rtm@csail.mit.edu）。[](mailto:rtm@csail.mit.edu)

第一章
===

操作系統介面
======

操作系統的工作是在多個程式之間共享計算機，並提供比單獨硬體支援的更有用的服務集。操作系統管理和抽象化低級硬體，因此，例如，字處理器無需關心正在使用哪種類型的磁碟硬體。操作系統在多個程式之間共享硬體，以便它們同時運行（或看起來正在運行）。最後，操作系統為程式提供了受控的交互方式，以便它們可以共用數據或協同工作。操作系統通過介面為使用者程式提供服務。設計一個好的介面被證明是困難的。一方面，我們希望介面簡單而狹窄，因為這樣更容易正確實現。另一方面，我們可能很想為應用程式提供許多複雜的功能。解決這種緊張關係的訣竅是設計依賴於一些機制的介面，這些機制可以組合起來以提供更多的通用性。本書使用單個操作系統作為具體示例來說明操作系統概念。該操作系統 xv6 提供了 Ken Thompson 和 Dennis Ritchie 的 Unix 作業系統 \[17\] 引入的基本介面，並模仿了 Unix 的內部設計。Unix 提供了一個狹窄的介面，其機制組合得很好，提供了令人驚訝的通用性。這個介面已經非常成功，以至於現代操作系統（BSD、Linux、macOS、Solaris，甚至在較小程度上還有 Microsoft Windows）都具有類似 Unix 的介面。Under standing xv6 是理解這些系統和許多其他系統的良好開端。如圖 1 所示。1 顯示，xv6 採用 aKernel 的傳統形式，這是一個為正在運行的程式提供服務的特殊程式。每個正在運行的程式（稱為 aprocess）都有包含指令、數據和堆疊的記憶體。這些說明實現程序的計算。數據是計算所作用於的變數。堆疊組織程序的過程調用。給定的計算機通常有許多進程，但只有一個內核。當進程需要調用內核服務時，它會調用 asystem 調用，這是操作系統介面中的調用之一。系統調用進入內核;內核執行服務並返回。因此，進程在執行 inuser space和 kernel space 之間交替。正如後面的章節中詳細描述的那樣，內核使用 CPU^1 提供的硬體保護機制來確保在用戶空間中執行的每個進程只能訪問

（^1）此文字通常是指使用術語 CPU（首字母縮略詞）執行計算的硬體元素

Kernel


shell cat
user
space


kernel
space


system
call


Figure 1.1: A kernel and two user processes.


它自己的記憶。內核使用實施這些保護所需的硬體許可權執行;使用者程式在沒有這些許可權的情況下執行。當使用者程式調用 sys tem 調用時，硬體會提高許可權級別並開始在內核中執行預先安排的函數。

內核提供的系統調用集合是用戶程式看到的介面。xv6 內核提供了 Unix 內核傳統上提供的服務和系統調用的子集。圖 1.2 列出了 xv6 的所有系統調用。本章的其餘部分概述了 xv6 的服務（進程、記憶體、檔描述符、管道和文件系統），並通過代碼片段和對 shell（Unix 的命令行使用者介面）如何使用它們的討論來說明它們。shell 對系統調用的使用說明了它們的設計是多麼仔細。shell 是一個普通程式，它從用戶那裡讀取命令並執行它們。shell 是一個用戶程式，而不是內核的一部分，這一事實說明了系統調用介面的強大功能：shell 沒有什麼特別之處。這也意味著外殼易於更換;因此，現代 Unix 系統有多種 shell 可供選擇，每個 shell 都有自己的使用者介面和腳本功能。xv6 shell 是 Unix Bourne shell 本質的簡單實現。它的實現可以在 （user/sh.c：1） 中找到。

### 1.1 進程和記憶體

xv6 行程由用戶空間記憶體（指令、資料和堆疊）和內核專用的每個進程狀態組成。Xv6分時進程：它在等待執行的進程集之間透明地切換可用的 CPU。當進程未執行時，xv6 會保存進程的 CPU 寄存器，並在下次運行該進程時恢復它們。內核將進程標識碼 （或 PID） 與每個進程相關聯。

一個進程可以使用fork系統創建一個新進程call.fork為新進程提供調用進程記憶體的精確副本：它將調用進程的指令、數據和堆棧複製到新進程的記憶體中.fork 返回原始進程和新進程。在原始進程中，fork 返回新進程的 PID。在新進程中，fork 返回零。原始進程和新進程通常稱為 parentandchild。

用於中央處理器。其他文件（例如 RISC-V 規範）也使用單詞 processor、core 和 hart 而不是 CPU。

System call Description
int fork() Create a process, return child’s PID.
int exit(int status) Terminate the current process; status reported to wait(). No return.
int wait(int *status) Wait for a child to exit; exit status in *status; returns child PID.
int kill(int pid) Terminate process PID. Returns 0, or -1 for error.
int getpid() Return the current process’s PID.
int sleep(int n) Pause for n clock ticks.
int exec(char *file, char *argv[]) Load a file and execute it with arguments; only returns if error.
char *sbrk(int n) Grow process’s memory by n zero bytes. Returns start of new memory.
int open(char *file, int flags) Open a file; flags indicate read/write; returns an fd (file descriptor).
int write(int fd, char *buf, int n) Write n bytes from buf to file descriptor fd; returns n.
int read(int fd, char *buf, int n) Read n bytes into buf; returns number read; or 0 if end of file.
int close(int fd) Release open file fd.
int dup(int fd) Return a new file descriptor referring to the same file as fd.
int pipe(int p[]) Create a pipe, put read/write file descriptors in p[0] and p[1].
int chdir(char *dir) Change the current directory.
int mkdir(char *dir) Create a new directory.
int mknod(char *file, int, int) Create a device file.
int fstat(int fd, struct stat *st) Place info about an open file into *st.
int link(char *file1, char *file2) Create another name (file2) for the file file1.
int unlink(char *file) Remove a file.


圖 1.2：Xv6 系統調用。如果沒有特別說明，這些調用將返回 0 表示沒有錯誤，如果出現錯誤，則返回 -1。

例如，考慮以下用 C 程式設計語言編寫的程式片段 \[7\]：

int pid = fork();
if(pid > 0){
printf("parent: child=%d\n", pid);
pid = wait((int *) 0);
printf("child %d is done\n", pid);
} else if(pid == 0){
printf("child: exiting\n");
exit(0);
} else {
printf("fork error\n");
}


exitsystem 調用會導致調用進程停止執行並釋放記憶體和打開的文件等資源。Exit 採用整數 status 參數，通常為 0 表示成功，1 表示失敗。waitsystem 調用返回當前進程的已退出（或已終止）子進程的 PID，並將子進程的退出狀態複製到傳遞給 wait 的位址;如果沒有

調用方的 children has exited，waits 等待一個 do this.如果調用方沒有子項，則 wait 立即返回 -1。如果 parent 不關心 child 的 exit 狀態，它可以傳遞一個 0 位址 towait。在示例中，輸出行 parent： child= child： exiting

可能按任一順序出現（甚至混合出現），具體取決於父級還是子級首先到達 itsprintfcall。子級退出后，父級的 swait返回，導致父級列印

parent: child 1234 is done


儘管 child 最初具有與 parent 相同的 memory 內容，但 parent 和 child 使用單獨的 memory 和單獨的 registers 執行： 更改一個中的變數不會影響另一個。例如，當 wait 的返回值存儲在父進程中的 intopid 中時，它不會更改子進程中的 variablepid。子項的 ofpidin 值仍為零。execsystem 調用將調用進程的記憶體替換為從文件系統中存儲的檔載入的新記憶體映像。該文件必須具有特定的格式，該格式指定檔的哪一部分包含指令，哪一部分是數據，從哪條指令開始，等等。Xv6 使用 ELF 格式，第 3 章對此進行了更詳細的討論。通常，該檔是編譯程式原始程式碼的結果。當 execsucceed 時，它不會返回到調用程式;相反，從檔載入的指令從 ELF 標頭中聲明的入口點開始執行。exec接受兩個參數：包含可執行檔的檔的名稱和字串參數數位。例如：

char *argv[3];


argv[0] = "echo";
argv[1] = "hello";
argv[2] = 0;
exec("/bin/echo", argv);
printf("exec error\n");


此 fragment 將調用程式替換為帶有參數 listecho hello 的 program/bin/echorunning 實例。大多數程式會忽略argument陣列的第一個元素，該元素通常是程式的名稱。xv6 shell 使用上述調用代表使用者運行程式。外殼的主要結構很簡單;參見main（user/sh.c：146）。主迴圈使用 getcmd 讀取來自使用者的一行 input。然後它調用 fork，後者創建 shell 進程的副本。父級調用 wait，而子級運行命令。例如，如果使用者在shell中鍵入了 「echo hello」，則 runcmd 將使用 「echo hello」 作為參數調用。runcmd（user/sh.c：55） 運行實際命令。對於 「echo hello」，它將調用 exec（user/sh.c：79）。如果 exec成功，則子級將執行 fromecho 而不是 runcmd 的指令。在某個時候echo 會調用 exit，這將導致父級返回 fromwaitinmain（user/sh.c：146）。您可能想知道為什麼 forkandexec 沒有合併到一個調用中;我們稍後將看到shell在其I/O重定向的實現中利用了分離。為避免浪費

創建一個重複的進程，然後立即替換它 （withexec），操作內核通過使用虛擬記憶體技術（如 Copy-on-write）來優化 fork 的實現對於這個用例（參見 Section 4.6）。Xv6 隱式分配大多數用戶空間記憶體：fork分配父級記憶體的子級副本所需的記憶體，並 exec 分配足夠的記憶體來保存可執行檔。在運行時需要更多記憶體的進程（可能是 formalloc）可以調用 brk（n） 來增加其數據記憶體 nzero 位元組;sbrk返回新記憶體的位置。

### 1.2 I/O and File descriptors

檔描述符是一個小整數，表示進程可以讀取或寫入的內核管理的物件。進程可以通過打開檔、目錄或設備，或者通過創建管道或複製現有描述符來獲取檔描述符。為簡單起見，我們通常將檔描述符引用的對象稱為 「file」;File Descriptor 介面抽象出檔、管道和設備之間的差異，使它們看起來都像位元組流。我們將輸入和輸出稱為 I/O。在內部，xv6 內核使用檔描述符作為每個進程表中的索引，因此每個進程都有一個從零開始的檔描述符的私有空間。按照約定，進程從檔描述符 0（標準輸入）讀取，將輸出寫入檔描述符 1（標準輸出），並將錯誤消息寫入檔描述符 2（標準錯誤）。正如我們將看到的，shell 利用約定來實現 I/O 重定向和管道。shell 確保它始終有三個檔描述符 open（user/sh.c：152），默認情況下，它們是控制台的檔描述符。Thereadandwritesystem 調用 read bytes from 和 write bytes 以打開由檔描述符命名的檔。callread（fd，buf，n） 從檔描述符 fd 中讀取最多 nbytes 位元組，將它們複製到 buf 中，並返回讀取的位元組數。引用檔的每個檔描述符都有一個與之關聯的偏移量。read從當前檔偏移量中讀取數據，然後將該偏移量提前讀取的位元元組數：後續read將返回 firstread 傳回的位元組數後面的位元組。當沒有更多位元組要讀取時，read返回零以指示文件結束。 callwrite（fd，buf，n）writesnbytes 從 buf 到檔描述符 fd，並返回寫入的位元組數。僅當發生錯誤時，才會寫入少於 thannbytes 的 binnbytes。Likeread 在當前檔偏移量處寫入數據，然後將該偏移量提前寫入的位元組數：eachwrite從前一個中斷的位置開始。以下程式片段（構成 programcat 的本質）將數據從其標準輸入複製到其標準輸出。如果發生錯誤，它會將消息寫入標準錯誤。

char buf[512];
int n;


for(;;){
n = read(0, buf, sizeof buf);
if(n == 0)


break;
if(n < 0){
fprintf(2, "read error\n");
exit(1);
}
if(write(1, buf, n) != n){
fprintf(2, "write error\n");
exit(1);
}
}


在代碼片段中需要注意的重要一點是，cat不知道它是從檔、控制台還是管道讀取。同樣cat不知道它是列印到控制台、文件還是其他任何內容。使用檔描述符以及檔描述符 0 是輸入而檔描述符 1 是輸出的約定允許對 cat 進行簡單的實現。closesystem 調用釋放了一個檔描述符，使其可以被 futureopen、pipe、ordupsystem 調用免費重用（見下文）。新分配的檔描述符始終是當前進程中編號最低的未使用描述符。File descriptors 和 forkinteract 使 I/O 重定向易於實現。fork 複製父級的檔描述符表及其記憶體，以便子級從與父級完全相同的打開檔開始。系統 callexec 替換調用進程的記憶體，但保留其檔表。此行為允許shell通過分叉、在子項中重新打開選定的檔描述符，然後調用exec來運行新程式來實現I/O重定向。以下是 shell 為 commandcat < input.txt執行的代碼的簡化版本：

char *argv[2];


argv[0] = "cat";
argv[1] = 0;
if(fork() == 0) {
close(0);
open("input.txt", O_RDONLY);
exec("cat", argv);
}


在子物件關閉檔描述符 0 后，open保證將該檔描述符用於新openedinput.txt：0 將是最小的可用檔 descriptor.cat，則使用檔描述符 0（標準輸入）執行，引用 toinput.txt。此序列不會更改父進程的檔描述符，因為它僅修改子進程的描述符。

xv6 shell 中的 I/O 重定向代碼正是以這種方式工作的 （user/sh.c：83）。回想一下，此時在代碼中，shell 已經分叉了子 shell，並且 runcmd 將調用 exec 來載入新程式。第二個參數 toopen由一組標誌組成，這些標誌以位表示，用於控制 open執行的操作。可能的值在檔控制 （fcntl） 頭檔 （kernel/fcntl.h：1-5） 中定義：O\_RDONLY、O\_WRONLY、O\_RDWR、O\_CREATE、andO\_TRUNC，它指示open打開檔

對於讀取、寫入或讀取和寫入，如果檔不存在，則創建該檔，並將檔截斷為零長度。

現在應該很清楚為什麼 forkandexec 單獨調用是有説明的：在兩者之間，shell 有機會重定向子 I/O 而不會干擾主 shell 的 I/O 設置。相反，人們可以想像一個假設的 combinedforkexecsystem 調用，但使用此類調用執行 I/O 重定向的選項似乎很尷尬。shell 可以在調用 forkexec 之前修改自己的 I/O 設置（然後撤消這些修改）;orforkexec可以將 I/O 重定向指令作為參數;或者（最不吸引人地）每個程式（如 cat）都可以被教導執行自己的 I/O 重定向。

儘管 fork 會複製檔描述符表，但每個底層檔偏移量都在父級和子級之間共用。請考慮以下範例：

if(fork() == 0) {
write(1, "hello ", 6);
exit(0);
} else {
wait(0);
write(1, "world\n", 6);
}


在此片段的末尾，附加到檔描述符 1 的檔將包含 datahello 世界。Thewrite在父級中（感謝 towait，它僅在子級完成後運行）從子級的 writeleft.此行為有助於從shell命令序列生成順序輸出，例如 （echo hello;Echo World） >output.txt。

Thedupsystem 調用複製現有檔描述符，返回引用同一底層 I/O 物件的新檔描述符。兩個檔描述符共用一個偏移量，就像 forkdo 複製的檔描述符一樣。這是將 hello world 寫入檔的另一種方法：

fd = dup(1);
write(1, "hello ", 6);
write(fd, "world\n", 6);


如果兩個檔描述符是通過一系列 forkanddupcalls 從同一原始檔描述符派生的，則它們共用一個偏移量。否則，檔描述符不會共用偏移量，即使它們是由同一 file.dup的 opencalls 產生的，允許 shell 實現如下命令：ls existing-file non-existing-file > tmp1 2>&1。The2>&1告訴 shell 為命令提供一個檔描述符 2，該描述符 2 是描述符 1 的重複項。現有文件的名稱和不存在檔的錯誤消息都將顯示在 filetmp1 中。xv6 shell 不支援錯誤檔描述符的 I/O 重定向，但現在您知道如何實現它了。

檔描述符是一個強大的抽象概念，因為它們隱藏了它們所連接的細節：寫入檔描述符 1 的進程可能正在寫入檔、控制台等設備或管道。

### 1.3 管道

Apipe是一個小型內核緩衝區，作為一對檔描述符暴露給進程，一個用於讀取，一個用於寫入。將數據寫入管道的一端使該數據可用於從管道的另一端讀取。管道為進程提供了一種通信方式。以下範例代碼運行程式式 wc，並將標準輸入連接到管道的讀取端。

int p[2];
char *argv[2];


argv[0] = "wc";
argv[1] = 0;


pipe(p);
if(fork() == 0) {
close(0);
dup(p[0]);
close(p[0]);
close(p[1]);
exec("/bin/wc", argv);
} else {
close(p[0]);
write(p[1], "hello world\n", 12);
close(p[1]);
}


程式 callspipe，它創建一個新管道並在 arrayp 中記錄讀取和寫入檔描述符。Afterfork 中，父級和子級都有引用管道的檔描述符。子項調用 closeanddup使檔描述符零引用管道的讀取端，關閉檔描述符 inp，並調用 exec 到 runwc。當 wcreads 從其標準輸入中讀取時，它會從管道中讀取。父級關閉管道的讀取端，寫入管道，然後關閉寫入端。如果沒有可用數據，則管道將等待寫入資料或關閉引用寫入端的所有檔描述器;在後一種情況下，read將返回 0，就像已到達數據檔的末尾一樣。readblocks 直到新數據無法到達的事實是 child 在執行 wcabove 之前關閉管道的寫入端很重要的原因之一：如果 ofwc 的檔描述符之一引用了管道的寫入端，wc 將永遠不會看到 end-of-file。xv6 shell 實現管道，例如 grep fork sh.c |wc -lin 的方式類似於上面的代碼 （user/sh.c：101）。子進程將創建一個管道，以將管道的左端與右端連接起來。然後，它為管道的左端調用 forkandruncmd，為右端調用 forkandruncmd，並等待兩者完成。管道的右端可能是一個命令，它本身包含一個管道（例如，a | b | c），它本身分叉兩個新的子進程（一個 forband 一個 forc）。因此，shell 可能會創建一個進程樹。葉子

此樹的 Commands 和 Interior 節點是等待 Left 和 Right 子節點完成的進程。管道似乎並不比臨時檔更強大：管道 echo hello world |廁所

可以在沒有管道的情況下實現，如

echo hello world >/tmp/xyz; wc </tmp/xyz


在這種情況下，管道比臨時檔至少具有三個優點。首先，管道會自動清理;使用檔重定向時，shell 必須小心地在完成後刪除 /tmp/xyz。其次，管道可以傳遞任意長的數據流，而檔重定向需要磁碟上有足夠的可用空間來存儲所有數據。第三，管道允許並行執行管道階段，而檔方法要求第一個程式在第二個程序開始之前完成。

### 1.4 檔案系統

xv6 檔案系統提供資料檔（包含未解釋的位元組陣列）和目錄（包含對資料檔和其他目錄的命名引用）。這些目錄形成一個樹，從名為 theroot 的特殊目錄開始。apath類/a/b/c是指文件或目錄 namedc在根目錄 / 中的目錄 namedb 內。不以/開頭的路徑將相對於調用進程的當前目錄進行評估，這可以通過 chdirsystem 調用進行更改。這兩個代碼片段都打開同一個檔（假設所有涉及的目錄都存在）：

chdir("/a");
chdir("b");
open("c", O_RDONLY);


open("/a/b/c", O_RDONLY);


第一個片段將進程的當前目錄更改為 /a/b;第二個選項既不引用也不更改進程的當前目錄。有用於創建新文件和目錄的系統調用：mkdir 創建新目錄，使用 theO\_CREATEflag 打開創建新資料檔，mknod 創建新設備檔。此範例說明瞭所有三個：

mkdir("/dir");
fd = open("/dir/file", O_CREATE|O_WRONLY);
close(fd);
mknod("/console", 1, 1);


mknod會創建一個引用設備的特殊檔。與設備文件關聯的是主設備號和次設備號（兩個參數 tomknod），它們唯一標識內核設備。當進程稍後打開設備檔時，內核會 divertsreadandwritesystem 調用內核設備實現，而不是將它們傳遞給文件系統。

檔名與檔本身不同;同一個底層檔（稱為 aninode）可以有多個名稱，稱為 links。每個連結都包含目錄中的一個條目;該條目包含檔名和對 inode 的引用。一個 inode holdsmetadata 關於一個檔，包括它的類型 （文件或目錄或設備）、它的長度、檔內容在磁碟上的位置以及指向檔的連結數。fstatsystem 調用從檔描述符引用的 inode 中檢索資訊。它填寫 astruct stat，定義 instat.h（kernel/stat.h）為：

#define T_DIR 1 // Directory
#define T_FILE 2 // File
#define T_DEVICE 3 // Device


struct stat { int dev; / 文件系統的磁碟設備 uint ino; / 索引節點編號 short type; ─ 檔類型 short nlink; & 指向文件的連結數 uint64 size; ─ 檔大小（以位元組為單位） };linksystem 調用會創建另一個文件系統名稱，該名稱引用與現有檔相同的 inode。此 fragment 將創建一個名為 bothaandb 的新檔。

open("a", O_CREATE|O_WRONLY);
link("a", "b");


讀取或寫入 toais 與讀取或寫入 tob 相同。每個 inode 都由唯一的 inode 編號標識。在上面的代碼序列之後，可以通過檢查結果 offstat 來確定 aandb 引用相同的底層內容：兩者都將返回相同的 inode 編號 （ino），然後 linkcount 將設置為 2。unlinksystem 調用會從文件系統中刪除名稱。僅當文件的連結計數為零且沒有檔描述符引用它時，才會釋放檔的 inode 和保存其內容的磁碟空間。因此，將

unlink("a");


到最後一個代碼序列，使 inode 和文件內容可訪問 ASB。此外

fd = open("/tmp/xyz", O_CREATE|O_RDWR);
unlink("/tmp/xyz");


是創建沒有名稱的臨時 inode 的一種慣用方法，當進程 closesfdor 退出時，該 inode 將被清理。Unix 提供了可從shell作為使用者級程式調用的文件實用程式，例如 mkdir、ln 和 andrm。此設計允許任何人通過添加新的使用者級程式來擴展命令行介面。事後看來，這個計劃似乎很明顯，但是在 Unix 時代設計的其他系統經常將此類命令內置到 shell 中（並將 shell 內置到內核中）。一個例外是shell（user/sh.c：161）.cd中內置的 cd 必須更改shell本身的當前工作目錄。Ifcd作為常規命令運行，則shell將

fork 一個子進程，子進程將運行 cd，而 cd 將更改子進程的工作目錄。父級（即 shell）的工作目錄不會更改。

### 1.5 Real world

Unix 將「標準」檔描述符、管道和方便的shell語法組合在一起，用於對它們進行操作，這是編寫通用可重用程式的重大進步。這個想法引發了一種“軟體工具”文化，這種文化是 Unix 的大部分力量和受歡迎程度的原因，而 shell 是第一個所謂的“腳本語言”。Unix 系統調用介面今天在 BSD、Linux 和 macOS 等系統中仍然存在。Unix 系統調用介面已通過可移植作業系統介面 （POSIX） 標準進行了標準化。Xv6 不符合 POSIX：它缺少許多系統調用（包括基本的調用，如 lseek），並且它提供的許多系統調用與標準不同。我們對 xv6 的主要目標是簡單明瞭，同時提供一個簡單的類似 UNIX 的系統調用介面。一些人已經通過更多的系統調用和一個簡單的 C 庫擴展了 xv6，以便運行基本的 Unix 程式。但是，與 xv6 相比，現代內核提供了更多的系統調用和更多種類的內核服務。例如，它們支持網路工作、視窗系統、用戶級線程、許多設備的驅動程式等。現代內核持續快速發展，並提供POSIX之外的許多功能。Unix 使用一組檔名和檔描述符介面對多種類型的資源（文件、目錄和設備）進行統一訪問。這個想法可以擴展到更多種類的資源;一個很好的例子是 Plan 9 \[16\]，它將 「資源是檔」 的概念應用於網路、圖形等。但是，大多數 Unix 派生的操作系統都沒有遵循這條路線。檔系統和檔描述符是強大的抽象。即便如此，還有其他用於操作系統介面的模型。 Multics 是 Unix 的前身，它以一種看起來像記憶體的方式抽象了檔存儲，從而產生了一種非常不同的介面風格。Multics 設計的複雜性直接影響了 Unix 的設計人員，他們的目標是構建更簡單的東西。Xv6 不提供使用者的概念或保護一個使用者免受另一個用戶的影響;在 Unix 術語中，所有 xv6 進程都以 root 身份運行。本書研究了 xv6 如何實現其類似 Unix 的介面，但這些思想和概念不僅適用於 Unix。任何操作系統都必須將進程多路複用到底層硬體上，將進程彼此隔離，併為受控的進程間通信提供機制。學習 xv6 後，您應該能夠查看其他更複雜的作業系統，並在這些系統中看到 xv6 的底層概念。

### 1.6 Exercises

1. 編寫一個程式，該程式使用 UNIX 系統調用在一對管道（每個方向一個管道）上兩個進程之間“乒乓”一個字節。測量程式的性能，以每秒換發次數為單位。

第 2 章
=====

Operating system organization
=============================

操作系統的一個關鍵要求是同時支援多個活動。例如，使用第 1 章中描述的系統調用介面，一個進程可以使用 fork 啟動新的進程。操作系統必須在這些進程之間時間共用計算機的資源。例如，即使進程數多於硬體CPU數，操作系統也必須確保所有進程都有機會執行。操作系統還必須安排進程之間的隔離。也就是說，如果一個進程有bug和故障，它不應該影響不依賴於bug進程的進程。然而，完全隔離太強了，因為進程應該有可能有意識地交互;管道就是一個例子。因此，操作系統必須滿足三個要求：多路複用、隔離和交互。

本章概述了如何組織操作系統以實現這三個要求。事實證明，有很多方法可以做到這一點，但本文重點介紹以非單體內核為中心的主流設計，許多 Unix 操作系統都使用這種內核。本章還概述了 xv6 進程（xv6 中的隔離單元）以及 xv6 啟動時第一個進程的創建。

Xv6 運行在多核^1 RISC-V 微處理器上，它的大部分低級功能（例如，它的工藝實現）都是特定於 RISC-V 的。RISC-V 是 64 位的 CPU，xv6 是用 “LP64” C 編寫的，這意味著 C 程式設計語言中的長 （L） 和指標 （P） 是 64 位，但 anintis 是 32 位。本書假設讀者已經對一些架構進行了一些機器級程式設計，並將在出現 RISC-V 特定的想法時介紹它們。使用者級 ISA \[2\] 和特權架構 \[3\] 文檔是完整的規範。您還可以參考“RISC-V 閱讀器：開放式架構圖集” \[15\]。

完整計算機中的CPU由支援硬體包圍，其中大部分以I/O介面的形式存在。Xv6 是為 qemu 的 “-machine virt” 選項類比的支持硬體編寫的。這包括 RAM、包含引導代碼的 ROM、與使用者鍵盤/螢幕的串行連接以及用於存儲的磁碟。

（^1）本文所說的 「multi-core」 是指共用記憶體但並行執行的多個 CPU，每個 CPU 都有自己的一組寄存器。本文有時使用術語 multiprocessor作為 multi-core 的同義詞，儘管 multiprocessor 也可以更具體地指具有多個不同處理器晶元的計算機。

### 2.1 抽象物理資源

遇到操作系統時，人們可能會問的第一個問題是為什麼還要擁有它？也就是說，可以將圖 1.2 中的系統調用實現為一個庫，應用程式與該庫連結。在這個計劃中，每個應用程式甚至可以擁有自己的庫來滿足其需求。應用程式可以直接與硬體資源交互，並以最適合應用程式的方式使用這些資源（例如，實現高性能或可預測的性能）。一些用於嵌入式設備或實時系統的操作系統就是以這種方式組織的。這種庫方法的缺點是，如果有多個應用程式正在運行，則應用程式必須運行良好。例如，每個應用程式都必須定期放棄CPU，以便其他應用程式可以運行。如果所有應用程式都相互信任並且沒有 bug，那麼這種 acooperativetime-sharing 方案可能是可以的。應用程式彼此不信任並且存在 bug 更為典型，因此人們通常需要比協作方案提供的更強的隔離。為了實現強隔離，禁止應用程式直接訪問敏感的硬體資源，而是將資源抽象到服務中是有説明的。例如，Unix 應用程式僅通過文件系統的 open、read、write 和 closesystem 調用與儲存交互，而不是直接讀取和寫入磁碟。這為應用程式提供了路徑名的便利性，並允許操作系統（作為介面的實現者）管理磁碟。即使不考慮隔離，有意交互（或只是希望不妨礙彼此）的程式也可能會發現文件系統比直接使用磁碟更方便的抽象。 同樣，Unix 在進程之間透明地切換硬體 CPU，根據需要保存和恢復寄存器狀態，這樣應用程式就不必知道分時。這種透明度允許操作系統共用CPU，即使某些應用程式處於無限迴圈中。再舉一個例子，Unix進程使用 exec 來構建其記憶體映射，而不是直接與物理記憶體交互。這允許os決定將進程放置在記憶體中的位置;如果記憶體緊張，操作系統甚至可能在 disk.exec 上存儲一些進程的數據，還為使用者提供了文件系統存儲可執行程式映像的便利。Unix 進程之間的許多形式的交互都是通過檔描述符進行的。檔描述符不僅抽象出許多細節（例如，管道或檔中的數據的存儲位置），而且還以簡化交互的方式定義它們。例如，如果管道中的一個應用程式發生故障，則內核會為管道中的下一個進程生成文件結束信號。圖 1.2 中的系統調用介面經過精心設計，既為程式師提供了便利，又提供了強隔離的可能性。Unix 介面不是抽象資源的唯一方法，但事實證明它是一個很好的方法。

### 2.2 User mode, supervisor mode, and system calls

強隔離要求應用程式和操作系統之間有一個硬邊界。如果應用程式出錯，我們不希望操作系統失敗或其他應用程式失敗

失敗。相反，操作系統應該能夠清理失敗的應用程式並繼續運行其他應用程式。為了實現強隔離，操作系統必須安排應用程式無法修改（甚至讀取）操作系統的數據結構和指令，並且應用程式無法訪問其他進程的記憶體。CPU 為強隔離提供硬體支援。例如，RISC-V 有三種 CPU 可以執行指令的模式：機器模式、管理模式和使用者模式。在機器模式下執行的指令具有完全許可權;CPU 以電腦模式啟動。計算機模式主要用於在啟動期間設置計算機。Xv6 在機器模式下執行幾行，然後更改為 supervisor 模式。在 Supervisor 模式下，允許 CPU 執行特權指令：例如，接收和禁用中斷，讀取和寫入保存頁表位址的寄存器等。如果使用者模式下的應用程式嘗試執行特權指令，則 CPU 不會執行該指令，而是切換到 supervisor 模式，以便 supervisor-mode 代碼可以終止應用程式，因為它執行了不應執行的操作。第 1 章中的圖 1.1 說明瞭這個組織。應用程式只能執行使用者模式指令（例如，添加數位等），並稱為在用戶空間中運行，而處於supervisor模式的軟體也可以執行特權指令，並稱為在 kernel space 中運行。在 kernel space（或 supervisor 模式）中運行的軟體稱為 thekernel。想要調用內核函數的應用程式（例如，xv6 中的 thereadsystem 調用）必須轉換到內核;應用程式不能直接調用內核函數。 CPU 提供特殊指令，將 CPU 從使用者模式切換到 Supervisor 模式，並在內核指定的入口點進入內核。（RISC-V 為此提供了 theecallinstruction。一旦 CPU 切換到 supervisor 模式，內核就可以驗證系統調用的參數（例如，檢查傳遞給系統調用的位址是否是應用程式記憶體的一部分），決定是否允許應用程式執行請求的操作（例如，檢查是否允許應用程式寫入指定的檔）， 然後否認或執行它。內核控制過渡到 supervisor 模式的入口點很重要;例如，如果應用程式可以決定內核入口點，則惡意應用程式可以在跳過參數驗證的位置進入內核。

### 2.3 Kernel organization

一個關鍵的設計問題是操作系統的哪個部分應該在supervisor模式下運行。一種可能性是整個操作系統駐留在內核中，因此所有系統調用的實現都在supervisor模式下運行。這種組織稱為 amonolithic kernel。在此組織中，整個操作系統由一個以完全硬體許可權運行的程序組成。這種組織很方便，因為操作系統設計人員不必決定操作系統的哪些部分不需要完全硬體許可權。此外，操作系統的不同部分更容易協作。例如，操作系統可能具有可由文件系統和虛擬記憶體系統共用的緩衝區緩存。整體式組織的一個缺點是操作系統不同部分之間的交互通常很複雜（我們將在本文的其餘部分看到），因此它

Microkernel


user shell File server
space


kernel
space


(^)發送消息 圖 2.1： 帶有文件系統伺服器的微內核很容易作系統開發人員弄錯。在整體式內核中，錯誤是致命的，因為supervisor模式中的錯誤通常會導致內核失敗。如果內核失敗，計算機將停止工作，因此所有應用程式也會失敗。計算機必須重新啟動才能重新啟動。為了降低內核出錯的風險，OS 設計人員可以最大限度地減少在supervisor模式下運行的作業系統代碼量，並在使用者模式下執行大部分作業系統。這種內核組織稱為 amicrokernel。圖 2.1 說明瞭這種微內核設計。在圖中，檔案系統作為用戶級進程運行。作為進程運行的OS服務稱為伺服器。為了允許應用程式與檔案伺服器交互，內核提供了一種進程間通信機制，用於將消息從一個使用者模式進程發送到另一個使用者模式進程。例如，如果像Shell這樣的應用程式想要讀取或寫入檔，它會向檔案伺服器發送消息並等待回應。在微內核中，內核介面由一些低級函數組成，用於啟動應用程式、發送消息、訪問設備硬體等。這種組織方式使內核相對簡單，因為大多數操作系統駐留在用戶級伺服器中。在現實世界中，單片內核和微內核都很受歡迎。許多 Unix 內核是整體式的。例如，Linux 有一個單片內核，儘管一些操作系統功能作為用戶級伺服器（例如，視窗系統）運行。Linux 為操作系統密集型應用程式提供高性能，部分原因是內核的子系統可以緊密集成。 Minix、L4 和 QNX 等作業系統被組織為帶有伺服器的微內核，並在嵌入式環境中得到廣泛部署。L4 的一個變體 seL4 足夠小，以至於它已經驗證了記憶體安全和其他安全特性 \[8\]。操作系統的開發人員之間關於哪個組織更好有很多爭論，並且沒有確鑿的證據。此外，這在很大程度上取決於“更好”的含義：更快的性能、更小的代碼大小、內核的可靠性、整個操作系統（包括用戶級服務）的可靠性等。還有一些實際的考慮可能比哪個組織的問題更重要。一些操作系統具有微內核，但出於性能原因，在內核空間中運行一些用戶級服務。一些操作系統具有單片內核，因為這是它們開始的方式，並且幾乎沒有動力轉向純微內核組織，因為新功能可能比重寫現有操作系統以適應微內核設計更重要。從本書的角度來看，微內核和單體操作系統有許多共同點。他們實現系統調用，使用頁表，處理中斷，支援

File Description
bio.c Disk block cache for the file system.
console.c Connect to the user keyboard and screen.
entry.S Very first boot instructions.
exec.c exec() system call.
file.c File descriptor support.
fs.c File system.
kalloc.c Physical page allocator.
kernelvec.S Handle traps from kernel.
log.c File system logging and crash recovery.
main.c Control initialization of other modules during boot.
pipe.c Pipes.
plic.c RISC-V interrupt controller.
printf.c Formatted output to the console.
proc.c Processes and scheduling.
sleeplock.c Locks that yield the CPU.
spinlock.c Locks that don’t yield the CPU.
start.c Early machine-mode boot code.
string.c C string and byte-array library.
swtch.S Thread switching.
syscall.c Dispatch system calls to handling function.
sysfile.c File-related system calls.
sysproc.c Process-related system calls.
trampoline.S Assembly code to switch between user and kernel.
trap.c C code to handle and return from traps and interrupts.
uart.c Serial-port console device driver.
virtio_disk.c Disk device driver.
vm.c Manage page tables and address spaces.


Figure 2.2: Xv6 kernel source files.


進程，它們使用鎖進行併發控制，它們實現文件系統等。本書重點介紹這些核心思想。與大多數 Unix 作業系統一樣，Xv6 是作為整體內核實現的。因此，xv6 內核介面對應於操作系統介面，內核實現完整的操作系統。由於 xv6 提供的服務不多，因此它的內核比一些微內核小，但從概念上講，xv6 是單體的。

### 2.4 Code: xv6 organization

xv6 內核源代碼位於 kernel/sub-directory 中。源檔被劃分為多個檔，遵循一個粗略的模組化概念;圖 2.2 列出了這些檔。模組間接口在

0


user text
and data


user stack


heap


MAXVA
trampoline
trapframe


Figure 2.3: Layout of a process’s virtual address space


defs.h(kernel/defs.h).

### 2.5 流程概述

xv6 中的隔離單元（與其他 Unix 作業系統一樣）是 aprocess。進程濫用可以防止一個進程破壞或監視另一個進程的記憶體、CPU、檔描述符等。它還可以防止進程破壞內核本身，因此進程無法破壞內核的隔離機制。內核必須小心實現進程抽象，因為有缺陷或惡意的應用程式可能會欺騙內核或硬體做壞事（例如，規避隔離）。內核用於實現進程的機制包括user/supervisor模式標誌、位址空間和線程的時間切片。為了幫助實施隔離，進程抽象為程式提供了它擁有自己的私有計算機的錯覺。進程為程式提供似乎是私有記憶體系統或位址空間的東西，其他進程無法讀取或寫入。進程還為程式提供似乎是其自己的 CPU 來執行程式的指令。Xv6 使用頁表（由硬體實現）為每個進程提供自己的廣告空間。RISC-V 頁表將虛擬位址（RISC-V 指令操作的位址）轉換（或“映射”）為非物理位址（CPU 發送到主記憶體的位址）。Xv6 為每個進程維護一個單獨的頁表，該頁表定義該進程的位址空間。如圖 2.3 所示，地址空間包括從虛擬位址 0 開始的進程的用戶記憶體。首先是指令，然後是全域變數，然後是堆疊，最後是進程可以根據需要擴展的“堆”區域（對於 malloc）。 有許多因素限制了進程位址空間的最大大小：RISC-V 上的指標寬 64 位;硬體在頁表中查找虛擬位址時僅使用低 39 位;而 xv6 只使用這 39 位中的 38 位。因此，最大位址為 238 − 1 = 0x3fffffffff，即

isMAXVA（kernel/riscv.h：378） 中。地址空間 xv6 的頂部放置了 atrampolinepage（4096 位元組）和 atrapframepage。Xv6 使用這兩個頁面來過渡到內核並返回;trampoline 頁面包含用於傳入和傳出內核的代碼，而 trapframe 是內核保存進程使用者寄存器的地方，如第 4 章所述。

xv6 內核為每個進程維護許多狀態，並將其收集到 astruct proc （kernel/proc.h：85） 中。進程最重要的內核狀態部分是其頁表、內核堆疊和運行狀態。我們將使用符號 p->xxx 來引用 procstructure 的元素;例如，p->pagetable是指向進程頁表的指標。

每個進程都有一個控制線程（或簡稱 thread），它保存執行進程所需的狀態。在任何給定時間，線程可能正在CPU上執行或暫停（未執行，但能夠在將來恢復執行）。要在進程之間切換 CPU，內核會暫停當前在該 CPU 上運行的線程並保存其狀態，並恢復另一個進程之前暫停的線程的狀態。線程的大部分狀態（本地變數、函數調用返回位址）都存儲在線程的堆疊上。每個進程有兩個堆疊：用戶堆疊和內核堆疊 （p->kstack）。當進程執行使用者指令時，只有其用戶堆疊正在使用，並且其內核堆疊為空。當進程進入內核（用於系統調用或中斷）時，內核代碼將在進程的內核堆棧上執行;當進程位於內核中時，其用戶堆疊仍包含已保存的數據，但未被主動使用。進程的線程在主動使用其用戶堆疊和內核堆疊之間交替。內核堆疊是獨立的（並且不受用戶代碼的影響），因此即使進程破壞了其使用者堆疊，內核也可以執行。

進程可以通過執行 RISC-Vecall 指令進行系統調用。此指令提高硬體許可權級別，並將 program counter 更改為內核定義的入口點。入口點的代碼切換到進程的內核堆疊，並執行實現 system 調用的內核指令。當系統調用完成時，內核會切換回使用者堆棧，並通過調用 thesretinstruction 傳回使用者空間，這會降低硬體許可權級別，並在系統調用指令之後立即恢復執行使用者指令。進程的線程可以在內核中 「阻塞」 以等待 I/O，並在 I/O 完成後從中斷的地方恢復。

p->state指示進程是否已分配、準備運行、當前在CPU上運行、等待I/O或正在退出。

p->pagetable保存進程的頁表，格式為 RISC-V 硬體指定的格式。Xv6 會導致分頁硬體在用戶空間中執行該進程時使用 process『sp->pagetable。進程的頁表還用作為存儲進程記憶體而分配的物理頁的地址的記錄。

總之，一個進程捆綁了兩個設計思想：一個位址空間，用於給進程帶來自己記憶體的錯覺，一個線程給進程帶來自己的 CPU 的錯覺。在 xv6 中，進程由一個位址空間和一個線程組成。在實際操作系統中，一個進程可能有多個線程來利用多個CPU。

### 2.6 代碼：啟動 xv6，第一個進程和系統調用

為了使 xv6 更具體，我們將概述內核如何啟動和運行第一個進程。後續章節將更詳細地描述本概述中顯示的機制。

當 RISC-V 電腦開機時，它會自我初始化並運行存儲在唯讀記憶體中的引導載入程式。引導載入程式將 xv6 內核載入記憶體中。然後，在機器模式下，CPU 執行 xv6 啟動 at\_entry（kernel/entry.S：7）。RISC-V 從禁用分頁硬體開始：虛擬位址直接映射到物理位址。

載入程式將 xv6 內核載入到物理位址 0x80000000 的記憶體中。它將內核置於 0x80000000 而不是 0x0 的原因是位址範圍0x0：0x80000000 包含 I/O 設備。

這些說明at\_entryset堆疊，以便 xv6 可以運行 C 代碼。Xv6 在 filestart.c（kernel/start.c：11） 中聲明了初始堆棧 stack0 的空間。該代碼at\_entryloads堆疊指標 registersp 與位址 stack0+4096（堆棧的頂部）進行交互，因為 RISC-V 上的堆疊會向下增長。現在內核已經有了一個堆疊，\_entrycalls 在 start （kernel/start.c：15） 進入 C 代碼。

functionstart執行一些僅在電腦模式下允許的配置，然後切換到 supervisor 模式。要進入 supervisor 模式，RISC-V 提供了指令 mret。這條指令最常用於從上一個從 supervisor 模式返回到機器模式.start不是從這樣的調用返回，而是像這樣設置：它在 registermstatus 中將以前的許可權模式設置為 supervisor，通過將 main 的位址寫入 registermepc 來將返回地址設置為 main，通過將 0 寫入頁表 registersatp 來禁用 supervisor 模式下的虛擬地址轉換， 並將所有中斷和異常委託給 Supervisor 模式。

在跳轉到 Supervisor 模式之前，start執行另一項任務：它對 clock chip 進行程式設計以產生 timer 中斷。完成這個內務處理後，通過調用 mret 開始「返回」監督模式。這會導致程式計數器更改為main（kernel/main.c：11），即之前存儲在mepc中的位址。

在 main（kernel/main.c：11）初始化多個設備和子系統後，它通過調用 userinit（kernel/proc.c：233） 創建第一個進程。第一個進程執行一個用 RISC-V 彙編編寫的小程式，該程式在 xv6.initcode.S（user/initcode.S：3）將 execsystem 調用 SYS\_EXEC（kernel/syscall.h：8） 的號碼載入到 registera7 中，然後調用 ecall重新進入內核。

內核使用 registera7insyscall（kernel/syscall.c：132） 中的數位來調用所需的系統調用。系統調用 table（kernel/syscall.c：107）mapsSYS\_EXECto內核調用的 functionsys\_exec。正如我們在第 1 章中看到的，exec 用一個新程式（在本例中為 /init）替換當前進程的記憶體和寄存器。

一旦內核完成 completedexec，它就會返回到 /initprocess.init 中的用戶空間 （user/init.c：15），如果需要，創建一個新的控制台設備檔，然後作為檔描述符 0、1 和 2 打開它。然後，它在控制臺上啟動一個shell。系統已啟動。

### 2.7 安全模型

您可能想知道操作系統如何處理錯誤或惡意代碼。因為應對惡意比處理意外錯誤更難，所以主要專注於提供針對惡意的安全性是合理的。以下是操作系統設計中典型安全假設和目標的高級視圖。操作系統必須假定進程的用戶級代碼將盡最大努力破壞內核或其他進程。用戶代碼可能會嘗試取消引用其允許的位址空間之外的指標;它可能會嘗試執行任何 RISC-V 指令，即使是那些不用於用戶代碼的指令;它可能會嘗試讀取和寫入任何 RISC-V 控制寄存器;它可能會嘗試直接訪問設備硬體;它可能會將聰明的值傳遞給系統調用，以試圖欺騙內核崩潰或做一些愚蠢的事情。內核的目標是限制每個用戶進程，以便它所能做的只是讀/寫/執行自己的用戶記憶體，使用 32 個通用的 RISC-V 寄存器，並以系統調用允許的方式影響內核和其他進程。內核必須阻止任何其他操作。這通常是內核設計中的絕對要求。對內核自身代碼的期望完全不同。內核代碼假定由善意且細心的程式師編寫。內核代碼應該沒有錯誤，並且肯定不包含任何惡意內容。這個假設會影響我們分析內核代碼的方式。例如，如果內核代碼錯誤地使用它們，則有許多內部內核函數（例如，旋轉鎖）將導致嚴重問題。在檢查任何特定的內核代碼時，我們要說服自己它的行為是正確的。 但是，我們假設內核代碼通常是正確編寫的，並遵循有關使用內核自身函數和數據結構的所有規則。在硬體級別，假設 RISC-V CPU、RAM、磁碟等按照文檔中宣傳的那樣運行，沒有硬體錯誤。當然，在現實生活中，事情並不那麼簡單。很難防止聰明的用戶代碼通過消耗受內核保護的資源來使系統不可用（或導致系統崩潰）

*   磁碟空間、CPU 時間、進程表槽等。通常不可能編寫無錯誤的內核代碼或設計無錯誤的硬體;如果惡意使用者代碼的編寫者知道內核或硬體錯誤，他們將利用這些錯誤。即使在成熟的、廣泛使用的內核中，例如Linux，人們也會不斷發現新的漏洞\[1\]。在內核中設計保護措施以防止它有bug的可能性是值得的：斷言、類型檢查、堆疊保護頁面等。最後，用戶代碼和內核代碼之間的區別有時很模糊：一些特權用戶級進程可能提供基本服務並有效地成為操作系統的一部分，而在某些操作系統中，特權用戶代碼可以將新代碼插入內核（就像 Linux 的可載入內核模組一樣）。

### 2.8 Real world

大多數操作系統都採用了進程概念，並且大多數進程看起來與 xv6 的進程相似。但是，現代操作系統支援一個進程中的多個線程，以允許單個進程利用多個CPU。在一個進程中支援多個線程涉及相當多的機制，而 xv6 沒有，通常包括介面更改（例如，Linux 的 sclone、

variant offork）來控制進程線程共用的方面。

### 2.9 Exercises

1. 添加對 xv6 的系統調用，該調用返回可用內存量。

第 3 章
=====

頁表
==

頁表是最流行的機制，操作系統通過它為每個進程提供自己的私有位址空間和記憶體。頁表確定記憶體廣告的含義以及可以訪問物理記憶體的哪些部分。它們允許 xv6 隔離不同進程的位址空間，並將它們多路復用到單個物理記憶體中。Page tab- bles 是一種流行的設計，因為它們提供了一定程度的間接性，允許操作系統執行許多技巧。Xv6 執行了一些技巧：在多個位址空間中映射相同的記憶體（一個 trampoline 頁面），並使用未映射的頁面保護內核和用戶堆棧。本章的其餘部分解釋了 RISC-V 硬體提供的頁表以及 xv6 如何使用它們。

### 3.1 Paging hardware

提醒一下，RISC-V 指令 （使用者和內核） 會操作虛擬位址。馬的 RAM 或物理記憶體與物理位址建立索引。RISC-V 頁表硬體通過將每個虛擬位址映射到物理位址來連接這兩種類型的位址。Xv6 在 Sv39 RISC-V 上運行，這意味著僅使用 64 位虛擬位址的底部 39 位;不使用前25位。在此 Sv39 配置中，RISC-V 頁表在邏輯上是一個包含 227 （134,217,728） 頁表條目 （PTE） 的陣列。每個 PTE 都包含一個 44 位物理頁碼 （PPN） 和一些標誌。分頁硬體通過使用 39 位的前 27 位索引到頁表中以查找 PTE，並生成一個 56 位物理位址，其前 44 位來自 PTE 中的 PPN，其底部 12 位從原始虛擬位址複製。圖 3.1 顯示了這個過程，頁表的邏輯視圖是一個簡單的 PTE 陣列（參見圖 3.2 以獲得更完整的故事）。頁表使操作系統能夠控制 4096 （ 212 ） 位元組的對齊塊的粒度從虛擬到物理位址的轉換。這樣的塊稱為 apage。在 Sv39 RISC-V 中，虛擬位址的前 25 位不用於轉換。物理位址也有增長空間：PTE 格式中還有空間讓物理頁碼再增長10位。RISC-V 的設計者根據技術預測選擇了這些數位。239 位元組是512 GB，對於運行的應用程式來說，這應該足夠了

Virtual address


Physical Address


12
Offset


12


PPN Flags


0


1


10


Page table


27
EXT


（^44） 2^27 44 索引 25 64 56 圖 3.1：RISC-V 虛擬位址和物理位址，具有簡化的邏輯頁表。在 RISC-V 電腦上。256 的物理記憶體空間在不久的將來足以容納許多 I/O 設備和 RAM 晶片。如果需要更多，RISC-V 設計人員已經定義了具有 48 位虛擬位址的 Sv48 \[3\]。如圖 3.2 所示，RISC-V CPU 通過三個步驟將虛擬位址轉換為物理位址。頁表作為三級樹存儲在物理記憶體中。樹的根是一個 4096 位元組的頁表頁，其中包含 512 個 PTE，其中包含樹的下一級別中頁表頁的物理位址。其中每個頁面都包含樹中最後一個級別的 512 個 PTE。分頁硬體使用 27 位的前 9 位來選擇根頁表頁中的 PTE，中間的 9 位來選擇樹的下一級別的頁表頁中的 PTE，使用後 9 位來選擇最終的 PTE。（在 Sv48 RISC-V 中，頁表有四個級別，虛擬位址索引的 39 到 47 位進入頂層。如果轉換位址所需的三個 PTE 中的任何一個不存在，則分頁硬體會引發 apage-fault 異常，將其留給內核來處理異常（請參閱第 4 章）。與圖 3.1 的單級設計相比，圖 3.2 的三級結構允許以一種節省記憶體的方式來記錄 PTE。在大範圍虛擬位址沒有映射的常見情況下，三級結構可以省略整個頁面目錄。例如，如果應用程式只使用從位址 0 開始的幾個頁面，那麼頂級頁面目錄的條目 1 到 511 是無效的，內核不必為 511 個中間頁面目錄分配頁面。 此外，內核也不必為這 511 個中間頁面目錄的底層頁面目錄分配頁面。因此，在此示例中，三級設計為中間頁面目錄保存了511個頁面，為底層頁面目錄保存了511×512個頁面。儘管 CPU 在執行 load 或 store 指令時在硬體中採用三級結構，但三級的潛在缺點是 CPU 必須從記憶體中載入三個 PTE，才能將 load/store 指令中的虛擬位址轉換為物理位址。為了避免從物理記憶體載入 PTE 的成本，RISC-V CPU 將頁表條目緩存在 Translation Look-aside Buffer （TLB） 中。

Physical Page Number


6
A


543
U


2
W


1
V


63 8910 07


V
R
W
X
U
AD


*   Valid
*   讀
*   Writable
*   Executable
*   User
*   Accessed
*   髒（頁面目錄中的 0）

Virtual address Physical Address
9 12
L1 L0 Offset


12
PPN Offset


PPN Flags


0


1


10


Page Directory


satp


L2


PPN Flags


0


1


44 10


Page Directory


PPN Flags


0


1


511


10


Page Directory


9 9
EXT


9


511
511


44


44


44


D GU X R


A - Accessed
-G - Global


RSW


Reserved for supervisor software


53
Reserved


Figure 3.2: RISC-V address translation details.


每個 PTE 都包含標誌位，這些標誌位告訴分頁硬體如何允許使用關聯的虛擬位址。PTE\_Vindicates PTE 是否存在：如果未設置，則對頁面的引用會導致異常（即不允許）。PTE\_Rcontrols是否允許將說明讀到該頁面。PTE\_Wcontrols是否允許將指令寫入頁面。PTE\_X 控制CPU是否可以將頁面內容解釋為指令並執行它們。PTE\_Ucontrols 是否允許使用者模式下的指令訪問該頁面;ifPTE\_Uis未設置，則 PTE 只能在 Supervisor 模式下使用。圖 3.2 顯示了這一切是如何工作的。標誌和所有其他與頁面硬體相關的結構在 （kernel/riscv.h） 中定義。

要告訴 CPU 使用頁表，內核必須將根頁錶頁的物理位址寫入 thesatpregister。CPU 將使用其 ownsatp 指向的頁表轉換後續指令生成的所有位址。每個CPU都有自己的 satpso，因此不同的CPU可以運行不同的進程，每個進程都有一個私有地址空間，由自己的頁表描述。

從內核的角度來看，頁表是存儲在記憶體中的數據，內核使用的代碼創建和修改頁表，就像您可能看到的任何樹形數據結構一樣。

關於本書中使用的術語的一些說明。物理記憶體是指 RAM 中的儲存單元。物理記憶體的一個字節有一個位址，稱為非物理位址。取消引用位址 （（如載入、存儲、跳轉和函數調用） ）的指令僅使用虛擬位址，分頁硬體將其轉換為物理位址，然後發送到 RAM 硬體以讀取或寫入存儲。Anaddress space是在給定頁表中有效的虛擬位址集;

每個 XV6 進程都有一個單獨的使用者位址空間，XV6 內核也有自己的地址空間。用戶記憶體是指進程的使用者位址空間加上頁表允許進程訪問的物理記憶體。虛擬記憶體是指與管理頁表並使用它們來實現隔離等目標相關的思想和技術。

0


Trampoline


Unused


Unused


Kstack 0 Unused


Guard page


Kstack 1


Guard page


0x1000
0


R-X


Virtual Addresses


CLINT


Kernel text


boot ROM


2^56-1 Physical Addresses


Unused
and other I/O devices


0x02000000


0x0C000000 PLIC

UART0


VIRTIO disk 0x10000000

0x10001000

KERNBASE
(0x80000000)


PHYSTOP
(0x88000000)


MAXVA


Kernel data


R-X


RW-


Physical memory (RAM)


VIRTIO disk
UART0


PLIC


RW-
RW-


RW-


Free memory RW-


---


---
RW-
RW-


圖 3.3： 左側是 xv6 的內核地址空間。RWX引用 PTE 讀取、寫入和執行許可權。右側是 xv6 希望看到的 RISC-V 物理地址空間。

### 3.2 Kernel address space

Xv6 為每個進程維護一個頁表，描述每個進程的使用者位址空間，以及一個描述內核位址空間的單頁表。內核配置其廣告空間的佈局，以 Predictable 的速度存取物理記憶體和各種硬體資源

虛擬位址。圖 3.3 顯示了這種佈局如何將內核虛擬位址映射到物理廣告。檔 （kernel/memlayout.h） 聲明了 xv6 的內核記憶體佈局的常量。QEMU 類比一台計算機，該計算機包括 RAM（物理記憶體），從物理 ad- dress0x80000000 開始，一直持續到至少 0x88000000，xv6 稱為 PHYSTOP。QEMU 類比還包括 I/O 設備，例如磁碟介面。QEMU 將設備介面公開給位於物理位址空間 0x80000000 以下的 memory-mappedcontrol 寄存器。內核可以通過讀/寫這些特殊的物理位址來與設備交互;此類讀取和寫入與設備硬體通信，而不是與 RAM 通信。第 4 章解釋了 xv6 如何與設備交互。內核使用 「直接映射」 獲取 RAM 和記憶體映射的設備寄存器，即在等於物理位址的虛擬位址處映射資源。例如，內核本身位於虛擬位址空間和物理記憶體中的 KERNBASE=0x80000000 處。直接映射簡化了讀取或寫入物理記憶體的內核代碼。例如，當 fork 為子進程分配用戶記憶體時，分配器返回該記憶體的物理位址;fork 在將父級的用戶記憶體複製到子級時，直接將該地址作為虛擬位址。有幾個內核虛擬位址不是直接映射的：

*   蹦床頁面。它被映射在虛擬位址空間的頂部;用戶頁表具有相同的映射。第 4 章討論了 trampoline 頁面的作用，但我們在這裡看到了一個有趣的頁表用例;物理頁（保存 trampoline 代碼）在內核的虛擬位址空間中映射兩次：一次在虛擬位址空間的頂部，一次使用直接映射。
*   內核堆疊頁面。每個進程都有自己的內核堆疊，該堆疊被映射到高處，因此在其下方 xv6 可以留下一個 unmappedguard 頁面。保護頁的 PTE 無效（即未設置PTE\_Vis），因此如果內核溢出內核堆棧，則可能會導致異常，並且內核將崩潰。如果沒有保護頁，溢出的堆疊將覆蓋其他內核記憶體，從而導致操作不正確。恐慌崩潰是可取的。雖然 kernel 通過 high-memory mapping使用其堆疊，但內核也可以通過直接映射的地址訪問它們。替代設計可能只有直接映射，並使用直接映射位址處的堆疊。但是，在這種安排中，提供保護頁將涉及取消映射虛擬位址，否則這些位址將引用物理記憶體，這將很難使用。內核將 trampoline 的頁面和內核文本與 permissionsPTE\_R andPTE\_X 進行映射。內核從這些頁面讀取並執行指令。內核將其他頁面與 permissionsPTE\_RandPTE\_W 映射，以便它可以讀取和寫入這些頁面中的記憶體。保護頁的映射無效。

### 3.3 代碼：創建位址空間

大多數用於操作位址空間和頁表的 xv6 代碼位於 vm.c（ker- nel/vm.c：1） 中。中央數據結構ispagetable\_t，它實際上是指向 RISC-V 的指標

根頁-表頁;apagetable\_tmay可以是內核頁表，也可以是每個進程的頁表之一。中心功能包括 walk（查找虛擬位址的 PTE）和 mappages（為新映射安裝 PTE）。以 kvm 開頭的函數操作內核頁表;以 uvm 操作用戶頁表的函數;其他函數用於 .copyoutandcopyIncopy 數據到和從作為系統調用參數提供的用戶虛擬位址;它們是 invm.c，因為它們需要顯式轉換這些位址才能找到相應的物理記憶體。

在啟動序列的早期，maincallskvminit（kernel/vm.c：54）使用 kvmmake（kernel/vm.c：20） 創建內核的頁面。此調用發生在 xv6 在 RISC-V 上啟用分頁之前，因此位址直接引用物理記憶體。kvmmakefirst 分配一個物理記憶體頁來保存根頁表頁。然後，它調用 kvmmap來安裝內核所需的翻譯。轉換包括內核的指令和數據、直到 PHYSTOP 的物理記憶體以及實際devices.proc\_mapstacks 的記憶體範圍（kernel/proc.c：33）為每個進程分配一個內核堆疊。它調用 kvmmap將每個堆疊映射到 KSTACK 產生的虛擬位址，從而為無效的堆疊保護頁面留出空間。

kvmmap（kernel/vm.c：132）調用mappages（kernel/vm.c：144），它將一系列虛擬位址到相應物理位址範圍的映射安裝到一個頁表中。它以頁面間隔對範圍中的每個虛擬位址分別執行此操作。對於每個要映射的虛擬位址，mappagescallswalk查找該位址的 PTE 位址。然後，它會初始化 PTE 以保存相關的物理頁碼、所需的許可權（PTE\_W、PTE\_X 和/或 PTE\_R），andPTE\_Vto將 PTE 標記為有效 （kernel/vm.c：165）。

walk（kernel/vm.c：86）類比 RISC-V 分頁硬體，因為它在 PTE 中查找虛擬位址（參見圖 3.2）。walk將頁表逐級下降，使用每級的 9 位虛擬位址對相關頁目錄頁進行索引。在每個級別，它都會找到下一級頁面目錄頁面的 PTE，或者最終頁面 （kernel/vm.c：92） 的 PTE。如果第一級或第二級頁面目錄頁面中的 PTE 無效，則尚未分配所需的目錄頁面;如果設置了alloc參數，則 walk分配一個新的頁錶頁面並將其物理位址放在 PTE 中。它返回樹中最低層 PTE 的位址 （kernel/vm.c：102）。

上面的代碼依賴於物理記憶體被直接映射到內核虛擬廣告空間。例如，aswalkdescends 頁表的級別，它會從 PTE（kernel/vm.c：94）中提取下一級頁表的（物理）位址，然後使用該位址作為虛擬位址來獲取下一級 PTE（kernel/vm.c：92）。

maincallskvminithart（kernel/vm.c：62）來安裝內核頁表。它將根頁表頁的物理位址寫入 registersatp。在此之後，CPU 將使用內核頁表翻譯廣告。由於內核使用直接映射，因此下一條指令的 now 虛擬位址將映射到正確的物理記憶體位址。

每個 RISC-V CPU 都將頁表條目緩存在 TLB 中，當 xv6 更改頁表時，它必須告訴 CPU 使相應的緩存 TLB 條目失效。如果沒有，那麼在以後的某個時候，TLB 可能會使用舊的緩存映射，指向同時已分配給另一個進程的物理頁，並且作為結果，一個進程可能能夠在其他進程的記憶體中塗鴉。RISC-V 有一個

instructionsfence.vma刷新當前 CPU 的 TLB。Xv6 在重新載入 satp 寄存器後執行 ssfence.vmain kvminithart，並在返回使用者空間之前切換到用戶頁表的 trampoline 代碼中（kernel/trampoline.S：89）。還需要在 changingsatp 之前 issuefence.vma，以便等待完成所有未完成的負載和存儲。此等待可確保對 page table 的先前更新已完成，並確保先前的載入和存儲使用舊的 page table，而不是新的 page table。為避免刷新完整的 TLB，RISC-V CPU 可能支援位址空間識別碼 （ASID） \[3\]。然後，內核可以僅刷新特定位址空間的 TLB 條目。Xv6 不使用此功能。

### 3.4 物理記憶體分配

內核必須在運行時為頁表、用戶記憶體、內核堆棧和管道緩衝區分配和釋放物理記憶體。Xv6 使用內核末尾和 PHYSTOP 之間的物理記憶體進行運行時分配。它一次分配和釋放整個 4096 位元組的頁面。它通過在頁面本身之間串接一個鏈表來跟蹤哪些頁面是空閒的。分配包括從鏈表中刪除頁面;釋放包括將釋放的頁面添加到清單中。

### 3.5 代碼：物理記憶體分配器

分配器駐留在 inkalloc.c（kernel/kalloc.c：1） 中。分配器的數據結構是可用於分配的物理記憶體頁的自由清單。每個空閑頁面的 list 元素都是一個 struct run（kernel/kalloc.c：17）。分配器從哪裡獲得保存該數據結構的記憶體？它將每個免費頁面的 srunstructure 儲存在免費頁面本身中，因為那裡沒有存儲任何其他內容。空閒清單受旋轉鎖 （kernel/kalloc.c：21-24） 保護。清單和鎖包裝在一個結構中，以明確該鎖保護結構中的欄位。現在，忽略 lock 和對 acquireandrelease 的調用;第 6 章將詳細研究鎖定。函數maincallskinit初始化分配器（kernel/kalloc.c：27）.kinit初始化空閒清單以保存內核末尾和 PHYSTOP 之間的每個頁面。Xv6 應該通過解析硬體提供的配置資訊來確定有多少物理記憶體可用。相反，xv6 假定電腦具有 128 兆位元組的 RAM.kinit調用 freerange，以通過每頁調用 tokfree 將記憶體添加到空閒清單中。PTE 只能引用在 4096 位元組邊界（是 4096 的倍數）上對齊的物理位址，因此 freerange 使用 PGROUNDUP來確保它僅釋放對齊的物理位址。分配器開始時沒有記憶體;這些調用tokfree給它一些來管理。分配器有時將位址視為整數，以便對它們執行算術運算（例如，自由遍歷所有頁面），有時使用位址作為讀取和寫入記憶體的指標（例如，操縱存儲在每個頁面中的 therunstructure）;這種位址的雙重使用是allocator代碼充滿 C 類型轉換的主要原因。

functionkfree（kernel/kalloc.c：47） 首先將要釋放的記憶體中的每個位元組設置為值 1。這將導致在釋放記憶體後使用記憶體的代碼（使用“懸空引用”）讀取垃圾而不是舊的有效內容;希望這會導致此類代碼更快地中斷。Thenkfree將頁面預置到空閒清單：它將 spacast 指標轉換為 struct run，記錄空閒清單的舊開頭 inr->next，並將空閒清單設置為等於 tor.kallocremoves，並返回空閒清單中的第一個元素。

### 3.6 Process address space

每個進程都有自己的頁表，當 xv6 在進程之間切換時，它也會更改頁表。圖 3.4 比圖 2.3 更詳細地顯示了進程的地址空間。進程的使用者記憶體從虛擬位址 0 開始，可以增長到 MAXVA（kernel/riscv.h：375），原則上允許進程尋址 256 GB 的記憶體。進程的位址空間由包含程式文本的頁面（xv6 使用 permissionsPTE\_R、PTE\_X、andPTE\_U 映射）、包含程式預初始化數據的頁面、堆棧頁面和堆頁面組成。Xv6 使用 permissionsPTE\_R、PTE\_W andPTE\_U 映射數據、堆疊和堆。在使用者位址空間內使用許可權是強化用戶進程的常用技術。如果文本被映射withPTE\_W，則進程可能會意外修改自己的程式;例如，程式設計錯誤可能會導致程式寫入NULL指標，修改位址0處的指令，然後繼續運行，這可能會造成更大的破壞。為了立即檢測到此類錯誤，xv6 將文本withoutPTE\_W映射;如果程式意外地嘗試存儲到位址 0，硬體將拒絕執行存儲並引發頁面錯誤（參見 Section 4.6）。然後，內核會終止該進程並列印出一條資訊性消息，以便開發人員可以跟蹤問題。同樣，通過映射數據withoutPTE\_X，用戶程式不會意外跳轉到程序數據中的某個位址並從該位址開始執行。在現實世界中，通過仔細設置許可權來強化進程也有助於抵禦安全攻擊。攻擊者可能會將精心構建的輸入提供給程式（例如，一個 Web 伺服器），它會觸發程式中的錯誤，以期將該錯誤轉化為漏洞 \[14\]。仔細設置許可權和其他技術（例如隨機化用戶位址空間的佈局）使此類攻擊更加困難。堆疊是一個頁面，並顯示由exec創建的初始內容。包含命令行參數的字串以及指向它們的指標陣列位於堆疊的最頂部。緊挨著一些值，這些值允許程式在函數 main（argc，argv） 剛剛被調用時啟動 atmainas。為了檢測用戶堆疊溢出分配的堆疊記憶體，xv6 通過清除 thePTE\_Uflag 在堆疊正下方放置一個無法訪問的守衛頁面。如果使用者堆疊溢出，並且進程嘗試使用堆疊下方的位址，則硬體將生成page-fault異常，因為在使用者模式下運行的程式無法訪問保護頁。實際操作系統可能會在用戶堆疊溢出時自動為用戶堆疊分配更多記憶體。當進程向 xv6 請求更多用戶記憶體時，xv6 會增加進程的堆。Xv6 首次使用

Figure 3.4: A process’s user address space, with its initial stack.


kalloc來分配物理頁。然後，它將 PTE 添加到進程的頁表中，這些頁指向新的實體頁。Xv6 在這些 PTE 中設置 thePTE\_W、PTE\_R、PTE\_U andPTE\_Vflags。大多數進程不使用整個使用者位址空間;xv6 leavesPTE\_Vclear未使用的 PTE。

我們在這裡看到一些使用頁表的很好的例子。首先，不同進程的頁表將使用者位址轉換為不同的物理記憶體頁，以便每個進程都有私有用戶記憶體。其次，每個進程都將其記憶體視為具有從零開始的連續虛擬位址，而進程的物理記憶體可以是非連續的。第三，內核在使用者位址空間 （withoutPTE\_U） 的頂部映射一個帶有 trampoline 代碼的頁面，因此單個物理記憶體頁面顯示在所有地址空間中，但只能由內核使用。

### 3.7 Code: sbrk

sbrk是系統調用進程來縮小或增加其記憶體。系統調用由函數 growproc（kernel/proc.c：260）.growproccallsuvmallocoruvmdealloc 實現，取決於是正還是負。uvmalloc（kernel/vm.c：233）使用 kalloc 分配物理記憶體，將分配的記憶體歸零，並將 PTE 添加到帶有映射頁的使用者頁面表中。uvmdealloc調用uvmunmap（kernel/vm.c：178），它使用 walk 查找 PTE，使用 kfree 釋放它們引用的物理記憶體。Xv6 使用進程的頁表不僅僅是告訴硬體如何映射使用者虛擬位址，

但也作為分配給該進程的物理記憶體頁的唯一記錄。這就是為什麼釋放用戶記憶體 （inuvmunmap） 需要檢查用戶頁面表的原因。

### 3.8 Code: exec

exec是一種系統調用，它將進程的使用者位址空間替換為從檔（稱為二進位檔或可執行檔）讀取的數據。二進位檔通常是編譯器和鏈接器的輸出，包含機器指令和程式 data.exec（kernel/exec.c：23）使用 namei（kernel/exec.c：36） 打開命名的 binarypath，這將在第 8 章中解釋。然後，它會讀取 ELF 標頭。Xv6 二進位檔的格式為廣泛使用的 ELF 格式，定義於 （kernel/elf.h）。ELF 二進位檔由一個 ELF 頭檔 struct elfhdr（kernel/elf.h：6） 和一系列程式段頭檔 struct proghdr（kernel/elf.h：25） 組成。Eachprogvhdr描述必須載入到記憶體中的應用程式部分;XV6 程式有兩個程式部分標題：一個用於指令，一個用於數據。第一步是快速檢查檔是否可能包含 ELF 二進位檔。ELF 二進位檔以四位元組的「幻數」開頭0x7F，『E』，『L』，『F』， orELF\_MAGIC（kernel/elf.h：3）。如果 ELF 標頭具有正確的幻數，則 exec 假定二進位檔格式正確。exec分配一個沒有使用者映射的新頁表 withproc\_pagetable （kernel/exec.c：49），使用 uvmalloc（kernel/exec.c：65） 為每個 ELF 段分配記憶體，並使用 loadseg（kernel/exec.c：10）.loadseguseswalkaddr將每個段載入到記憶體中，以查找分配記憶體的物理顯示，在該記憶體處寫入 ELF 段的每一頁，並讀取該檔。使用 exec 建立的第一個使用者程式 for/init 的程式部份標頭如下所示：

objdump -p user/\_init
======================

user/\_init: file format elf64-little

程式頭：0x70000003關閉 0x0000000000006bb0 vaddr 0x0000000000000000 paddr 0x0000000000000000 對齊 2\*\* 0 檔z 0x000000000000004a memsz 0x0000000000000000 標誌 r-- LOAD 關閉 0x0000000000001000 vaddr 0x0000000000000000 paddr 0x0000000000000000 對齊 2\*\* 12 檔z 0x0000000000001000 memsz 0x0000000000001000 標誌 r-x LOAD 關閉 0x0000000000002000 vaddr 0x0000000000001000 paddr 0x0000000000001000 對齊 2\*\* 12 檔z 0x0000000000000010 memsz 0x0000000000000030 標誌 rw- STACK 關閉0x0000000000000000 Vaddr 0x0000000000000000 Paddr 0x0000000000000000 align 2\*\* 4 filesz 0x0000000000000000 memsz 0x0000000000000000 flags RW-

我們看到，文本段應該在記憶體中的虛擬位址0x0處載入（沒有寫入許可權），從檔中偏移量0x1000處的內容載入。我們還看到，數據應該在位址 0x1000 處載入，該位址位於頁面邊界處，並且沒有可執行許可權。

程序節頭的 sfilesz 可能小於 thememsz，這表明它們之間的間隙應該用零填充（對於 C 全域變數），而不是從檔中讀取。對於 /init，datafilesz為 0x10 位元組，memsz為 0x30 位元組，因此 uvmallocallocate 分配了足夠的物理記憶體來容納 0x30 位元組，但僅從 file/init 中讀取 0x10 位元組。Nowexec分配並初始化用戶堆疊。它只分配一個堆疊page.exec將參數位串一次複製到堆疊頂部，將指向它們的指標記錄在ustack中。它將一個 null 指標放置在將傳遞給 main 的 argvlist 的末尾。forargc andargvare 的值通過系統調用返回路徑傳遞給main：argc是通過系統調用返回值傳遞的，即 ina0，andargvis 通過進程陷阱幀的 a1 條目傳遞。exec將無法訪問的頁面放置在堆疊頁面的正下方，因此嘗試使用多個頁面的程式將出錯。這個無法訪問的頁面還允許 sexec 處理太大的參數;在這種情況下，將參數複製到堆疊的 CopyOut（kernel/vm.c：359）函數將注意到目標頁面無法訪問，並返回 -1。在準備新的記憶體映射期間，ifexec檢測到無效的程式段等錯誤，它會跳轉到 labelbad，釋放新映像，並返回 -1.exec必須等待釋放舊映射，直到確定系統調用會成功：如果舊映射消失，則系統調用無法返回 -1 給它。唯一的錯誤情況 inexec 發生在映像創建期間。鏡像完成後，exec可以提交到新的頁表 （kernel/exec.c：125） 並釋放舊的頁表 （kernel/exec.c：129）。 exec將 ELF 檔中的位元組載入到 ELF 檔指定的位址處的記憶體中。用戶或進程可以將他們想要的任何位址放入 ELF 檔中。因此exec 有風險，因為 ELF 檔中的位址可能無意或有意地引用了內核。粗心的內核的後果可能從崩潰到惡意破壞內核的隔離機制（即安全漏洞）。Xv6 執行許多檢查來避免這些風險。例如if（ph.vaddr + ph.memsz < ph.vaddr）檢查和是否溢出 64 位整數。危險在於，使用者可能會使用aph.vaddr構造一個ELF二進位檔，該二進位檔指向使用者選擇的位址，並且 ph.memsz大到足以使總和溢出到 0x1000，這看起來像一個有效值。在舊版本的 xv6 中，使用者位址空間也包含內核（但在使用者模式下不可讀/可寫），使用者可以選擇與內核記憶體對應的地址，從而將數據從 ELF 二進位檔複製到內核中。在 xv6 的 RISC-V 版本中，這不會發生，因為內核有自己單獨的頁表;loadseg負載載入到進程的頁表中，而不是內核的頁表中。內核開發人員很容易忽略關鍵檢查，而現實世界的內核長期以來一直缺少檢查，用戶程式可以利用這些檢查的缺失來獲得內核特權。xv6 可能無法完成驗證提供給內核的用戶級數據的完整工作，惡意用戶程式可能會利用這些數據來規避 xv6 的隔離。

### 3.9 Real world

與大多數操作系統一樣，xv6 使用分頁硬體進行記憶體保護和映射。大多數操作系統通過組合分頁，使分頁的使用比 xv6 複雜得多

和 page-fault 異常，我們將在第 4 章中討論。Xv6 通過內核在虛擬位址和物理位址之間使用直接映射，並假設在位址 0x80000000 處存在物理 RAM，內核希望載入該位址，從而簡化了 Xv6。這適用於 QEMU，但在實際硬體上證明這是一個壞主意;實際硬體將 RAM 和設備放置在不可預測的物理位址上，因此（例如）0x80000000 可能沒有 RAM，而 xv6 希望能夠儲存內核。更嚴肅的內核設計利用頁表將任意硬體物理記憶體佈局轉換為可預測的內核虛擬地址佈局。RISC-V 支援物理位址級別的保護，但 xv6 不使用該功能。在具有大量記憶體的機器上，使用 RISC-V 對 “super pages” 的支援可能是有意義的。當物理記憶體較小時，小頁面是有意義的，以允許以精細粒度分配和分頁到磁碟。例如，如果一個程式只使用8 KB的記憶體，那麼給它一個完整的4 MB超級頁物理記憶體就是浪費。較大的頁面在具有大量 RAM 的機器上是有意義的，並且可以減少頁表操作的開銷。xv6 內核缺少可以為小物件提供記憶體的類似amalloc的分配器，因此阻止了內核使用需要動態分配的複雜數據結構。更精細的內核可能會分配許多不同大小的小塊，而不是（如 xv6 中）只有 4096 位元組的塊;真正的 kernel 分配器需要處理小的分配和大的分配。記憶體分配是一個永恆的熱門話題，基本問題是有效利用有限的記憶體和為未知的未來請求做準備 \[9\]。 如今，人們更關心速度而不是空間效率。

### 3.10 Exercises

1. 解析 RISC-V 的設備樹以查找電腦具有的物理內存量。
2. 編寫一個使用者程序，通過 callingsbrk（1） 將其地址空間增加一個字節。運行該程式並調查調用 tosbrk 之前和調用 tosbrk 之後的程序的頁表。內核分配了多少空間？新記憶體的 PTE 包含什麼？
3. 修改 xv6 以使用內核的 super pages。
4. exec的 Unix 實現傳統上包括對 shell 腳本的特殊處理。如果要執行的檔以文本 #！ 開頭，則第一行被視為要運行以解釋檔的程式。例如，如果調用exec來運行 myprog arg1andmyprog 的第一行是#！/interp，則 execruns/interp與命令行/interp myprog arg1 一起使用。在 xv6 中實現對此約定的支援。
5. 為內核實現位址空間佈局隨機化。

第 4 章
=====

陷阱和系統調用
=======

有三種類型的事件會導致 CPU 擱置指令的正常執行，並強制將控制權轉移到處理該事件的特殊代碼。一種情況是系統調用，當使用者程序執行 theecall指令要求內核為其做一些事情時。另一種情況是異常：指令（使用者或內核）執行非法操作，例如除以零或使用無效的虛擬位址。第三種情況是 deviceinterrupt，當設備發出需要注意的信號時，例如，當磁碟硬體完成讀取或寫入請求時。

本書使用 strap作為這些情況的通用術語。通常，在 trap 發生時正在執行的任何代碼稍後都需要恢復，並且不需要知道發生了任何特殊情況。也就是說，我們通常希望陷阱是透明的;這對於設備中斷尤其重要，因為被中斷的代碼通常不希望出現這種情況。通常的順序是 trap 強制將控制權轉移到 kernel 中;內核保存 registers 和其他 state，以便可以恢復執行;內核執行適當的處理程式代碼（例如，系統調用實現或設備驅動程式）;內核恢復已保存的狀態並從 trap 返回;原始代碼將從中斷處恢復。

Xv6 處理內核中的所有陷阱;陷阱不會傳遞給用戶代碼。在內核中處理陷阱對於系統調用來說是很自然的。它對中斷是有意義的，因為隔離要求只允許內核使用設備，並且因為內核是一種方便的機制，可以在多個進程之間共享設備。它對異常也很有意義，因為 xv6 通過終止有問題的程式來回應來自用戶空間的所有異常。

Xv6 陷阱處理分四個階段進行：RISC-V CPU 執行的硬體操作、為內核 C 代碼準備的一些彙編指令、決定如何處理陷阱的 C 函數，以及系統調用或設備驅動程式服務例程。雖然這三種陷阱類型的共性表明內核可以使用單個代碼路徑處理所有陷阱，但事實證明，為兩種不同的情況使用單獨的代碼很方便：來自用戶空間的陷阱和來自內核空間的陷阱。處理 trap 的內核代碼（彙編程式或 C）通常稱為 ahandler;第一個處理程式指令通常是用彙編程式（而不是 C）編寫的，有時稱為向量。

### 4.1 RISC-V trap machinery

每個 RISC-V CPU 都有一組控制寄存器，內核寫入這些寄存器以告訴 CPU 如何處理陷阱，內核可以讀取這些寄存器以找出已發生的陷阱。RISC-V 文檔包含完整的故事 \[3\].riscv.h（kernel/riscv.h：1）包含 xv6 使用的定義。以下是最重要的寄存器的概述：

*   stvec：內核在此處寫入其 trap 處理程序的位址;RISC-V 跳轉到位址 instvec 來處理陷阱。
*   sepc：當陷阱發生時，RISC-V 會在此處保存程式計數器（因為 thepcis 隨後會用值 instvec 覆蓋）。Thesret（return from trap） 指令將 sepc 複製到 thepc。內核可以 writesepc來控制 wheresretgoes。
*   scause：RISC-V 在此處放置一個數位，用於描述陷阱的原因。
*   sscratch：陷阱處理程式碼使用 sscratch 來説明它避免在保存使用者寄存器之前覆蓋使用者寄存器。
*   sstatus：SIE 位 insstatus 控制是否啟用設備中斷。如果內核清除了 SIE，則 RISC-V 將推遲設備中斷，直到內核設置 SIE。SPP 位指示陷阱是來自使用者模式還是管理者模式，並控制modesret返回的內容。

上述 registers 與在 supervisor 模式下處理的 traps 有關，它們不能在 user 模式下讀取或寫入。多核晶元上的每個 CPU 都有自己的一組 registers，並且在任何給定時間都可能有多個 CPU 正在處理 trap。當需要強制執行陷阱時，RISC-V 硬體會對所有陷阱類型執行以下操作：

1. 如果陷阱是設備中斷，並且 thesstatusSIE 位是明確的，請不要執行以下任何操作。
2. 通過清除 SIE bit insstatus 來禁用中斷。
3. Copy thepctosepc.
4. 將當前模式 （user 或 supervisor） 保存在 SPP bit insstatus 中。
5. Setscauseto reflect the trap’s cause.
6. Set the mode to supervisor.
7. Copystvecto thepc.
8. Start executing at the newpc.

請注意， CPU 不會切換到 kernel 頁表，不會切換到 kernel 中的 stack，也不會保存除 pc.內核軟體必須執行這些任務。CPU 在 trap 期間執行最少工作的一個原因是為軟體提供靈活性;例如，某些操作系統在某些情況下省略了頁表開關，以提高陷阱性能。值得考慮是否可以省略上面列出的任何步驟，也許是為了尋找更快的陷阱。儘管在某些情況下，更簡單的序列可以工作，但通常省略許多步驟是危險的。例如，假設 CPU 沒有切換程式計數器。然後，來自用戶空間的陷阱可以切換到 Supervisor 模式，同時仍運行使用者指令。這些使用者指令可能會破壞使用者/內核隔離，例如，通過修改 thesatpregister 以指向允許訪問所有物理記憶體的頁表。因此，CPU 切換到內核指定的指令位址 lystvec 非常重要。

### 4.2 來自用戶空間的陷阱

Xv6 對 trap 的處理方式不同，具體取決於 trap 是在內核中執行時還是在用戶代碼中執行時發生。這是用戶代碼中陷阱的故事;Section 4.5 描述了內核代碼中的 traps。如果使用者程式進行系統調用（ecall 指令）或執行非法操作，或者設備中斷，則在使用者空間中執行時可能會發生陷阱。來自用戶空間的 trap 的高級路徑是 uservec（kernel/trampoline.S：22），然後usertrap（kernel/trap.c：37）;當重新轉彎時，usertrapret（kernel/trap.c：90）然後 userret（kernel/trampoline.S：101）。xv6 的陷阱處理設計的一個主要限制是 RISC-V 硬體在強制陷阱時不會切換頁表。這意味著 stvec 中的 trap 處理程式地址必須在 user page table 中具有有效的映射，因為當 trap 處理代碼開始執行時，該頁表是有效的。此外，xv6 的 trap 處理代碼需要切換到內核頁表;為了能夠在該切換後繼續執行，內核頁表還必須具有指向 BystVec 的處理程式的映射。Xv6 使用 atrampolinepage 滿足這些要求。蹦床頁面包含 suservec，這是 stvec 指向的 xv6 陷阱處理代碼。trampoline 頁映射到每個進程的頁表中的 addressTRAMPOLINE，它位於虛擬位址空間的頂部，因此它將位於程式自身使用的記憶體之上。trampoline 頁也映射到內核頁表中的位址 TRAMPOLINE。參見圖 2.3 和圖 3.3。由於 trampoline 頁面映射在用戶頁面表中，因此 trap 可以在 supervisor 模式下開始執行。 由於 trampoline 頁映射到內核地址空間中的相同位址，因此 trap 處理程式在切換到內核頁表后可以繼續執行。uservectrap 處理程式的代碼是 intrampoline。S（內核/蹦床。S：22）。當uservecstarts時，所有32個registers都包含被中斷的用戶代碼擁有的值。這32個值需要保存在記憶體中的某個位置，以便稍後內核可以在返回用戶空間之前恢復它們。存儲到記憶體需要使用 register 來保存位址，但此時沒有通用的 registers！幸運的是，RISC-V 以 thesscratchregister 的形式提供了説明。uservecsavesa0in 開頭的 csrw指令

劃痕。nowuservec有一個寄存器 （a0） 可供使用。

UserVec 的下一個任務是保存 32 個使用者寄存器。內核為每個進程分配一頁記憶體給 atrapframestructure，該結構（除其他外）有空間保存 32 個使用者寄存器 （kernel/proc.h：43）。由於 satp仍然引用了用戶頁表，因此 uservec 需要在使用者位址空間中映射 trapframe。Xv6 將每個進程的陷阱幀映射到該進程的用戶頁表中的虛擬 addressTRAPFRAME;TRAPFRAME位於 TRAMPOLINE 的正下方。process『sp->trapframe 也指向 trapframe，儘管位於其物理位址，以便內核可以通過內核頁表使用它。

因此 uservec 將 addressTRAPFRAME載入 a0 中，並將所有使用者寄存器保存到其中，包括使用者的 sa0，從 scratch 讀回。

trapframe 包含當前進程的內核棧位址、當前 CPU 的 hartid、usertrap函數的位址和內核頁的位址 table.uservec 檢索這些值，切換到內核頁表，並跳轉到 usertrap。

usertrap 的工作是確定陷阱的原因，處理它，然後返回（kernel/- trap.c：37）。它首先更改 stvec，以便內核中的 trap 將由 kernelvec 而不是 uservec 處理。它會保存這些 pcregister （保存的使用者程式計數器），因為 usertrap 可能會調用 yield來切換到另一個進程的內核線程，並且該進程可能會返回到用戶空間，在此過程中它將修改 sepc。如果 trap 是系統調用，則 usertrapcallssyscall來處理它;如果設備中斷，devintr;否則，它是一個例外，內核會殺死出錯的進程。系統調用路徑將 4 添加到保存的使用者程式計數器中，因為 RISC-V 在系統調用的情況下，使程式指標指向 theecallinstruction，但用戶代碼需要在後續指令處恢復執行。在出去時，usertrap 檢查進程是否已被殺死或應該讓出 CPU（如果此陷阱是定時器中斷）。

返回用戶空間的第一步是調用usertrapret（kernel/trap.c：90）。此函數設置 RISC-V 控制寄存器，為將來的使用者空間陷阱做準備：設置 stvectouservec並準備 uservec 依賴的陷阱幀字段。usertrapret 將 sepc設置為以前保存的使用者程式計數器。最後，usertrapret調用userret 在 user 和 kernel 頁表中映射的 trampoline 頁上;原因是 as- sembly code inuserret會切換頁表。

UserTrapret 對 UserRet 的調用傳遞一個指向進程的用戶頁表 ina0 （kernel/trampoline.S：101）.userretswitchessatp添加到進程的用戶頁面表中。回想一下，用戶頁面表同時映射了 trampoline 頁面和 TRAPFRAME，但內核中沒有其他任何內容。在user和 kernel 頁表中的同一虛擬位址處的 trampoline 頁面映射允許userretto在 changingsatp 後繼續執行。從這時起，datauserret 唯一能用的就是寄存器內容和 trapframe.userret 的內容將 TRAPFRAME 位址載入 a0 中，通過 a0 從 trapframe 中恢復保存的使用者寄存器，恢復保存的使用者 a0，並執行 ssret 傳回用戶空間。

### 4.3 Code: Calling system calls

第 2 章以 initcode 結束。調用 execsystem 調用（user/initcode.S：11）。讓我們看看 user 調用是如何進入內核中 execsystem 調用的實現的。init代碼。替換 execin registersa0anda1 的參數，並放置系統調用號 ina7。系統調用編號與 syscallsarray 中的條目匹配，該陣列是函數指標表 （kernel/syscall.c：107）。theecall指令捕獲到內核中，並導致 uservec、usertrap 和 thensyscall執行，如上所示。syscall（kernel/syscall.c：132）從 trapframe 中的 saveda7 中檢索系統調用號，並使用它為 syscalls 編製索引。對於第一次系統調用，a7包含 SYS\_exec（ker- nel/syscall.h：8），從而導致對系統調用實現functionsys\_exec調用。Whensys\_execreturns，syscall記錄其返回值 inp->trapframe->a0。這將導致原始用戶空間調用 toexec（） 傳回該值，因為 RISC-V 上的 C 調用約定返回值 ina0。系統調用通常返回負數來表示錯誤，返回零或正數表示成功。如果系統調用號無效，則 syscall 將列印錯誤並返回− 1。

### 4.4 代碼：系統調用參數

內核中的系統調用實現需要找到用戶代碼傳遞的參數。因為用戶代碼調用系統調用包裝函數，所以參數最初位於 RISC-V C 調用約定將它們放置的位置：在寄存器中。內核陷阱代碼將使用者寄存器保存到當前進程的陷阱幀中，內核代碼可以在其中找到它們。然後，內核函數argint、argaddr和argfd從陷阱幀中檢索第個系統調用參數，作為整數、指標或檔描述符。它們都調用argraw來檢索適當的已保存使用者寄存器 （kernel/syscall.c：34）。某些系統調用將指標作為參數傳遞，內核必須使用這些指標來讀取或寫入用戶記憶體。例如，execsystem 調用向內核傳遞一個指標陣列，該陣列引用用戶空間中的字串參數。這些指標帶來了兩個挑戰。首先，用戶程式可能是有缺陷的或惡意的，並且可能會向內核傳遞一個無效的指標或一個旨在誘騙內核訪問內核記憶體而不是用戶記憶體的指標。其次，xv6 內核頁表映射與用戶頁表映射不同，因此內核不能使用普通指令從使用者提供的位址載入或存儲。內核實現安全地將數據傳輸到使用者提供的位址或從使用者提供的位址傳輸數據的函數。fetchstr 為例 （kernel/syscall.c：25）。文件系統調用（如 execusefetchstr）從使用者 space.fetchstrcallscopyinstr 檢索字串檔名參數來完成艱苦的工作。copyinstr（kernel/vm.c：415）從用戶頁 tablepagetable 中的虛擬位址srcva複製最多最大位元元組數 todst。由於 pagetable 不是當前頁表，copyinstr 使用 walkaddr（調用 walk）查找 srcvainpagetable，得到物理位址 pa0。 內核的頁表將所有物理 RAM 映射到等於 RAM 物理位址的虛擬位址。這允許 copyinstr 直接從 pa0todst 複製字串位元組。walkaddr（kernel/vm.c：109）檢查使用者提供的虛擬位址是否是進程的

用戶位址空間，因此程式無法欺騙內核讀取其他記憶體。類似的函數 copyout 將數據從內核複製到使用者提供的位址。

### 4.5 來自內核空間的陷阱

Xv6 處理內核代碼陷阱的方式與處理用戶代碼陷阱的方式不同。進入內核時，usertrappointsstvec 到彙編代碼 atkernelvec（kernel/kernelvec.S：12）。由於 kernelvec 僅在 xv6 已在內核中時執行，kernelvec 可以依賴於設置為內核頁表的 satp，以及引用有效內核堆疊的堆棧指標。kernelvec將所有 32 個寄存器推送到堆疊上，稍後將從堆疊中恢復它們，以便中斷的內核代碼可以不受干擾地恢復。kernelvec將寄存器保存在中斷的內核線程的堆棧上，這是有道理的，因為寄存器值屬於該線程。如果 trap 導致切換到不同的線程，這一點尤其重要——在這種情況下，trap 實際上會從新線程的堆棧返回，將被中斷的線程保存的 registers 安全地留在其堆棧上。kernelVec跳到 kerneltrap（kernel/trap.c：135）保存寄存器后.kerneltrap 準備了兩種類型的陷阱：設備中斷和異常。它調用 devintr（kernel/- trap.c：185） 來檢查和處理前者。如果 trap 不是設備中斷，則它一定是異常，如果它發生在 xv6 內核中，則始終是致命錯誤;內核調用 panic 並停止執行。如果內核陷阱是由於計時器中斷而被調用的，並且進程的內核線程正在運行（而不是調度程序線程），則 kerneltrap 會調用 yield，以便為其他線程提供運行的機會。在某個時候，其中一個線程將生成，並讓我們的線程和itskerneltrap再次恢復。第 7 章解釋了 inyield 會發生什麼。當 kerneltrap 的工作完成後，它需要返回到被 trap 中斷的任何代碼。 因為 ayield 可能干擾了 sepc，並且之前的模式處於 in狀態，所以 kerneltrap 會在啟動時保存它們。現在，它會恢復這些控制寄存器並返回給 kernelvec（kernel/kernelvec.S：38）.kernelvec 從堆棧中彈出保存的寄存器，並執行 ecutessret，後者複製 sepctopc並恢復中斷的內核代碼。如果 kerneltrapcalledyield由於計時器中斷，則值得考慮一下陷阱返回是如何發生的。Xv6 設置一個 CPU 的 sstvectokernelvec當該 CPU 從使用者空間進入內核時;你可以看到這個 inUsertrap（kernel/trap.c：29）。內核開始執行 butstvecis 仍然設置為 uservec 的時間視窗，在該視窗期間不發生設備中斷至關重要。幸運的是，RISC-V 在開始接受 trap 時總是禁用中斷，而 usertrap 直到 setsstvec 之後才會再次啟用它們。

### 4.6 頁面錯誤異常

Xv6 對異常的回應相當無聊：如果用戶空間發生異常，內核會殺死出錯的進程。如果內核中發生異常，內核將 panic。真實操作

系統通常以更有趣的方式進行回應。

例如，許多內核使用頁面錯誤來實現寫入時複製 （COW） fork。為了解釋寫時複製分叉，請考慮第 3 章中描述的 xv6 的分叉，fork導致子級的初始記憶體內容與分叉時父級的初始記憶體內容相同。Xv6 實現了 fork withuvmcopy（kernel/vm.c：313），它為子節點分配物理記憶體，並將父節點的記憶體複製到其中。如果子級和父級可以共用父級的物理記憶體，則效率會更高。但是，直接實現此方案是行不通的，因為它會導致父級和子級通過對共用堆疊和堆的寫入來中斷彼此的執行。

父級和子級可以通過適當使用頁表許可權和頁錯誤來安全地共用物理記憶體。當使用的虛擬位址在頁表中沒有映射，或者具有清除的映射whosePTE\_Vflag，或者其許可權位 （PTE\_R，PTE\_W，PTE\_X，PTE\_U） 禁止嘗試操作的映射時，CPU 會引發 apage-fault 異常。RISC-V 區分了三種頁面錯誤：載入頁面錯誤（由載入指令引起）、存儲頁錯誤（由存儲指令引起）和指令頁錯誤（由要執行的指令的獲取引起）。thescauseregister 指示頁面錯誤的類型，thestvalregister 包含無法轉換的位址。

COW fork 的基本計劃是父級和子級最初共用所有物理頁面，但每個父級和子級都將它們映射為只讀（thePTE\_Wflag清除）。父級和子級可以從共用的物理記憶體中讀取。如果其中任何一個寫入給定的頁面，RISC-V CPU 將引發 page-fault 異常。內核的 trap 處理程式通過分配一個新的物理記憶體頁並將出錯的位址映射到的物理頁複製到其中來回應。內核將出錯進程的頁表中的相關 PTE 更改為指向副本並允許寫入和讀取，然後在導致錯誤的指令處恢復出錯進程。由於 PTE 現在允許寫入，因此重新執行的指令將執行而不會出錯。寫入時複製需要簿記來幫助確定何時可以釋放物理頁面，因為每個頁面都可以由不同數量的頁表引用，具體取決於 fork、頁面錯誤、exec 和退出的歷史記錄。這種簿記允許進行重要的優化：如果一個進程發生存儲頁錯誤，並且物理頁僅從該進程的頁表中引用，則不需要副本。

Copy-on-write 使 fork 更快，因為 fork 不需要複製記憶體。一些記憶體在寫入時必須稍後複製，但通常情況下，大多數記憶體永遠不必複製。一個常見的例子是 forkfollowed byexec：在 fork 之後可能會寫入一些頁面，但隨後 child'sexec 會釋放從父級繼承的大部分記憶體。Copy-on-writefork 消除了複製此記憶體的需要。此外，COW 分叉是透明的：無需對應用程式進行修改即可從中受益。

頁表和頁錯誤的組合除了 COW 分叉之外，還開闢了一系列有趣的可能性。另一個廣泛使用的功能稱為 lazy allocation，它包含兩個部分。首先，當應用程式通過 callingsbrk 請求更多記憶體時，內核會注意到大小增加，但不會分配物理記憶體，也不會為新的虛擬位址範圍創建 PTE。其次，在其中一個新位址的page fault上，內核分配一頁物理記憶體並將其映射到page table。與 COW fork 一樣，內核可以對應用程式透明地實現延遲分配。

由於應用程式經常請求比它們需要的更多的記憶體，因此延遲分配是一個好處：內核根本不需要為應用程式從未使用的頁面做任何工作。此外，如果應用程式要求將位址空間大幅增加，那麼沒有惰性分配的 sbrks 成本很高：如果應用程式需要 1 GB 的記憶體，則內核必須分配 262,144 個 4096 位元組的頁面並將其歸零。延遲分配允許此成本隨時間分攤。另一方面，惰性分配會產生頁面錯誤的額外開銷，這涉及使用者/內核轉換。操作系統可以通過為每個頁面錯誤分配一批連續頁面而不是一個頁面，並通過專門為此類頁面錯誤分配內核進入/退出代碼來降低此成本。

另一個廣泛使用的利用頁面錯誤的特性是需求分頁。Inexec xv6 在啟動應用程式之前將應用程式的所有文本和數據載入到記憶體中。由於應用程式可能很大，並且從磁碟讀取需要時間，因此這種啟動成本對用戶來說可能是顯而易見的。為了減少啟動時間，現代內核最初不會將可執行檔載入記憶體中，而只是創建所有 PTE 都標記為無效的用戶頁表。內核啟動程序運行;每次程式第一次使用頁面時，都會發生頁面錯誤，作為回應，內核會從磁碟讀取頁面的內容並將其映射到使用者位址空間。與 COW fork 和 lazy allocation 一樣，內核可以對應用程式透明地實現此功能。

計算機上運行的程式需要的記憶體可能比計算機的 RAM 多。為了順利應對，操作系統可以實現對磁碟的分頁。這個想法是將一小部分用戶頁面存儲在 RAM 中，其餘部分存儲在磁碟的分頁區域中。內核將與存儲在分頁區域（因此不在 RAM）中的記憶體相對應的 PTE 標記為無效。如果應用程式嘗試使用已分頁到磁碟的頁面之一，則應用程式將產生頁面錯誤，並且該頁面必須分頁：內核陷阱處理程式將分配一頁物理 RAM，將頁面從磁碟讀取到 RAM，並修改相關的 PTE 以指向 RAM。

如果需要對頁面進行分頁，但沒有可用的物理 RAM，會發生什麼情況？在這種情況下，內核必須首先釋放物理頁，方法是將其分頁到磁碟上的分頁區域，並將引用該物理頁的 PTE 標記為無效。驅逐成本高昂，因此如果分頁不頻繁，則分頁性能最佳：如果應用程式僅使用其記憶體頁的子集，並且子集的並集適合 RAM。此屬性通常稱為具有良好的引用位置。與許多虛擬記憶體技術一樣，內核通常以對應用程式透明的方式實現對磁碟的分頁。

計算機通常使用少量或沒有自由物理記憶體運行，無論硬體提供多少 RAM。例如，雲供應商在單個馬上多路複用多個客戶，以經濟高效地使用其硬體。再舉一個例子，使用者在智慧手機上運行許多應用程式，佔用少量物理記憶體。在此類設置中，分配頁面可能需要先逐出現有頁面。因此，當可用物理記憶體稀缺時，分配成本很高。

當可用記憶體稀缺且程式只主動使用其已分配記憶體的一小部分時，延遲分配和需求分頁特別有利。這些技術還可以避免在分配或載入頁面時浪費的工作，但在使用頁面之前從未使用或逐出。

將分頁和頁面錯誤異常組合在一起的其他功能包括自動擴展堆疊和記憶體映射檔，這些檔是程式使用 themmapsystem 調用映射到其位址空間的檔，以便程式可以使用 load 和 store 讀取和寫入它們

指示。

### 4.7 Real world

蹦床和陷阱架可能看起來過於複雜。驅動力是 RISC-V 在強制疏水閥時有意地盡可能少地工作，以允許非常快速的疏水閥處理，這被證明是很重要的。因此，kernel trap 處理程式的前幾條指令必須在用戶環境中有效地執行：用戶頁表和用戶註冊內容。陷阱處理程式最初不知道有用的事實，例如正在運行的進程的身份或內核頁表的位址。解決方案是可能的，因為 RISC-V 提供了受保護的位置，內核可以在進入用戶空間之前隱藏資訊：thesscratchregister 和指向內核記憶體但受到缺乏 ofPTE\_U保護的用戶頁表條目。Xv6 的 trampoline 和 trapframe 利用了這些 RISC-V 功能。

如果將內核記憶體映射到每個進程的用戶頁表 （withPTE\_Uclear） 中，則可以消除對特殊 trampoline 頁的需求。這也將消除從用戶空間捕獲到內核時對頁表切換的需要。這反過來又允許 kernel 中的 system call implementations 利用當前進程的使用者記憶體被映射，從而允許 kernel 代碼直接取消引用用戶指標。許多操作系統都使用這些想法來提高效率。Xv6 避免使用它們是為了減少由於無意中使用用戶指標而導致內核中出現安全錯誤的機會，並降低確保使用者和內核虛擬位址不重疊所需的一些複雜性。生產操作系統實現寫入時複製分叉、延遲分配、需求分頁、分頁到磁碟、記憶體映射檔等。此外，生產操作系統嘗試在物理記憶體的所有區域中存儲有用的內容，通常將檔內容緩存在進程未使用的記憶體中。生產操作系統還為應用程式提供系統調用，以管理其位址空間並通過 themmap、munmap 和 sigactionsystem 調用實現自己的頁面錯誤處理，以及提供將記憶體固定到 RAM 中的調用（seemlock）和建議內核應用程式計劃如何使用其記憶體（seemadvise）。

### 4.8 Exercises

1. 函數 copyinandcopyinstrwalk 軟體中的用戶頁表。設置內核頁表，以便內核映射使用者程序，並且 copyin 和 copyinstr可以使用 memcpy 將系統調用參數複製到內核空間，依靠硬體進行頁表遍歷。
2. 實現延遲記憶體分配。
3. 實施 COW fork。
4. 有沒有辦法消除每個使用者位址空間中的specialTRAPFRAMEpage映射？例如，是否可以修改 coduservec 以簡單地將 32 個使用者寄存器推送到內核堆疊上，或將它們存儲在 procstructure 中？
5. 可以修改 xv6 以消除 specialTRAMPOLINEpage 映射嗎？
6. Implementmmap.

第 5 章
=====

中斷和設備驅動程式
=========

Adriver是作業系統中管理特定設備的代碼：它配置設備硬體，告訴設備執行操作，處理生成的中斷，並與可能正在等待設備 I/O 的進程交互。驅動程式代碼可能很棘手，因為驅動程式與它管理的設備同時執行。此外，驅動程式必須了解設備的硬體介面，該介面可能很複雜且記錄不佳。需要操作系統注意的設備通常可以配置為生成中斷，這是 trap 的一種類型。內核陷阱處理代碼可識別設備何時引發中斷並調用驅動程式的中斷處理程式;在 XV6 中，此 dispatch 發生在 devintr（kernel/trap.c：185） 中。許多設備驅動程式在兩個上下文中執行代碼：在進程的內核線程中運行的上半部分，以及在中斷時執行的下半部分。上半部分通過系統調用（如 readandwrite）調用，這些調用希望設備執行 I/O。此代碼可能會要求硬體啟動操作（例如，要求磁碟讀取塊）;然後，代碼等待操作完成。最終，設備完成操作並引發中斷。驅動程式的中斷處理程式充當下半部分，找出已完成的操作，在適當的情況下喚醒等待進程，並告知硬體開始處理任何等待的下一個操作。

### 5.1 Code: Console input

控制台驅動程式 （kernel/console.c） 是驅動程式結構的簡單說明。控制台驅動程式接受人類通過連接到 RISC-V 的 UART 串行埠硬體鍵入的字元。控制台驅動程式一次累積一行輸入，處理特殊輸入字元，例如backspace和control-u。用戶進程（如 shell）使用 thereadsystem 調用從主控台獲取輸入行。當您在 QEMU 中鍵入 input to xv6 時，您的擊鍵將通過 QEMU 的類比 UART 硬體傳送到 xv6。驅動程式與之通信的 UART 硬體是由 QEMU 類比的 16550 晶片 \[13\]。在真實電腦上，16550 將管理連接到終端或其他計算機的 RS232 串行鏈路。運行 QEMU 時，它連接到您的鍵盤和顯示器。UART 硬體在軟體中顯示為一組 memory-mappedcontrol registers。那

是，RISC-V 硬體連接到一些物理位址到 UART 設備，因此載入和儲存與設備硬體而不是 RAM 交互。UART 的記憶體映射廣告從 0x10000000 開始，即 UART0（kernel/memlayout.h：21）。有一些 UART 控制寄存器，每個寄存器的寬度為一個字節。它們從 UART0 的偏移量在 （kernel/uart.c：22） 中定義。例如，LSRregister 包含指示輸入字元是否正在等待軟體讀取的位。這些字元（如果有）可從 RHRregister 中讀取。每次讀取一個字元時， UART 硬體都會將其從等待字元的內部 FIFO 中刪除，並在 FIFO 為空時清除 LSR 中的 “ready” 位。UART 傳輸硬體在很大程度上獨立於接收硬體;如果軟體向 THR 寫入位元組，則 UART 傳輸該位元組。Xv6 的maincallsconsoleinit（kernel/console.c：182）來初始化 UART 硬件。此代碼將 UART 配置為在 UART 接收到每個位元組的輸入時生成一個接收中斷，並在 UART 每次完成發送一個字節的輸出時發送 completeinterrupt （kernel/uart.c：53）。xv6 shell 通過 init.c（user/init.c：19） 打開的檔描述符從控制台讀取數據。對 thereadsystem 調用的調用通過內核 toconsoleread（kernel/con- sole.c：80）.consolereads 等待輸入到達（通過中斷）並被緩衝 incons.buf，將輸入複製到用戶空間，並（在整行到達后）返回用戶進程。如果使用者還沒有輸入完整的行，任何讀取進程都將在 thesleepcall（kernel/con- sole.c：96）（第 7 章解釋了 sleep 的細節）。 當使用者鍵入字元時，UART 硬體會要求 RISC-V 引發中斷，從而啟動 xv6 的陷阱處理程式。陷阱處理程式調用 devintr（kernel/trap.c：185），它查看 RISC-Vscauseregister 以發現中斷來自外部設備。然後它要求一個名為 PLIC \[3\] 的硬體單元告訴它哪個設備被中斷了 （kernel/trap.c：193）。如果是 UART，devintrcallsuartintr.uartintr（kernel/uart.c：177）從 UART 硬體中讀取任何等待的輸入字元，並將它們交給 consoleintr（kernel/console.c：136）;它不會等待 個字元，因為未來的input將引發新的中斷。consoleintris 的工作是在 cons.buf 中累積輸入字元，直到一整行到達。consoleintr 特別處理退格和其他一些字元。當換行符到達時，consoleintr 喚醒一個等待的 consoleread（如果有的話）。一旦被喚醒，consoleread將觀察到一行完整的 incons.buf，將其複製到用戶空間，然後返回（通過系統調用機制）到用戶空間。

### 5.2 代碼：主控台輸出

對連接到主控台的檔描述符的 Awritesystem 調用最終到達 atuartputc （kernel/uart.c：87）。設備驅動程式維護一個輸出緩衝區 （uart\_tx\_buf） ，以便寫入進程不必等待 UART 完成發送;相反，uartputc將每個字元附加到緩衝區，調用 uartstart以啟動設備傳輸（如果尚未傳輸），然後返回。uartputcwaits 的唯一情況是緩衝區已滿。每次 UART 完成發送一個字節時，它都會生成一個 interrupt.uartintrcallsuartstart，

該命令檢查設備是否確實已完成發送，並將下一個緩衝的輸出字元交給設備。因此，如果一個進程向控制台寫入多個字節，通常第一個字節將由 uartputc 的調用 touartstart 發送，其餘緩衝的位元組將由 uartstartcalls 從 uartintras 發送完整中斷到達。需要注意的一般模式是通過緩衝和中斷將設備活動與進程活動解耦。控制台驅動程式可以處理輸入，即使沒有進程等待讀取輸入;後續讀取將看到 Input。同樣，進程可以發送輸出，而不必等待設備。這種解耦可以通過允許進程與設備 I/O 同時執行來提高性能，當設備速度較慢（如 UART）或需要立即關注（如回顯鍵入字元）時尤其重要。這個想法有時稱為 I/O 併發。

### 5.3 驅動程式中的併發

您可能已經注意到對 acquireinconsoleread 和 inconsoleintr 的調用。這些調用獲取一個鎖，該鎖可保護控制台驅動程序的數據結構免受併發訪問。這裡有三個併發危險：不同 CPU 上的兩個進程可能會同時調用 consoleread;硬體可能會要求 CPU 提供控制台（實際上是 UART）中斷，而該 CPU 已經在執行 insideconsoleread;並且硬體可能會在執行 consoleread時在不同的 CPU 上提供控制台中斷。第 6 章解釋了如何使用鎖來確保這些危險不會導致不正確的結果。在驅動程式中需要注意併發的另一種方式是，一個進程可能正在等待來自設備的輸入，但當其他進程（或根本沒有進程）正在運行時，輸入的中斷信號可能會到達。因此，不允許中斷處理程式考慮它們已中斷的進程或代碼。例如，中斷處理程式無法安全地使用當前進程的頁表調用 copyout。中斷處理程式通常執行相對較少的工作（例如，只需將 input 數據複製到緩衝區），並喚醒上半部分代碼以完成其餘工作。

### 5.4 Timer interrupts

Xv6 使用計時器中斷來維護其當前時間的概念，並在計算密集型進程之間切換。定時器中斷來自連接到每個 RISC-V CPU 的 clock 硬體。Xv6 對每個 CPU 的時鐘硬體進行程式設計，以定期中斷 CPU。代碼 instart.c（kernel/start.c：53） 設置了一些控制位，允許對定時器控制寄存器進行監控模式訪問，然後請求第一個定時器中斷。timecontrol 寄存器包含硬體以穩定速率遞增的計數;這用作當前時間的概念。Thestimecmpregister 包含 CPU 將引發計時器中斷的時間;settingstimecmp設置為 timeplusx 的當前值將安排一個 interruptxtime units 在將來。Forqemu 的 RISC-V 模擬，1000000 個時間單位大約是十分之一秒。計時器中斷通過usertraporkerneltrapanddevintr到達，就像其他設備輸入一樣。計時器中斷到達時，scause 的低位設置為 5;devintrintrap.c檢測

這種情況並調用 ClockIntr（kernel/trap.c：164）。后一個函數 increments，降低內核以跟蹤時間的流逝。增量只發生在一個 CPU 上，以避免在有多個 CPU 時時間流逝得更快。clockintr喚醒在 sleepsystem 調用中等待的任何進程，並通過編寫 stimecmp 來安排下一個計時器中斷。

devintr返回 2 來表示計時器中斷，以指示 kerneltraporusertrap 它們應該調用 yield，以便 CPU 可以在可運行的進程之間進行多路複用。

內核代碼可以被定時器中斷中斷，通過 yield 強制進行上下文切換，這是早期代碼 inusertrapis 在啟用中斷之前小心保存 assepc 等狀態的部分原因。這些上下文切換還意味著，在編寫內核代碼時，必須知道它可能會在沒有警告的情況下從一個 CPU 放在另一個 CPU。

### 5.5 Real world

與許多操作系統一樣，Xv6 在內核中執行時允許中斷甚至上下文切換 （viayield）。這樣做的原因是，在長時間運行的複雜系統調用中保持快速響應時間。但是，如上所述，允許在內核中中斷是一些複雜性的來源;因此，一些操作系統僅在執行用戶代碼時允許中斷。在典型計算機上全面支援所有設備是一項艱巨的工作，因為設備眾多，設備具有許多功能，並且設備和驅動程式之間的協定可能很複雜且文檔記錄不佳。在許多操作系統中，驅動程式佔用的代碼比核心內核多。

UART 驅動程式通過讀取 UART 控制寄存器，一次檢索一個字節的數據;這種模式稱為程式設計 I/O，因為軟體正在驅動數據移動。程式設計 I/O 很簡單，但速度太慢，無法在高數據速率下使用。需要高速移動大量數據的設備通常使用直接記憶體訪問 （DMA）。DMA 設備硬體直接將傳入數據寫入 RAM，並從 RAM 讀取傳出數據。現代磁碟和網路設備使用 DMA。DMA 器件的驅動程式將在 RAM 中準備數據，然後對控制寄存器進行一次寫入，告訴器件處理準備好的數據。

當設備在不可預測的時間需要關注時，中斷是有意義的，而且不會太頻繁。但是中斷的CPU開銷很高。因此，高速設備（如網路和磁碟控制器）使用減少中斷需求的技巧。一個技巧是為整批傳入或傳出請求引發單個中斷。另一個技巧是讓驅動程式完全禁用中斷，並定期檢查設備以查看是否需要注意。這種技術稱為輪詢。如果設備以高速率執行操作，則輪詢是有意義的，但如果設備大部分時間處於空閒狀態，則會浪費 CPU 時間。某些驅動程式根據當前設備負載在輪詢和中斷之間動態切換。

UART 驅動程式首先將傳入數據複製到內核中的緩衝區，然後複製到用戶空間。這在低數據速率下是有意義的，但這樣的雙重複製會顯著降低快速生成或使用數據的設備的性能。某些作業系統能夠直接在用戶空間緩衝區和設備硬體之間行動數據，通常使用 DMA。

如第 1 章所述，控制台對應用程式顯示為常規檔，應用程式使用 thereadandwritesystem 調用讀取輸入和寫入輸出。應用程式可能希望控制設備中無法通過標準檔案系統調用表示的方面（例如，在控制台驅動程式中啟用/禁用行緩衝）。Unix 作業系統支援在此類情況下調用ioctl系統。計算機的某些用法要求系統必須在限定時間內回應。例如，在安全關鍵系統中，錯過最後期限可能會導致災難。Xv6 不適合硬實時設置。硬即時操作系統往往是與應用程式連結的庫，其方式允許分析以確定最壞情況的回應時間。Xv6 也不適合軟即時應用程式，偶爾錯過截止日期是可以接受的，因為 xv6 的調度器過於簡單，並且它具有內核代碼路徑，中斷會長時間禁用。

### 5.6 Exercises

1. Modifyuart.c完全不使用中斷。您可能還需要修改 console.cas。
2. 為乙太網卡添加驅動程式。

第 6 章
=====

Locking
=======

大多數內核（包括 xv6）都會交錯執行多個 activity。交錯的一個來源是多處理器硬體：具有多個 CPU 獨立執行的計算機，例如 xv6 的 RISC-V。這些多個 CPU 共用物理 RAM，而 xv6 利用共用來維護所有 CPU 讀取和寫入的數據結構。這種共用增加了一個 CPU 讀取數據結構而另一個 CPU 正在更新數據結構的可能性，甚至多個 CPU 同時更新相同的數據;如果不仔細設計，這種並行訪問可能會產生不正確的結果或損壞的數據結構。即使在單處理器上，內核也可能在多個線程之間切換 CPU，從而導致它們的執行交錯。最後，如果中斷發生在錯誤的時間，則修改與某些可中斷代碼相同的數據的設備中斷處理程式可能會損壞數據。單詞併發是指由於多處理器並行性、線程切換或中斷而導致多個指令流交錯的情況。

內核中充滿了併發訪問的數據。例如，兩個 CPU 可以同時調用 kalloc，從而同時從空閒清單的頭部彈出。內核設計人員喜歡允許大量併發，因為它可以通過並行性提高性能，並提高回應能力。但是，因此，儘管存在這種併發性，但內核設計人員必須說服自己正確性。有很多方法可以得出正確的代碼，有些方法比其他方法更容易推理。旨在實現併發性的正確性的策略以及支持它們的抽象稱為併發控制技術。

Xv6 根據方式使用了多種併發控制技術;還有更多的可能性。本章重點介紹一種廣泛使用的技術：thelock。鎖提供互斥，確保一次只有一個CPU可以持有鎖。如果程式師將鎖與每個共享數據項關聯，並且代碼在使用項時始終持有關聯的鎖，則該專案一次只能由一個 CPU 使用。在這種情況下，我們說鎖保護數據項。儘管鎖是一種易於理解的併發控制機制，但鎖的缺點是它們會限制性能，因為它們會序列化併發操作。

本章的其餘部分解釋了為什麼 xv6 需要鎖，xv6 如何實現鎖，以及它如何使用鎖。

CPU CPU

l->next = list l->next = list


list


Memory

BUS


Figure 6.1: Simplified SMP architecture


### 6.1 Races

作為我們為什麼需要鎖的一個例子，考慮兩個進程，其中有退出的子進程調用兩個不同的CPU。wait釋放子進程的記憶體。因此，在每個CPU上，內核將 callkfree 以釋放子級的記憶體頁。內核分配器維護一個鏈表：kalloc（）（ker- nel/kalloc.c：69）從空閒頁面清單中彈出一個記憶體頁，並且 kfree（）（kernel/kalloc.c：47） 將一個頁面推送到空閒清單上。為了獲得最佳性能，我們可能希望兩個父進程的 kfrees 能夠並行執行，而不必等待另一個，但考慮到 xv6 的 skfree實現，這是不正確的。

圖 6.1 更詳細地說明了該設置：空閑頁的連結清單位於兩個 CPU 共用的記憶體中，這兩個 CPU 使用 load 和 store 指令操作清單。（實際上，處理器具有高速緩存，但從概念上講，多處理器系統的行為就像存在單個共用記憶體一樣。如果沒有併發請求，您可以實施 listpushoperation，如下所示：

1 struct element {
2 int data;
3 struct element *next;
4 };
5
6 struct element *list = 0;
7
8 void
9 push(int data)
10 {
11 struct element *l;
12
13 l = malloc(sizeof *l);
14 l->data = data;
15 l->next = list;
16 list = l;


Memory


CPU 1


CPU2
15


l->next


16


list


15 16


l->next list


Time


Figure 6.2: Example race


17 }


如果單獨執行，則此實現是正確的。但是，如果同時執行多個副本，則代碼不正確。如果兩個 CPU 同時執行 push，則兩個 CPU 都可能執行第 15 行，如圖 6.1 所示，在任何一個執行第 16 行之前，這會導致不正確的結果，如圖 6.2 所示。然後將有兩個 list 元素，其中 nextset 設置為前一個值 list。當兩個賦值 tolist發生在第 16 行時，第二個賦值將覆蓋第一個賦值;第一個賦值中涉及的元素將丟失。第 16 行的 lost update 是大race 的一個示例。爭用是指同時訪問記憶體位置，並且至少有一個訪問是寫入的情況。爭用通常是 bug 的標誌，要麼是丟失的更新（如果訪問是寫入的），要麼是讀取未完全更新的數據結構。爭用的結果取決於編譯器生成的機器代碼、所涉及的兩個 CPU 的時序以及記憶體系統如何對它們的記憶體操作進行排序，這可能會使爭用引起的錯誤難以重現和調試。例如，在 debuggingpush 時添加 print 語句可能會改變執行時間，使爭用消失。避免 race 的常用方法是使用鎖。鎖確保互斥，因此一次只有一個 CPU 可以執行敏感的 push 行;這使得上述情況不可能。上述代碼的正確鎖定版本只新增了幾行代碼（以黃色突出顯示）：

6 struct element *list = 0;
7 struct lock listlock;
8
9 void
10 push(int data)
11 {
12 struct element *l;
13 l = malloc(sizeof *l);
14 l->data = data;


15
16 acquire(&listlock);
17 l->next = list;
18 list = l;
19 release(&listlock);
20 }


acquireandrelease 之間的指令序列通常稱為非關鍵部分。該鎖通常稱為 protectinglist。

When we say that a lock protects data, we really mean that the lock protects some collection of invariants that apply to the data. Invariants are properties of data structures that are maintained across operations. Typically, an operation’s correct behavior depends on the invariants being true when the operation begins. The operation may temporarily violate the invariants but must reestab- lish them before finishing. For example, in the linked list case, the invariant is thatlistpoints at the first element in the list and that each element’snextfield points at the next element. The implementation ofpushviolates this invariant temporarily: in line 17,lpoints to the next list element, butlistdoes not point atlyet (reestablished at line 18). The race we examined above happened because a second CPU executed code that depended on the list invariants while they were (temporarily) violated. Proper use of a lock ensures that only one CPU at a time can operate on the data structure in the critical section, so that no CPU will execute a data structure operation when the data structure’s invariants do not hold.當我們說鎖保護數據時，我們實際上是指鎖保護適用於數據的某些不變量集合。不變量是跨操作維護的數據結構的屬性。通常，操作的正確行為取決於操作開始時的不變量是否為 true。該操作可能會暫時違反不變量，但必須在完成之前重新建立它們。例如，在鏈表情況下，不變量是 thatlistpoints 在清單中的第一個元素上，並且每個元素的 nextfield 都指向下一個元素。push的實現暫時違反了這個不變量：在第 17 行，l指向下一個清單元素，butlist不指向 atlyet（在第 18 行重新建立）。我們上面檢查的競爭之所以發生，是因為第二個 CPU 執行了依賴於清單不變量的代碼，而它們（暫時）被違反了。正確使用鎖可確保一次只有一個 CPU 可以對 critical 部分中的數據結構進行操作，因此當數據結構的不變量不成立時，沒有 CPU 會執行數據結構操作。

You can think of a lock asserializingconcurrent critical sections so that they run one at a time, and thus preserve invariants (assuming the critical sections are correct in isolation). You can also think of critical sections guarded by the same lock as being atomic with respect to each other, so that each sees only the complete set of changes from earlier critical sections, and never sees partially-completed updates.你可以把鎖 asserializingconcurrent critical sections 想像成這樣它們一次運行一個，從而保留不變量（假設 critical 部分在隔離中是正確的）。您還可以將由同一鎖保護的關鍵部分視為彼此之間的原子，以便每個部分只能看到早期關鍵部分的完整更改集，而永遠不會看到部分完成的更新。

儘管鎖對正確性很有用，但鎖本身會限制性能。例如，如果兩個進程同時調用 kfree，則鎖將序列化兩個關鍵部分，因此在不同的 CPU 上運行它們沒有任何好處。如果多個進程同時想要同一個鎖，或者鎖遇到爭用，我們說多個進程衝突。內核設計中的一個主要挑戰是避免鎖爭用以追求並行性。Xv6 幾乎沒有做這些，但複雜的內核專門組織數據結構和演算法以避免鎖爭用。在列表示例中，內核可以為每個CPU維護一個單獨的空閒清單，並且只有在當前CPU的清單為空並且它必須從另一個CPU竊取記憶體時，內核才會觸及另一個CPU的空閒清單。其他用例可能需要更複雜的設計。

鎖的位置對性能也很重要。例如，在第 13 行之前 moveacquireearlier inpush 是正確的。但這可能會降低性能，因為這樣調用 tomalloc 將被序列化。下面的“使用鎖”部分提供了有關在何處插入acquireandreleaseinvocations的一些準則。

### 6.2 Code: Locks

Xv6 有兩種類型的鎖：自旋鎖和睡眠鎖。我們將從旋轉鎖開始。Xv6 將自旋鎖表示為 astruct spinlock（kernel/spinlock.h：2）。結構中的重要欄位是locked，當lock可用時該詞為零，當lock處於持有狀態時為非零。從邏輯上講，xv6 應該通過執行類似

21 void
22 acquire(struct spinlock *lk) // does not work!
23 {
24 for(;;) {
25 if(lk->locked == 0) {
26 lk->locked = 1;
27 break;
28 }
29 }
30 }


Unfortunately, this implementation does not guarantee mutual exclusion on a multiprocessor. It could happen that two CPUs simultaneously reach line 25, see thatlk->lockedis zero, and then both grab the lock by executing line 26. At this point, two different CPUs hold the lock, which violates the mutual exclusion property. What we need is a way to make lines 25 and 26 execute as anatomic(i.e., indivisible) step.不幸的是，此 implementation 並不能保證在 multiprocessor 上互斥。可能會發生兩個 CPU 同時到達第 25 行的情況，看到 lk->lockeded 為零，然後都通過執行第 26 行來獲取鎖。此時，兩個不同的CPU持有鎖，這違反了互斥屬性。我們需要的是一種使第 25 行和第 26 行作為解剖學（即不可分割）步驟執行的方法。

Because locks are widely used, multi-core processors usually provide instructions that imple- ment an atomic version of lines 25 and 26. On the RISC-V this instruction isamoswap r, a. amoswapreads the value at the memory addressa, writes the contents of registerrto that address, and puts the value it read intor. That is, it swaps the contents of the register and the memory address. It performs this sequence atomically, using special hardware to prevent any other CPU from using the memory address between the read and the write.由於鎖被廣泛使用，多核處理器通常提供實現第 25 行和第 26 行的原子版本的指令。在 RISC-V 上，此指令 isamoswap r， a. amoswap讀取記憶體位址 a 處的值，將 registerr 的內容寫入該位址，並將它讀取的值放入 intor。也就是說，它交換 register 和 memory 位址的內容。它以原子方式執行此序列，使用特殊硬體來防止任何其他 CPU 在讀取和寫入之間使用記憶體位址。

Xv6’sacquire(kernel/spinlock.c:22)uses the portable C library call\_\_sync\_lock\_test\_and\_set, which boils down to theamoswapinstruction; the return value is the old (swapped) contents of lk->locked. Theacquirefunction wraps the swap in a loop, retrying (spinning) until it has acquired the lock. Each iteration swaps one intolk->lockedand checks the previous value; if the previous value is zero, then we’ve acquired the lock, and the swap will have setlk->locked to one. If the previous value is one, then some other CPU holds the lock, and the fact that we atomically swapped one intolk->lockeddidn’t change its value.Xv6 的 acquire（kernel/spinlock.c：22） 使用可移植的 C 庫call\_\_sync\_lock\_test\_and\_set，歸結為 theamoswapinstruction;返回值是 lk->locked 的舊 （交換） 內容。acquire函數將交換包裝在一個迴圈中，重試 （旋轉） 直到它獲取了鎖。每次反覆運算交換一個 intolk->locked並檢查前一個值;如果前一個值為零，則我們已獲得鎖，並且交換會將 setlk->locked 為 1。如果前一個值是 1，那麼其他一些 CPU 持有鎖，並且我們原子交換了一個 intolk->locked 的事實並沒有改變它的值。

Once the lock is acquired,acquirerecords, for debugging, the CPU that acquired the lock. Thelk->cpufield is protected by the lock and must only be changed while holding the lock.獲取鎖后，acquirerecords 獲取鎖的CPU（用於調試）。thelk->cpu字段受鎖保護，只能在持有鎖時進行更改。

The functionrelease(kernel/spinlock.c:47)is the opposite ofacquire: it clears thelk->cpu field and then releases the lock. Conceptually, the release just requires assigning zero tolk->locked. The C standard allows compilers to implement an assignment with multiple store instructions, so a C assignment might be non-atomic with respect to concurrent code. Instead,releaseuses the C library function\_\_sync\_lock\_releasethat performs an atomic assignment. This function also boils down to a RISC-Vamoswapinstruction.函數release（kernel/spinlock.c：47）與 acquire 相反：它清除 lk->cpu 字段，然後釋放鎖。從概念上講，該版本只需要分配零 tolk->locked。C 標準允許編譯器使用多個 store 指令實現賦值，因此 C 賦值對於併發代碼可能是非原子的。相反，release使用 C 庫function\_\_sync\_lock\_releasethat執行原子賦值。這個函數也歸結為 RISC-Vamoswap指令。

### 6.3 Code: Using locks

Xv6 uses locks in many places to avoid races. As described above,kalloc(kernel/kalloc.c:69)and kfree(kernel/kalloc.c:47)form a good example. Try Exercises 1 and 2 to see what happens if those functions omit the locks. You’ll likely find that it’s difficult to trigger incorrect behavior, suggesting that it’s hard to reliably test whether code is free from locking errors and races. Xv6 may well have as-yet-undiscovered races. A hard part about using locks is deciding how many locks to use and which data and invariants each lock should protect. There are a few basic principles. First, any time a variable can be written by one CPU at the same time that another CPU can read or write it, a lock should be used to keep the two operations from overlapping. Second, remember that locks protect invariants: if an invariant involves multiple memory locations, typically all of them need to be protected by a single lock to ensure the invariant is maintained. The rules above say when locks are necessary but say nothing about when locks are unneces- sary, and it is important for efficiency not to lock too much, because locks reduce parallelism. If parallelism isn’t important, then one could arrange to have only a single thread and not worry about locks. A simple kernel can do this on a multiprocessor by having a single lock that must be ac- quired on entering the kernel and released on exiting the kernel (though blocking system calls such as pipe reads orwaitwould pose a problem). Many uniprocessor operating systems have been converted to run on multiprocessors using this approach, sometimes called a “big kernel lock,” but the approach sacrifices parallelism: only one CPU can execute in the kernel at a time. If the kernel does any heavy computation, it would be more efficient to use a larger set of more fine-grained locks, so that the kernel could execute on multiple CPUs simultaneously. As an example of coarse-grained locking, xv6’skalloc.callocator has a single free list pro- tected by a single lock. If multiple processes on different CPUs try to allocate pages at the same time, each will have to wait for its turn by spinning inacquire. Spinning wastes CPU time, since it’s not useful work. If contention for the lock wasted a significant fraction of CPU time, perhaps performance could be improved by changing the allocator design to have multiple free lists, each with its own lock, to allow truly parallel allocation. As an example of fine-grained locking, xv6 has a separate lock for each file, so that processes that manipulate different files can often proceed without waiting for each other’s locks. The file locking scheme could be made even more fine-grained if one wanted to allow processes to simul- taneously write different areas of the same file. Ultimately lock granularity decisions need to be driven by performance measurements as well as complexity considerations. As subsequent chapters explain each part of xv6, they will mention examples of xv6’s use of locks to deal with concurrency. As a preview, Figure 6.3 lists all of the locks in xv6.Xv6 在許多地方使用鎖來避免爭用。如上所述，kalloc（kernel/kalloc.c：69） 和 kfree（kernel/kalloc.c：47） 就是一個很好的例子。嘗試練習 1 和 2，看看如果這些函數省略了鎖會發生什麼情況。您可能會發現很難觸發不正確的行為，這表明很難可靠地測試代碼是否沒有鎖定錯誤和爭用。Xv6 很可能有尚未被發現的種族。使用鎖的一個難點是決定使用多少個鎖以及每個鎖應該保護哪些數據和不變量。有一些基本原則。首先，每當一個 CPU 可以寫入一個變數，而另一個 CPU 可以讀取或寫入該變數時，都應該使用鎖來防止兩個操作重疊。其次，請記住鎖保護不變量：如果一個不變量涉及多個記憶體位置，通常所有記憶體位置都需要由單個鎖保護，以確保保持不變量。上面的規則說明了何時需要鎖，但沒有說明何時不需要鎖，並且為了提高效率，重要的是不要鎖定太多，因為鎖會降低並行性。如果並行性不重要，那麼可以安排只有一個線程，而不用擔心鎖。一個簡單的內核可以在多處理器上做到這一點，因為它有一個鎖，該鎖必須在進入內核時獲得，並在退出內核時釋放（儘管阻止系統調用，如管道讀取或 wait會帶來問題）。許多單處理器操作系統已使用這種方法轉換為在多處理器上運行，有時稱為“大內核鎖”，但這種方法犧牲了並行性：一次只有一個 CPU 可以在內核中執行。 如果內核執行任何繁重的計算，則使用更大、更細粒度的鎖集會更有效，以便內核可以同時在多個 CPU 上執行。作為粗粒度鎖定的一個例子，xv6'skalloc.callocator 有一個由單個鎖保護的空閒清單。如果不同 CPU 上的多個進程嘗試同時分配頁面，則每個進程都必須通過旋轉 inacquire 來等待輪到它。旋轉會浪費 CPU 時間，因為它不是有用的工作。如果對鎖的爭用浪費了很大一部分 CPU 時間，也許可以通過更改分配器設計來提高性能，每個清單都有自己的鎖，以實現真正的並行分配。作為精細鎖定的一個示例，xv6 為每個檔提供單獨的鎖定，因此處理不同文件的進程通常可以在不等待彼此的鎖定的情況下繼續進行。如果希望允許進程同時寫入同一檔的不同區域，則可以使文件鎖定方案更加細粒度。最終，鎖定粒度決策需要由性能測量和複雜性考慮驅動。在後續章節解釋 xv6 的每個部分時，它們將提到 xv6 使用鎖來處理併發的範例。作為預覽，圖 6.3 列出了 xv6 中的所有鎖。

### 6.4 Deadlock and lock ordering

If a code path through the kernel must hold several locks at the same time, it is important that all code paths acquire those locks in the same order. If they don’t, there is a risk ofdeadlock. Let’s say two code paths in xv6 need locks A and B, but code path 1 acquires locks in the order A then如果通過內核的代碼路徑必須同時持有多個鎖，則所有代碼路徑都以相同的順序獲取這些鎖，這一點很重要。如果他們不這樣做，則存在死鎖的風險。假設 xv6 中的兩個代碼路徑需要鎖 A 和 B，但代碼路徑 1 按順序 A 獲取鎖

Lock Description
bcache.lock Protects allocation of block buffer cache entries
cons.lock Serializes access to console hardware, avoids intermixed output
ftable.lock Serializes allocation of a struct file in file table
itable.lock Protects allocation of in-memory inode entries
vdisk_lock Serializes access to disk hardware and queue of DMA descriptors
kmem.lock Serializes allocation of memory
log.lock Serializes operations on the transaction log
pipe’s pi->lock Serializes operations on each pipe
pid_lock Serializes increments of next_pid
proc’s p->lock Serializes changes to process’s state
wait_lock Helps wait avoid lost wakeups
tickslock Serializes operations on the ticks counter
inode’s ip->lock Serializes operations on each inode and its content
buf’s b->lock Serializes operations on each block buffer


Figure 6.3: Locks in xv6


B, and the other path acquires them in the order B then A. Suppose thread T1 executes code path 1 and acquires lock A, and thread T2 executes code path 2 and acquires lock B. Next T1 will try to acquire lock B, and T2 will try to acquire lock A. Both acquires will block indefinitely, because in both cases the other thread holds the needed lock, and won’t release it until its acquire returns. To avoid such deadlocks, all code paths must acquire locks in the same order. The need for a global lock acquisition order means that locks are effectively part of each function’s specification: callers must invoke functions in a way that causes locks to be acquired in the agreed-on order.B 中，另一個路徑按照 B 和 A 的順序獲取它們。假設線程 T1 執行代碼路徑 1 並獲取鎖 A，線程 T2 執行代碼路徑 2 並獲取鎖 B。接下來，T1 將嘗試獲取鎖 B，T2 將嘗試獲取鎖 A。兩個 acquires 都將無限期地阻塞，因為在這兩種情況下，另一個線程都持有所需的鎖，並且在其 acquire 傳回之前不會釋放它。為避免此類死鎖，所有代碼路徑必須以相同的 Sequences 獲取鎖。對全域鎖獲取順序的需求意味著鎖實際上是每個函數規範的一部分：調用者必須以一種導致按商定順序獲取鎖的方式調用函數。

Xv6 has many lock-order chains of length two involving per-process locks (the lock in each struct proc) due to the way thatsleepworks (see Chapter 7). For example,consoleintr (kernel/console.c:136)is the interrupt routine which handles typed characters. When a newline ar- rives, any process that is waiting for console input should be woken up. To do this,consoleintr holdscons.lockwhile callingwakeup, which acquires the waiting process’s lock in order to wake it up. In consequence, the global deadlock-avoiding lock order includes the rule thatcons.lock must be acquired before any process lock. The file-system code contains xv6’s longest lock chains. For example, creating a file requires simultaneously holding a lock on the directory, a lock on the new file’s inode, a lock on a disk block buffer, the disk driver’svdisk\_lock, and the calling pro- cess’sp->lock. To avoid deadlock, file-system code always acquires locks in the order mentioned in the previous sentence.由於 sleepworks 的方式（參見第 7 章），Xv6 有許多長度為 2 的鎖順序鏈，涉及每個進程的鎖（每個 struct proc 中的鎖）。例如，consoleintr （kernel/console.c：136） 是處理類型字元的中斷例程。當換行符到達時，任何正在等待控制台輸入的進程都應該被喚醒。為此，consoleintr holdscons.lock同時調用 wakeup，它獲取等待進程的鎖以喚醒它。因此，全域避免死鎖鎖定順序包括必須在任何進程鎖定之前獲取 cons.lock 的規則。檔案系統代碼包含 xv6 最長的鎖鏈。例如，創建檔需要同時持有目錄上的鎖、新檔的 inode 上的鎖、磁碟塊緩衝區上的鎖、磁碟驅動程式的svdisk\_lock以及調用程式 sp->lock。為避免死鎖，文件系統代碼始終按照上一句中提到的順序獲取鎖。

Honoring a global deadlock-avoiding order can be surprisingly difficult. Sometimes the lock order conflicts with logical program structure, e.g., perhaps code module M1 calls module M2, but the lock order requires that a lock in M2 be acquired before a lock in M1. Sometimes the identities of locks aren’t known in advance, perhaps because one lock must be held in order to discover the identity of the lock to be acquired next. This kind of situation arises in the file system as it looks up successive components in a path name, and in the code forwaitandexitas they search the table遵守避免全域僵局的順序可能非常困難。有時鎖順序與邏輯程序結構衝突，例如，可能代碼模組 M1 調用模組 M2，但鎖順序要求 M2 中的鎖在 M1 中的鎖之前獲取。有時，鎖的身份是事先不知道的，可能是因為必須持有一把鎖才能發現接下來要獲取的鎖的身份。這種情況出現在文件系統中，因為它在路徑名中查找連續的元件，而在代碼 forwaitandexit中，當它們搜索表時

of processes looking for child processes. Finally, the danger of deadlock is often a constraint on how fine-grained one can make a locking scheme, since more locks often means more opportunity for deadlock. The need to avoid deadlock is often a major factor in kernel implementation.的進程查找子進程。最後，死鎖的危險通常是限制了鎖定方案的細粒度，因為更多的鎖通常意味著更多的死鎖機會。避免死鎖的需要通常是內核實現中的一個主要因素。

### 6.5 Re-entrant locks

It might appear that some deadlocks and lock-ordering challenges could be avoided by usingre- entrant locks, which are also calledrecursive locks. The idea is that if the lock is held by a process and if that process attempts to acquire the lock again, then the kernel could just allow this (since the process already has the lock), instead of calling panic, as the xv6 kernel does. It turns out, however, that re-entrant locks make it harder to reason about concurrency: re- entrant locks break the intuition that locks cause critical sections to be atomic with respect to other critical sections. Consider the following functionsfandg, and a hypothetical functionh:似乎可以通過使用重入鎖（也稱為遞歸鎖）來避免一些死鎖和鎖排序挑戰。這個想法是，如果鎖被一個進程持有，並且該進程試圖再次獲取鎖，那麼內核可以只允許這樣做（因為該進程已經有鎖），而不是像 xv6 內核那樣調用 panic。然而，事實證明，重入鎖使併發性推理變得更加困難：重入鎖打破了鎖導致關鍵部分相對於其他關鍵部分是原子的直覺。考慮以下 functionsfandg 和一個假設的 functionh：

struct spinlock lock;
int data = 0; // protected by lock


f() {
acquire(&lock);
if(data == 0){
call_once();
h();
data = 1;
}
release(&lock);
}


g() {
aquire(&lock);
if(data == 0){
call_once();
data = 1;
}
release(&lock);
}


h() { ... } Looking at this code fragment, the intuition is thatcall\_oncewill be called only once: either byf, or byg, but not by both. But if re-entrant locks are allowed, andhhappens to callg,call\_oncewill be calledtwice. If re-entrant locks aren’t allowed, thenhcallinggresults in a deadlock, which is not great either. But, assuming it would be a serious error to callcall\_once, a deadlock is preferable. Theh() { ... }查看此代碼片段，直覺thatcall\_oncewill只能調用一次：byf 或 byg，但不能同時調用兩者。但是，如果允許重入鎖，則 andh恰好調用 callg，call\_oncewill 被調用兩次。如果不允許重入鎖，則 thenhcallingg會導致死鎖，這也不是很好。但是，假設callcall\_once這是一個嚴重的錯誤，則最好使用死鎖。這

kernel developer will observe the deadlock (the kernel panics) and can fix the code to avoid it, while callingcall\_oncetwice may silently result in an error that is difficult to track down. For this reason, xv6 uses the simpler to understand non-re-entrant locks. As long as program- mers keep the locking rules in mind, however, either approach can be made to work. If xv6 were to use re-entrant locks, one would have to modifyacquireto notice that the lock is currently held by the calling thread. One would also have to add a count of nested acquires to struct spinlock, in similar style topush\_off, which is discussed next.內核開發人員將觀察死鎖（內核 panics）並可以修復代碼以避免它，而callingcall\_oncetwice可能會悄無聲息地導致難以追蹤的錯誤。因此，xv6 使用更簡單的方法來理解不可重入鎖。然而，只要程式師牢記鎖定規則，任何一種方法都可以奏效。如果 xv6 要使用重入鎖，則必須修改acquire以注意到該鎖當前由調用線程持有。還必須以類似的樣式將嵌套 acquires 的計數添加到 struct spinlock topush\_off，這將在下面討論。

### 6.6 Locks and interrupt handlers

Some xv6 spinlocks protect data that is used by both threads and interrupt handlers. For example, theclockintrtimer interrupt handler might incrementticks(kernel/trap.c:164)at about the same time that a kernel thread readsticksinsys\_sleep(kernel/sysproc.c:61). The locktickslock serializes the two accesses. The interaction of spinlocks and interrupts raises a potential danger. Supposesys\_sleepholds tickslock, and its CPU is interrupted by a timer interrupt.clockintrwould try to acquire tickslock, see it was held, and wait for it to be released. In this situation,tickslockwill never be released: onlysys\_sleepcan release it, butsys\_sleepwill not continue running until clockintrreturns. So the CPU will deadlock, and any code that needs either lock will also freeze. To avoid this situation, if a spinlock is used by an interrupt handler, a CPU must never hold that lock with interrupts enabled. Xv6 is more conservative: when a CPU acquires any lock, xv6 always disables interrupts on that CPU. Interrupts may still occur on other CPUs, so an interrupt’s acquirecan wait for a thread to release a spinlock; just not on the same CPU. Xv6 re-enables interrupts when a CPU holds no spinlocks; it must do a little book-keeping to cope with nested critical sections.acquirecallspush\_off(kernel/spinlock.c:89)andrelease callspop\_off(kernel/spinlock.c:100)to track the nesting level of locks on the current CPU. When that count reaches zero,pop\_offrestores the interrupt enable state that existed at the start of the outermost critical section. Theintr\_offandintr\_onfunctions execute RISC-V instructions to disable and enable interrupts, respectively. It is important thatacquirecallpush\_offstrictly before settinglk->locked(kernel/spin- lock.c:28). If the two were reversed, there would be a brief window when the lock was held with interrupts enabled, and an unfortunately timed interrupt would deadlock the system. Similarly, it is important thatreleasecallpop\_offonly after releasing the lock(kernel/spinlock.c:66).某些 xv6 自旋鎖保護線程和中斷處理程式使用的數據。例如，clockintrtimer 中斷處理程式可能會在內核線程readsticksinsys\_sleep （kernel/sysproc.c：61） 的同時增加 ticks（kernel/trap.c：164）。locktickslock序列化這兩個訪問。自旋鎖和中斷的交互會帶來潛在的危險。Supposesys\_sleepholds tickslock，並且它的 CPU 被定時器 interrupt.clockintr 中斷，將嘗試獲取 tickslock，看到它被持有，並等待它被釋放。在這種情況下，tickslock將永遠不會被釋放：onlysys\_sleepcan釋放它，butsys\_sleepwill在 clockintr 返回之前不要繼續運行。因此，CPU 將死鎖，任何需要任一鎖的代碼也將凍結。為避免這種情況，如果中斷處理程式使用旋轉鎖，則 CPU 絕不能在啟用中斷的情況下持有該鎖。Xv6 更保守：當 CPU 獲取任何鎖時，xv6 始終禁用該 CPU 上的中斷。中斷可能仍發生在其他CPU上，因此中斷的acquires可以等待線程釋放自旋鎖;只是不在同一個CPU上。Xv6 在 CPU 沒有自旋鎖時重新啟用中斷;它必須做一些記賬來應對嵌套的關鍵sections.acquirecallspush\_off （kernel/spinlock.c：89） 和 release callspop\_off （kernel/spinlock.c：100） 來跟蹤當前 CPU 上鎖的嵌套級別。當該計數達到零時，pop\_offrestores最外層關鍵部分開始時存在的中斷啟用狀態。Theintr\_offandintr\_onfunctions執行 RISC-V 指令分別禁用和啟用中斷。在 setlk->locked（kernel/spin- lock.c：28） 之前thatacquirecallpush\_offstrictly很重要。 如果兩者顛倒，則在啟用中斷的情況下持有鎖時將有一個短暫的視窗，不幸的是，定時中斷將使系統死鎖。同樣，在釋放鎖 （kernel/spinlock.c：66） 後thatreleasecallpop\_offonly也很重要。

### 6.7 指令和記憶體排序

很自然地會認為程式按照原始程式碼語句出現的順序執行。對於單線程代碼來說，這是一個合理的心智模型，但當多個線程通過共用記憶體交互時，這是不正確的 \[2， 4\]。一個原因是編譯器以與原始程式碼隱含的順序不同的順序發出load和 store 指令，並且可能會完全省略它們（例如，通過在registers 中緩存數據）。另一個原因是 CPU 可能會亂序執行指令

to increase performance. For example, a CPU may notice that in a serial sequence of instructions A and B are not dependent on each other. The CPU may start instruction B first, either because its inputs are ready before A’s inputs, or in order to overlap execution of A and B. As an example of what could go wrong, in this code forpush, it would be a disaster if the compiler or CPU moved the store corresponding to line 4 to a point after thereleaseon line 6:以提高性能。例如，CPU 可能會注意到，在指令的串行序列中，A 和 B 並不相互依賴。CPU 可以先啟動指令 B，要麼是因為它的輸入在 A 的輸入之前就準備好了，要麼是為了重疊 A 和 B 的執行。例如，在此代碼 forpush 中，如果編譯器或 CPU 將與第 4 行對應的存儲移動到第 6 行 release之後的某個點，那將是一場災難：

1 l = malloc(sizeof *l);
2 l->data = data;
3 acquire(&listlock);
4 l->next = list;
5 list = l;
6 release(&listlock);


If such a re-ordering occurred, there would be a window during which another CPU could acquire the lock and observe the updatedlist, but see an uninitializedlist->next. The good news is that compilers and CPUs help concurrent programmers by following a set of rules called thememory model, and by providing some primitives to help programmers control re-ordering. To tell the hardware and compiler not to re-order, xv6 uses\_\_sync\_synchronize()in both acquire(kernel/spinlock.c:22)andrelease(kernel/spinlock.c:47).\_\_sync\_synchronize()is a memory barrier: it tells the compiler and CPU to not reorder loads or stores across the barrier. The barriers in xv6’sacquireandreleaseforce order in almost all cases where it matters, since xv6 uses locks around accesses to shared data. Chapter 9 discusses a few exceptions.如果發生此類重新排序，則會出現一個視窗，在此期間，另一個 CPU 可以獲取鎖並觀察 updatedlist，但會看到 uninitializedlist->next。好消息是，編譯器和 CPU 通過遵循一組稱為記憶體模型的規則來幫助併發程式師，並提供一些基元來幫助程式員控制重新排序。為了告訴硬體和編譯器不要重新排序，acquire（kernel/spinlock.c：22）和 release（kernel/spinlock.c：47）.\_\_sync\_synchronize（） 中的 xv6 uses\_\_sync\_synchronize（） 是一個記憶體屏障：它告訴編譯器和 CPU 不要跨屏障對載入或存儲重新排序。xv6 的 acquireandreleaseforce 中的屏障幾乎在所有重要情況下都會排序，因為 xv6 在訪問共享數據時使用鎖。第 9 章討論了一些例外情況。

### 6.8 Sleep locks

Sometimes xv6 needs to hold a lock for a long time. For example, the file system (Chapter 8) keeps a file locked while reading and writing its content on the disk, and these disk operations can take tens of milliseconds. Holding a spinlock that long would lead to waste if another process wanted to acquire it, since the acquiring process would waste CPU for a long time while spinning. Another drawback of spinlocks is that a process cannot yield the CPU while retaining a spinlock; we’d like to do this so that other processes can use the CPU while the process with the lock waits for the disk. Yielding while holding a spinlock is illegal because it might lead to deadlock if a second thread then tried to acquire the spinlock; sinceacquiredoesn’t yield the CPU, the second thread’s spinning might prevent the first thread from running and releasing the lock. Yielding while holding a lock would also violate the requirement that interrupts must be off while a spinlock is held. Thus we’d like a type of lock that yields the CPU while waiting to acquire, and allows yields (and interrupts) while the lock is held. Xv6 provides such locks in the form ofsleep-locks.acquiresleep(kernel/sleeplock.c:22) yields the CPU while waiting, using techniques that will be explained in Chapter 7. At a high level, a sleep-lock has alockedfield that is protected by a spinlock, andacquiresleep’s call tosleepatomically yields the CPU and releases the spinlock. The result is that other threads can execute whileacquiresleepwaits.有時 xv6 需要長時間持鎖。例如，文件系統（第 8 章）在磁碟上讀取和寫入文件內容時保持檔鎖定，這些磁碟操作可能需要數十毫秒。如果另一個進程想要獲取自旋鎖，那麼保持自旋鎖這麼長時間會導致浪費，因為獲取進程會在自旋時長時間浪費 CPU。自旋鎖的另一個缺點是，進程無法在保留自旋鎖的同時產生CPU;我們希望這樣做，以便其他進程可以在帶鎖的進程等待磁碟時使用CPU。在持有自旋鎖時讓步是非法的，因為如果第二個線程隨後嘗試獲取自旋鎖，則可能會導致死鎖;sinceacquire不會產生 CPU，則第二個線程的旋轉可能會阻止第一個線程運行和釋放鎖。在持有鎖時讓步也會違反在持有自旋鎖時必須關閉中斷的要求。因此，我們想要一種鎖，它在等待 acquire 時產生 CPU，並在持有鎖時允許 yields （和中斷）。Xv6 以 sleep-locks.acquiresleep（kernel/sleeplock.c：22） 的形式提供這樣的鎖，在等待時產生 CPU，使用的技術將在第 7 章中解釋。在高級別上，sleep-lock 具有受自旋鎖保護的 alockedfield，並且acquiresleep 的調用 sleepatomically 生成 CPU 並釋放自旋鎖。結果是其他線程可以執行 whileacquiresleepwaits。

Because sleep-locks leave interrupts enabled, they cannot be used in interrupt handlers. Be- causeacquiresleepmay yield the CPU, sleep-locks cannot be used inside spinlock critical sections (though spinlocks can be used inside sleep-lock critical sections). Spin-locks are best suited to short critical sections, since waiting for them wastes CPU time; sleep-locks work well for lengthy operations.由於睡眠鎖使中斷處於啟用狀態，因此不能在中斷處理程式中使用它們。由於acquiresleep可能會產生 CPU，因此不能在自旋鎖關鍵部分內使用睡眠鎖（儘管可以在睡眠鎖關鍵部分內使用自旋鎖）。自旋鎖最適合於短的關鍵部分，因為等待它們會浪費 CPU 時間;sleep-locks 適用於長時間的操作。

### 6.9 Real world

Programming with locks remains challenging despite years of research into concurrency primitives and parallelism. It is often best to conceal locks within higher-level constructs like synchronized queues, although xv6 does not do this. If you program with locks, it is wise to use a tool that attempts to identify races, because it is easy to miss an invariant that requires a lock. Most operating systems support POSIX threads (Pthreads), which allow a user process to have several threads running concurrently on different CPUs. Pthreads has support for user-level locks, barriers, etc. Pthreads also allows a programmer to optionally specify that a lock should be re- entrant. Supporting Pthreads at user level requires support from the operating system. For example, it should be the case that if one pthread blocks in a system call, another pthread of the same process should be able to run on that CPU. As another example, if a pthread changes its process’s address space (e.g., maps or unmaps memory), the kernel must arrange that other CPUs that run threads of the same process update their hardware page tables to reflect the change in the address space. It is possible to implement locks without atomic instructions \[10\], but it is expensive, and most operating systems use atomic instructions. Locks can be expensive if many CPUs try to acquire the same lock at the same time. If one CPU has a lock cached in its local cache, and another CPU must acquire the lock, then the atomic instruction to update the cache line that holds the lock must move the line from the one CPU’s cache to the other CPU’s cache, and perhaps invalidate any other copies of the cache line. Fetching a cache line from another CPU’s cache can be orders of magnitude more expensive than fetching a line from a local cache. To avoid the expenses associated with locks, many operating systems use lock-free data struc- tures and algorithms \[6, 12\]. For example, it is possible to implement a linked list like the one in the beginning of the chapter that requires no locks during list searches, and one atomic instruction to insert an item in a list. Lock-free programming is more complicated, however, than programming locks; for example, one must worry about instruction and memory reordering. Programming with locks is already hard, so xv6 avoids the additional complexity of lock-free programming.儘管對併發基元和並行性進行了多年的研究，但使用鎖進行程式設計仍然具有挑戰性。通常最好將鎖隱藏在更高級別的結構（如同步佇列）中，儘管 xv6 不這樣做。如果使用鎖進行程式設計，則明智的做法是使用嘗試識別種族的工具，因為很容易錯過需要鎖的不變量。大多數操作系統都支援 POSIX 線程 （Pthread），它允許用戶進程在不同的 CPU 上同時運行多個線程。Pthreads 支援用戶級鎖、屏障等。Pthreads 還允許程式師選擇性地指定鎖應該是可重入的。在用戶級別支援 Pthread 需要操作系統的支援。例如，如果一個 pthread 在系統調用中阻塞，則同一進程的另一個 pthread 應該能夠在該 CPU 上運行。再舉一個例子，如果一個 pthread 改變了其進程的位址空間（例如，映射或取消映射記憶體），內核必須安排運行同一進程線程的其他 CPU 更新其硬體頁表以反映地址空間的變化。可以在沒有原子指令的情況下實現鎖 \[10\]，但這很昂貴，而且大多數操作系統都使用原子指令。如果許多 CPU 嘗試同時獲取相同的鎖，則鎖可能會很昂貴。如果一個 CPU 在其本地緩存中緩存了一個鎖，並且另一個 CPU 必須獲取該鎖，那麼更新持有該鎖的緩存行的原子指令必須將該行從一個 CPU 的緩存移動到另一個 CPU 的緩存，並且可能會使緩存行的任何其他副本失效。 從另一個 CPU 的緩存中獲取緩存行可能比從本地緩存中獲取行的成本高幾個數量級。為了避免與鎖相關的費用，許多操作系統使用無鎖的數據結構和演算法 \[6， 12\]。例如，可以實現一個鏈表，如本章開頭的那個，在清單搜索期間不需要鎖，以及一個原子指令來在清單中插入一個專案。但是，無鎖程式設計比程式設計鎖更複雜;例如，必須考慮 INSTRUCTION 和 MEMORY 的重新排序。使用鎖程式設計已經很困難，因此 xv6 避免了無鎖程式設計的額外複雜性。

### 6.10 Exercises

1. Comment out the calls toacquireandreleaseinkalloc(kernel/kalloc.c:69). This seems like it should cause problems for kernel code that callskalloc; what symptoms do you expect to see? When you run xv6, do you see these symptoms? How about when running註釋掉對 acquireandreleaseinkalloc（kernel/kalloc.c：69） 的調用。這似乎應該會給調用 kalloc 的內核代碼帶來問題;您預計會看到什麼癥狀？當您運行 xv6 時，您是否看到這些癥狀？跑步時怎麼樣

usertests? If you don’t see a problem, why not? See if you can provoke a problem by
inserting dummy loops into the critical section ofkalloc.


1. Suppose that you instead commented out the locking in kfree(after restoring locking inkalloc). What might now go wrong? Is lack of locks inkfreeless harmful than in kalloc?假設您在 kfree 中註釋掉了鎖定（在恢復鎖定 inkalloc 之後）。現在可能會出什麼問題？缺少鎖 inkfree 比 kalloc 有害嗎？
2. If two CPUs callkallocat the same time, one will have to wait for the other, which is bad for performance. Modifykalloc.cto have more parallelism, so that simultaneous calls to kallocfrom different CPUs can proceed without waiting for each other.如果兩個 CPU 同時調用 kalloc，則一個 CPU 將不得不等待另一個 CPU，這對性能不利。Modifykalloc.c具有更高的並行度，因此來自不同 CPU 的 kalloc 同時調用可以繼續進行，而無需相互等待。
3. Write a parallel program using POSIX threads, which is supported on most operating sys- tems. For example, implement a parallel hash table and measure if the number of puts/gets scales with increasing number of CPUs.使用 POSIX 線程編寫並行程式，大多數作業系統都支援該線程。例如，實現一個並行哈希表，並測量 puts/get 的數量是否隨著 CPU 數量的增加而增加。
4. Implement a subset of Pthreads in xv6. That is, implement a user-level thread library so that a user process can have more than 1 thread and arrange that these threads can run in parallel on different CPUs. Come up with a design that correctly handles a thread making a blocking system call and changing its shared address space.在 xv6 中實現 Pthreads 的子集。也就是說，實現使用者級線程庫，以便用戶進程可以有多個線程，並安排這些線程可以在不同的CPU上並行運行。想出一個設計，可以正確處理一個線程，一個阻塞系統調用並改變它的共用位址空間。

第 7 章
=====

Scheduling
==========

Any operating system is likely to run with more processes than the computer has CPUs, so a plan is needed to time-share the CPUs among the processes. Ideally the sharing would be transparent to user processes. A common approach is to provide each process with the illusion that it has its own virtual CPU bymultiplexingthe processes onto the hardware CPUs. This chapter explains how xv6 achieves this multiplexing.任何操作系統運行的進程數都可能超過計算機的CPU數，因此需要一個計劃在進程之間分時共用CPU。理想情況下，共用對用戶進程是透明的。一種常見的方法是通過將進程多路複用到硬體CPU上，為每個進程提供它擁有自己的虛擬CPU的錯覺。本章解釋了 xv6 如何實現這種多路複用。

### 7.1 Multiplexing

Xv6 multiplexes by switching each CPU from one process to another in two situations. First, xv6’s sleepandwakeupmechanism switches when a process makes a system call that blocks (has to wait for an event), typically inread,wait, orsleep. Second, xv6 periodically forces a switch to cope with processes that compute for long periods without blocking. The former are voluntary switches; the latter are called involuntary. This multiplexing creates the illusion that each process has its own CPU.Xv6 通過在兩種情況下將每個 CPU 從一個進程切換到另一個進程來實現多路複用。首先，xv6 的 sleepandwakeup機制在進程進行阻塞（必須等待事件）的系統調用時切換，通常是 inread、wait 或 sleep。其次，xv6 會定期強制 switch 處理長時間計算而不阻塞的進程。前者是自願開關;後者被稱為非自願的。這種多路復用會產生每個進程都有自己的CPU的錯覺。

Implementing multiplexing poses a few challenges. First, how to switch from one process to another? The basic idea is to save and restore CPU registers, though the fact that this cannot be expressed in C makes it tricky. Second, how to force switches in a way that is transparent to user processes? Xv6 uses the standard technique in which a hardware timer’s interrupts drive context switches. Third, all of the CPUs switch among the same set of processes, so a locking plan is necessary to avoid races. Fourth, a process’s memory and other resources must be freed when the process exits, but it cannot do all of this itself because (for example) it can’t free its own kernel stack while still using it. Fifth, each CPU of a multi-core machine must remember which process it is executing so that system calls affect the correct process’s kernel state. Finally,sleepandwakeup allow a process to give up the CPU and wait to be woken up by another process or interrupt. Care is needed to avoid races that result in the loss of wakeup notifications.實現多路復用會帶來一些挑戰。首先，如何從一個進程切換到另一個進程？基本思想是保存和恢復 CPU registers，儘管這不能用 C 表示的事實使其很棘手。其次，如何以對用戶進程透明的方式強制切換？Xv6 使用標準技術，其中硬體計時器的中斷驅動上下文切換。第三，所有 CPU 都在同一組進程之間切換，因此需要一個鎖定計劃來避免爭用。第四，當進程退出時，必須釋放進程的記憶體和其他資源，但它無法自己完成所有這些操作，因為（例如）它無法在仍然使用內核堆疊的同時釋放自己的內核堆疊。第五，多核機器的每個CPU都必須記住它正在執行的進程，以便系統調用影響正確進程的內核狀態。最後，sleepandwakeup 允許一個進程放棄 CPU 並等待被另一個進程或中斷喚醒。需要小心避免導致丟失喚醒通知的爭用。

Kernel


shell cat


user
space


kernel
space kstack
shell


kstack
cat


kstack
scheduler


save
swtch swtch restore


圖 7.1.. 從一個用戶進程切換到另一個用戶進程。在此示例中，xv6 使用一個 CPU（因此使用一個計劃程式線程）運行。

### 7.2 代碼：上下文切換

圖 7.1 概述了從一個用戶進程切換到另一個用戶進程所涉及的步驟：從使用者空間到舊進程的內核線程的陷阱（系統調用或中斷），到當前 CPU 的調度程式線程的上下文切換，到新進程的內核線程的上下文切換，以及到使用者級進程的陷阱返回。Xv6 有單獨的線程（保存的寄存器和堆棧）來執行調度器，因為調度器在任何進程的內核堆棧上執行都是不安全的：其他一些 CPU 可能會喚醒進程並運行它，在兩個不同的 CPU 上使用相同的堆疊將是一場災難。每個CPU都有一個單獨的調度程式線程，以應對多個CPU正在運行想要放棄CPU的進程的情況。在本節中，我們將研究在內核線程和調度程式線程之間切換的機制。

Switching from one thread to another involves saving the old thread’s CPU registers, and restor- ing the previously-saved registers of the new thread; the fact that the stack pointer and program counter are saved and restored means that the CPU will switch stacks and switch what code it is executing.從一個線程切換到另一個線程涉及保存舊線程的CPU寄存器，並恢復新線程之前保存的寄存器;堆疊指標和程式計數器被保存和恢復的事實意味著 CPU 將切換堆疊並切換它正在執行的代碼。

The functionswtchsaves and restores registers for a kernel thread switch.swtchdoesn’t directly know about threads; it just saves and restores sets of RISC-V registers, calledcontexts. When it is time for a process to give up the CPU, the process’s kernel thread callsswtchto save its own context and restore the scheduler’s context. Each context is contained in astruct context(kernel/proc.h:2), itself contained in a process’sstruct procor a CPU’sstruct cpu. swtchtakes two arguments:struct context_oldandstruct context_new. It saves the current registers inold, loads registers fromnew, and returns.函數 wtch保存和恢復內核線程的寄存器 switch.swtch 並不直接了解線程;它只是保存和恢復 RISC-V 寄存器集，稱為 contexts。當進程需要放棄 CPU 時，進程的內核線程會調用 swtch 來保存自己的上下文並恢復調度程式的上下文。每個上下文都包含在 astruct context（kernel/proc.h：2） 中，它本身包含在進程的 struct procor 和 CPU 的 sstruct cpu 中。swtch 接受兩個參數：struct context_old和 struct context_new。它將當前 registers 保存在 inold，從 new 載入 registers，然後返回。

Let’s follow a process throughswtchinto the scheduler. We saw in Chapter 4 that one possibil- ity at the end of an interrupt is thatusertrapcallsyield.yieldin turn callssched, which calls swtchto save the current context inp->contextand switch to the scheduler context previously saved incpu->context(kernel/proc.c:506). swtch(kernel/swtch.S:3)saves only callee-saved registers; the C compiler generates code in the caller to save caller-saved registers on the stack.swtchknows the offset of each register’s field instruct context. It does not save the program counter. Instead,swtchsaves theraregister,讓我們按照一個流程通過 swtch 進入調度器。我們在第 4 章中看到，在中斷結束時，一種可能性是 usertrapcallsyield.yield反過來調用 sched，它調用 swtch 來保存當前上下文 inp->context，並切換到之前保存在 cpu->context（kernel/proc.c：506） 中的調度程式上下文。swtch（kernel/swtch.S：3）僅保存被調用方保存的寄存器;C 編譯器在調用者中生成代碼，以將調用者保存的寄存器保存在 stack.swtch 上知道每個寄存器的 field instruct 上下文的偏移量。它不會保存程式計數器。相反，swtch會保存 theraregister、

which holds the return address from whichswtchwas called. Nowswtchrestores registers from the new context, which holds register values saved by a previousswtch. Whenswtchreturns, it returns to the instructions pointed to by the restoredraregister, that is, the instruction from which the new thread previously calledswtch. In addition, it returns on the new thread’s stack, since that’s where the restoredsppoints. In our example,schedcalledswtchto switch tocpu->context, the per-CPU scheduler context. That context was saved at the point in the past whenschedulercalledswtch(ker- nel/proc.c:466)to switch to the process that’s now giving up the CPU. When theswtchwe have been tracing returns, it returns not toschedbut toscheduler, with the stack pointer in the current CPU’s scheduler stack.，其中包含調用 swtchwas 的返回位址。nowswtch 從新上下文恢復寄存器，該上下文保存由前一個 swtch 保存的寄存器值。當 swtch 傳回時，它會返回到 restoredraregister 指向的指令，即新線程之前從中調用 swtch 的指令。此外，它還在新線程的堆疊上返回，因為這是 restoredsppoints 的位置。在我們的示例中，schedcalledswtch切換到 cpu->context，即每個 CPU 的調度程式上下文。該上下文在過去 schedulercallswtch（ker- nel/proc.c：466） 切換到現在放棄 CPU 的進程時保存。當 swtchwe 一直在跟蹤返回時，它返回的不是 tosched 而是 toscheduler，堆棧指標位於當前 CPU 的調度器堆疊中。

### 7.3 Code: Scheduling

The last section looked at the low-level details ofswtch; now let’s takeswtchas a given and examine switching from one process’s kernel thread through the scheduler to another process. The scheduler exists in the form of a special thread per CPU, each running theschedulerfunc- tion. This function is in charge of choosing which process to run next. A process that wants to give up the CPU must acquire its own process lockp->lock, release any other locks it is holding, update its own state (p->state), and then callsched. You can see this sequence in yield(kernel/proc.c:512),sleepandexit.scheddouble-checks some of those requirements (kernel/proc.c:496-501)and then checks an implication: since a lock is held, interrupts should be disabled. Finally,schedcallsswtchto save the current context inp->context and switch to the scheduler context incpu->context.swtchreturns on the scheduler’s stack as though scheduler’sswtchhad returned(kernel/proc.c:466). The scheduler continues itsforloop, finds a process to run, switches to it, and the cycle repeats. We just saw that xv6 holdsp->lockacross calls toswtch: the caller ofswtchmust already hold the lock, and control of the lock passes to the switched-to code. This arrangement is unusual: it’s more common for the thread that acquires a lock to also release it. Xv6’s context switching must break this convention becausep->lockprotects invariants on the process’sstateandcontext fields that are not true while executing inswtch. For example, ifp->lockwere not held during swtch, a different CPU might decide to run the process afteryieldhad set its state toRUNNABLE, but beforeswtchcaused it to stop using its own kernel stack. The result would be two CPUs running on the same stack, which would cause chaos. Onceyieldhas started to modify a running process’s state to make itRUNNABLE,p->lockmust remain held until the invariants are restored: the earliest correct release point is afterscheduler(running on its own stack) clearsc->proc. Similarly, onceschedulerstarts to convert aRUNNABLEprocess toRUNNING, the lock cannot be released until the process’s kernel thread is completely running (after theswtch, for example in yield). The only place a kernel thread gives up its CPU is insched, and it always switches to the same location inscheduler, which (almost) always switches to some kernel thread that previously calledsched. Thus, if one were to print out the line numbers where xv6 switches threads, one would observe the following simple pattern:(kernel/proc.c:466),(kernel/proc.c:506),最後一部分著眼於 swtch 的低級細節;現在讓我們把 SWTCHas 作為一個給定的，並檢查從一個進程的內核線程通過調度程式切換到另一個進程。調度程式以每個CPU的特殊線程的形式存在，每個線程都運行 schedulerfunc- tion。此函數負責選擇接下來要運行的進程。想要放棄 CPU 的進程必須獲取自己的進程 lockp->lock，釋放它持有的任何其他鎖，更新自己的狀態 （p->state），然後調用。你可以在 yield（kernel/proc.c：512） 中看到這個序列，sleepandexit.sched雙檢查其中一些要求 （kernel/proc.c：496-501），然後檢查一個含義：由於持有鎖，應該禁用中斷。最後，schedcallsswtch 將當前上下文保存在 p->context 中，並切換到調度器上下文 incpu->context.swtch 傳回調度器的堆疊上，就像調度器的 swtchhad 返回了 （kernel/proc.c：466） 一樣。調度程序繼續 itsforloop，找到要運行的進程，切換到該進程，然後重複迴圈。我們剛剛看到 xv6 holdsp->lockacross 調用 toswtch：調用者 ofswtch 必須已經持有鎖，並且鎖的控制權傳遞給 switched-to 代碼。這種安排很不尋常：獲取鎖的線程也會釋放它。Xv6 的上下文切換必須打破此約定，因為 p->lock 會保護進程的 stateandcontext 字段上的不變量，這些字段在執行 inswtch 時不是 true。例如，ifp->lock在切換期間沒有被保留，則不同的 CPU 可能會決定在 afteryieldhas 將其狀態設置為 RUNNABLE 之後運行該進程，但在 swtch 之前導致它停止使用自己的內核堆棧。結果將是兩個 CPU 在同一個堆疊上運行，這會導致混亂。 一旦 yield開始修改正在運行的進程的狀態以使其可RUNNABLE，p->lock必須保持保持狀態，直到不變量恢復：最早的正確釋放點是 afterscheduler（在自己的堆棧上運行） clearsc->proc。同樣，一旦scheduler開始將 aRUNNABLE進程轉換為 RUNNING，則在進程的內核線程完全運行之前（在 theswtch 之後，例如在 yield 中）才能釋放鎖。內核線程放棄其CPU的唯一位置是insched，並且它總是切換到相同的位置 inscheduler，而該位置（幾乎）總是切換到以前調用 sched 的某個內核線程。因此，如果要列印出 xv6 切換線程的行號，將觀察到以下簡單模式：（kernel/proc.c：466），（kernel/proc.c：506）、

(kernel/proc.c:466),(kernel/proc.c:506), and so on. Procedures that intentionally transfer control to each other via thread switch are sometimes referred to ascoroutines; in this example,schedand schedulerare co-routines of each other.（kernel/proc.c：466），（kernel/proc.c：506） 等。有意通過 thread switch 將控制權相互轉移的過程有時稱為 ascoroutines;在此示例中，sched和 scheduler 是彼此的協程。

There is one case when the scheduler’s call toswtchdoes not end up insched.allocproc sets the contextraregister of a new process toforkret(kernel/proc.c:524), so that its firstswtch “returns” to the start of that function.forkretexists to release thep->lock; otherwise, since the new process needs to return to user space as if returning fromfork, it could instead start at usertrapret.有一種情況是調度器的調用 toswtch 沒有以 insched.allocproc 將新進程的 contextraregister 設置為 forkret（kernel/proc.c：524），以便其第一個swtch “返回”該函數的開頭.forkretexists 以釋放 p->lock;否則，由於新進程需要像從 Fork 返回一樣返回到用戶空間，因此它可以從 Usertrapret 開始。

scheduler(kernel/proc.c:445)runs a loop: find a process to run, run it until it yields, repeat. The scheduler loops over the process table looking for a runnable process, one that hasp->state == RUNNABLE. Once it finds a process, it sets the per-CPU current process variablec->proc, marks the process asRUNNING, and then callsswtchto start running it(kernel/proc.c:461-466).scheduler（kernel/proc.c：445）運行一個迴圈：找到一個要運行的進程，運行它直到它產生，然後重複。調度程式遍歷進程表，尋找可運行的進程，即 hasp->state == RUNNABLE 的進程。找到進程後，設置每個CPU的當前進程變數 c->proc，將進程標記為 RUNNING，然後調用 swtch 開始運行它（kernel/proc.c：461-466）。

### 7.4 Code: mycpu and myproc

Xv6 often needs a pointer to the current process’sprocstructure. On a uniprocessor one could have a global variable pointing to the currentproc. This doesn’t work on a multi-core machine, since each CPU executes a different process. The way to solve this problem is to exploit the fact that each CPU has its own set of registers.Xv6 通常需要一個指向當前進程的 procstructure 的指標。在 uniprocessor 上，可以有一個指向 currentproc 的全域變數。這在多核計算機上不起作用，因為每個CPU執行不同的進程。解決這個問題的方法是利用每個CPU都有自己的registers集這一事實。

While a given CPU is executing in the kernel, xv6 ensures that the CPU’stpregister always holds the CPU’s hartid. RISC-V numbers its CPUs, giving each a uniquehartid.mycpu(ker- nel/proc.c:74)usestpto index an array ofcpustructures and return the one for the current CPU. A struct cpu(kernel/proc.h:22)holds a pointer to theprocstructure of the process currently run- ning on that CPU (if any), saved registers for the CPU’s scheduler thread, and the count of nested spinlocks needed to manage interrupt disabling.當給定的 CPU 在內核中執行時，xv6 確保 CPU 的 stpregister 始終保存 CPU 的 hartid。RISC-V 對其 CPU 進行編號，為每個 CPU 分配一個 uniquehartid.mycpu（ker- nel/proc.c：74）usestp來索引 cpustructures 陣列並返回當前 CPU 的陣列。結構體 cpu（kernel/proc.h：22） 保存一個指標，指向當前在該 CPU 上運行的進程的 procstructure（如果有的話），為 CPU 的調度程式線程保存的寄存器，以及管理中斷禁用所需的嵌套自旋鎖的數量。

Ensuring that a CPU’stpholds the CPU’s hartid is a little involved, since user code is free to modifytp.startsets thetpregister early in the CPU’s boot sequence, while still in machine mode(kernel/start.c:45).usertrapretsavestpin the trampoline page, in case user code modifies it. Finally,uservecrestores that savedtpwhen entering the kernel from user space(kernel/trampo- line.S:78). The compiler guarantees never to modifytpin kernel code. It would be more convenient if xv6 could ask the RISC-V hardware for the current hartid whenever needed, but RISC-V allows that only in machine mode, not in supervisor mode. The return values ofcpuidandmycpuare fragile: if the timer were to interrupt and cause the thread to yield and later resume execution on a different CPU, a previously returned value would no longer be correct. To avoid this problem, xv6 requires that callers disable interrupts, and only enable them after they finish using the returnedstruct cpu. The functionmyproc(kernel/proc.c:83)returns thestruct procpointer for the process that is running on the current CPU.myprocdisables interrupts, invokesmycpu, fetches the current process pointer (c->proc) out of thestruct cpu, and then enables interrupts. The return value ofmyprocis safe to use even if interrupts are enabled: if a timer interrupt moves the calling process to a different CPU, itsstruct procpointer will stay the same.確保 CPU 的 stphold CPU 的 hartid 有點複雜，因為使用者代碼可以在 CPU 啟動序列的早期自由修改tp.startsets thetpregister，同時仍處於機器模式（kernel/start.c：45）.usertrapretsavestpin 蹦床頁面，以防用戶代碼修改它。最後，uservec 會恢復從用戶空間進入內核時保存的 tp（kernel/trampo- line.S：78）。編譯器保證永遠不會修改 tpin 內核代碼。如果 xv6 可以在需要時向 RISC-V 硬體請求當前的 hartid 會更方便，但 RISC-V 只允許在機器模式下這樣做，而不允許在管理程式模式下這樣做。cpuidandmycpu 的返回值是脆弱的：如果計時器中斷並導致線程屈服，然後又在不同的 CPU 上恢復執行，則以前返回的值將不再正確。為避免此問題，xv6 要求調用方禁用中斷，並且僅在使用 returnedstruct cpu 后啟用中斷。函數myproc（kernel/proc.c：83）返回當前 CPU 上運行的進程的結構體 procpointer。myproc 禁用中斷，調用 mycpu，從結構體 cpu 中獲取當前進程指標 （c->proc），然後啟用中斷。即使啟用了中斷，myproc 的返回值也可以安全使用：如果計時器中斷將調用進程移動到不同的 CPU，則 itsstruct procpointer 將保持不變。

### 7.5 Sleep and wakeup

Scheduling and locks help conceal the actions of one thread from another, but we also need ab-
stractions that help threads intentionally interact. For example, the reader of a pipe in xv6 may need
to wait for a writing process to produce data; a parent’s call towaitmay need to wait for a child
to exit; and a process reading the disk needs to wait for the disk hardware to finish the read. The
xv6 kernel uses a mechanism called sleep and wakeup in these situations (and many others). Sleep
allows a kernel thread to wait for a specific event; another thread can call wakeup to indicate that
threads waiting for a specified event should resume. Sleep and wakeup are often calledsequence
coordinationorconditional synchronizationmechanisms.
Sleep and wakeup provide a relatively low-level synchronization interface. To motivate the
way they work in xv6, we’ll use them to build a higher-level synchronization mechanism called
asemaphore[5] that coordinates producers and consumers (xv6 does not use semaphores). A
semaphore maintains a count and provides two operations. The “V” operation (for the producer)
increments the count. The “P” operation (for the consumer) waits until the count is non-zero,
and then decrements it and returns. If there were only one producer thread and one consumer
thread, and they executed on different CPUs, and the compiler didn’t optimize too aggressively,
this implementation would be correct:


100 struct semaphore { 101 struct spinlock lock; 102 int count; 103 }; 104 105 void 106 V(struct semaphore \*s) 107 { 108 acquire(&s->lock); 109 s->count += 1; 110 release(&s->lock); 111 } 112 113 void 114 P(struct semaphore \*s) 115 { 116 while(s->count == 0) 117 ; 118 acquire(&s->lock); 119 s->count -= 1; 120 release(&s->lock); 121 }

The implementation above is expensive. If the producer acts rarely, the consumer will spend
most of its time spinning in thewhileloop hoping for a non-zero count. The consumer’s CPU
could probably find more productive work thanbusy waitingby repeatedlypollings->count.


Avoiding busy waiting requires a way for the consumer to yield the CPU and resume only afterV
increments the count.
Here’s a step in that direction, though as we will see it is not enough. Let’s imagine a pair of
calls,sleepandwakeup, that work as follows.sleep(chan)waits for an event designated by
the value ofchan, called thewait channel.sleepputs the calling process to sleep, releasing the
CPU for other work.wakeup(chan)wakes all processes that are in calls tosleepwith the same
chan(if any), causing theirsleepcalls to return. If no processes are waiting onchan,wakeup
does nothing. We can change the semaphore implementation to usesleepandwakeup(changes
highlighted in yellow):


200 void 201 V(struct semaphore \*s) 202 { 203 acquire(&s->lock); 204 s->count += 1; 205 wakeup(s); 206 release(&s->lock); 207 } 208 209 void 210 P(struct semaphore \*s) 211 { 212 while(s->count == 0) 213 sleep(s); 214 acquire(&s->lock); 215 s->count -= 1; 216 release(&s->lock); 217 }

Pnow gives up the CPU instead of spinning, which is nice. However, it turns out not to be
straightforward to designsleepandwakeupwith this interface without suffering from what is
known as thelost wake-upproblem. Suppose thatPfinds thats->count == 0on line 212. While
Pis between lines 212 and 213,Vruns on another CPU: it changess->countto be nonzero and
callswakeup, which finds no processes sleeping and thus does nothing. NowPcontinues executing
at line 213: it callssleepand goes to sleep. This causes a problem:Pis asleep waiting for aVcall
that has already happened. Unless we get lucky and the producer callsVagain, the consumer will
wait forever even though the count is non-zero.
The root of this problem is that the invariant thatPsleeps only whens->count == 0is violated
byVrunning at just the wrong moment. An incorrect way to protect the invariant would be to move
the lock acquisition (highlighted in yellow below) inPso that its check of the count and its call to
sleepare atomic:


300 void 301 V(struct semaphore \*s) 302 { 303 acquire(&s->lock);

304 s->count += 1; 305 wakeup(s); 306 release(&s->lock); 307 } 308 309 void 310 P(struct semaphore \*s) 311 { 312 acquire(&s->lock); 313 while(s->count == 0) 314 sleep(s); 315 s->count -= 1; 316 release(&s->lock); 317 }304 s->count += 1;305 次喚醒;306 發佈（&s->lock）;307 } 308 309 void 310 P（struct semaphore \*s） 311 { 312 acquire（&s->lock）; 313 while（s->count == 0） 314 sleep（s）; 315 s->count -= 1; 316 release（&s->lock）; 317 }

One might hope that this version ofPwould avoid the lost wakeup because the lock preventsV
from executing between lines 313 and 314. It does that, but it also deadlocks:Pholds the lock
while it sleeps, soVwill block forever waiting for the lock.
We’ll fix the preceding scheme by changingsleep’s interface: the caller must pass thecon-
dition locktosleepso it can release the lock after the calling process is marked as asleep and
waiting on the sleep channel. The lock will force a concurrentVto wait untilPhas finished putting
itself to sleep, so that thewakeupwill find the sleeping consumer and wake it up. Once the con-
sumer is awake againsleepreacquires the lock before returning. Our new correct sleep/wakeup
scheme is usable as follows (change highlighted in yellow):


400 void 401 V(struct semaphore \*s) 402 { 403 acquire(&s->lock); 404 s->count += 1; 405 wakeup(s); 406 release(&s->lock); 407 } 408 409 void 410 P(struct semaphore \*s) 411 { 412 acquire(&s->lock); 413 while(s->count == 0) 414 sleep(s, &s->lock); 415 s->count -= 1; 416 release(&s->lock); 417 }400 void 401 V（struct semaphore \*s） 402 { 403 acquire（&s->lock）; 404 s->count += 1; 405 喚醒（s）;406 release（&s->lock）; 407 } 408 409 void 410 P（struct semaphore \*s） 411 { 412 acquire（&s->lock）; 413 while（s->count == 0） 414 sleep（s， &s->lock）; 415 s->count -= 1; 416 release（&s->lock）; 417 }

The fact thatPholdss->lockpreventsVfrom trying to wake it up betweenP’s check of
s->countand its call tosleep. However,sleepmust releases->lockand put the consuming


process to sleep in a way that’s atomic from the point of view ofwakeup, in order to avoid lost wakeups.process 以一種從 WakeUp 的角度來看是原子的方式進入睡眠狀態，以避免丟失喚醒。

### 7.6 Code: Sleep and wakeup

Xv6’ssleep(kernel/proc.c:548)andwakeup(kernel/proc.c:579)provide the interface used in the last example above. The basic idea is to havesleepmark the current process asSLEEPINGand then callschedto release the CPU;wakeuplooks for a process sleeping on the given wait channel and marks it asRUNNABLE. Callers ofsleepandwakeupcan use any mutually convenient number as the channel. Xv6 often uses the address of a kernel data structure involved in the waiting. sleepacquiresp->lock(kernel/proc.c:559)andonly thenreleaseslk. As we’ll see, the fact thatsleepholds one or the other of these locks at all times is what prevents a concurrentwakeup (which must acquire and hold both) from acting. Now thatsleepholds justp->lock, it can put the process to sleep by recording the sleep channel, changing the process state toSLEEPING, and callingsched(kernel/proc.c:563-566). In a moment it will be clear why it’s critical thatp->lockis not released (byscheduler) until after the process is markedSLEEPING. At some point, a process will acquire the condition lock, set the condition that the sleeper is waiting for, and callwakeup(chan). It’s important thatwakeupis called while holding the condition lock^1 .wakeuploops over the process table(kernel/proc.c:579). It acquires thep->lock of each process it inspects. Whenwakeupfinds a process in stateSLEEPINGwith a matching chan, it changes that process’s state toRUNNABLE. The next timeschedulerruns, it will see that the process is ready to be run. Why do the locking rules forsleepandwakeupensure that a process that’s going to sleep won’t miss a concurrent wakeup? The going-to-sleep process holds either the condition lock or its ownp->lockor both frombeforeit checks the condition untilafterit is markedSLEEPING. The process callingwakeupholdsbothlocks inwakeup’s loop. Thus the waker either makes the condition true before the consuming thread checks the condition; or the waker’swakeupexamines the sleeping thread strictly after it has been markedSLEEPING. Thenwakeupwill see the sleeping process and wake it up (unless something else wakes it up first). Sometimes multiple processes are sleeping on the same channel; for example, more than one process reading from a pipe. A single call towakeupwill wake them all up. One of them will run first and acquire the lock thatsleepwas called with, and (in the case of pipes) read whatever data is waiting. The other processes will find that, despite being woken up, there is no data to be read. From their point of view the wakeup was “spurious,” and they must sleep again. For this reason sleepis always called inside a loop that checks the condition. No harm is done if two uses of sleep/wakeup accidentally choose the same channel: they will see spurious wakeups, but looping as described above will tolerate this problem. Much of the charm of sleep/wakeup is that it is both lightweight (no need to create special data structures to act as sleep channels) and provides a layer of indirection (callers need not know which specific process they are interacting with).Xv6 的 sleep（kernel/proc.c：548）和 wakeup（kernel/proc.c：579）提供了上面最後一個例子中使用的介面。基本思路是 havesleepmark 當前進程為 SLEEPING，然後調用 ched來釋放 CPU;wakeup查找在給定等待通道上休眠的進程，並將其標記為 RUNNABLE。sleepandwakeup 的調用者可以使用任何雙方都方便的號碼作為通道。Xv6 通常使用等待中涉及的內核數據結構的位址。sleepacquiresp->lock（kernel/proc.c：559），然後才發佈 slk。正如我們將看到的，sleep始終持有這些鎖中的一個或另一個的事實是阻止 concurrentwakeup（它必須獲取並持有兩者）起作用的原因。現在 sleephold justp->lock，它可以通過記錄 sleep 通道，將進程狀態更改為 SLEEPING，並調用 sched（kernel/proc.c：563-566） 來使進程進入休眠狀態。稍後就會清楚為什麼 p->lockis 在進程被標記為 SLEEPING 之前才被釋放 （byscheduler） 是至關重要的。在某些時候，進程將獲取條件鎖，設置休眠者正在等待的條件，然後 callwakeup（chan）。重要的是，在按住條件 lock^1 .wakeup時調用 wakeup會在進程表上迴圈 （kernel/proc.c：579）。它獲取它檢查的每個過程的 p->lock。當 wakeup 在 stateSLEEPING中找到一個具有匹配 chan 的進程時，它會將該進程的狀態更改為 RUNNABLE。下次 timescheduler運行時，它將看到該進程已準備好運行。為什麼 sleepandwakeup 的鎖定規則可以確保將要進入睡眠狀態的進程不會錯過併發喚醒？進入睡眠狀態進程在檢查條件之前持有條件鎖或它自己的p->lock或兩者，直到它被標記為 SLEEPING。 進程 callingwakeupholdsbothlocks inwakeup 的迴圈。因此，喚醒器要麼在使用線程檢查條件之前使條件為 true;或者 waker'swakeupexexamine 在被標記為 SLEEPING 之後嚴格檢查休眠線程。thenwakeup將看到休眠進程並將其喚醒（除非有其他東西先喚醒它）。有時多個進程在同一通道上休眠;例如，多個進程從管道中讀取數據。只需一個 to wakeup 的電話就會把他們全部喚醒。其中一個將首先運行並獲取調用 sleepwas 的鎖，並（在管道的情況下）讀取正在等待的任何數據。其他進程會發現，儘管被喚醒，但沒有數據可供讀取。從他們的角度來看，醒來是 「虛假的」，他們必須再次入睡。因此，sleep總是在檢查條件的迴圈中調用。如果兩次使用 sleep/wakeup 意外選擇了同一個頻道，也不會造成任何傷害：它們會看到虛假的喚醒，但如上所述的迴圈可以容忍這個問題。sleep/wakeup 的大部分魅力在於它既是輕量級的（不需要創建特殊的數據結構來充當 sleep 通道），又提供了一個間接層（調用者不需要知道他們正在與哪個特定進程交互）。

(^1) Strictly speaking it is sufficient ifwakeupmerely follows theacquire(that is, one could callwakeupafter therelease).（^1）嚴格來說，如果 wakeups 只跟隨 acquire（也就是說，可以在 release 之後調用 wakeup）就足夠了。

### 7.7 代碼：管道

A more complex example that usessleepandwakeupto synchronize producers and consumers is xv6’s implementation of pipes. We saw the interface for pipes in Chapter 1: bytes written to one end of a pipe are copied to an in-kernel buffer and then can be read from the other end of the pipe. Future chapters will examine the file descriptor support surrounding pipes, but let’s look now at the implementations ofpipewriteandpiperead. Each pipe is represented by astruct pipe, which contains alockand adatabuffer. The fieldsnreadand nwritecount the total number of bytes read from and written to the buffer. The buffer wraps around: the next byte written afterbuf\[PIPESIZE-1\]isbuf\[0\]. The counts do not wrap. This convention lets the implementation distinguish a full buffer (nwrite == nread+PIPESIZE) from an empty buffer (nwrite == nread), but it means that indexing into the buffer must usebuf\[nread % PIPESIZE\]instead of justbuf\[nread\](and similarly for nwrite). Let’s suppose that calls topipereadandpipewritehappen simultaneously on two different CPUs.pipewrite(kernel/pipe.c:77)begins by acquiring the pipe’s lock, which protects the counts, the data, and their associated invariants.piperead(kernel/pipe.c:106)then tries to acquire the lock too, but cannot. It spins inacquire(kernel/spinlock.c:22)waiting for the lock. Whilepiperead waits,pipewriteloops over the bytes being written (addr\[0..n-1\]), adding each to the pipe in turn(kernel/pipe.c:95). During this loop, it could happen that the buffer fills(kernel/pipe.c:88). In this case,pipewritecallswakeupto alert any sleeping readers to the fact that there is data waiting in the buffer and then sleeps on&pi->nwriteto wait for a reader to take some bytes out of the buffer.sleepreleases the pipe’s lock as part of puttingpipewrite’s process to sleep. pipereadnow acquires the pipe’s lock and enters its critical section: it finds thatpi->nread != pi->nwrite(kernel/pipe.c:113)(pipewritewent to sleep becausepi->nwrite == pi->nread使用 sleepandwakeup 同步生產者和消費者的更複雜的範例是 xv6 的管道實現。我們在第 1 章中看到了管道的介面：寫入管道一端的位元組被複製到內核內緩衝區，然後可以從管道的另一端讀取。後面的章節將研究圍繞管道的檔描述符支援，但現在讓我們看看pipewrite和piperead的實現。每個管道都由 astruct pipe 表示，其中包含 alock 和 adatabuffer。欄位 nread 和 nwrite 對從緩衝區讀取和寫入緩衝區的總位元組數進行計數。緩衝區回繞：下一個字節寫入 afterbuf\[PIPESIZE-1\]isbuf\[0\]。計數不換行。此約定允許實現區分完整緩衝區 （nwrite == nread+PIPESIZE） 和空緩衝區 （nwrite == nread），但這意味著索引到緩衝區必須使用buf\[nread % PIPESIZE\]而不是justbuf\[nread\]（對於nwrite也是如此）。假設對 pipereadandpipewrite的調用在兩個不同的 CPU 上同時發生.pipewrite（kernel/pipe.c：77）首先獲取管道的鎖，該鎖保護計數、數據及其關聯的不變量.piperead（kernel/pipe.c：106）然後嘗試也獲取鎖，但無法獲取。它旋轉 inacquire（kernel/spinlock.c：22） 等待鎖。當 piperead 等待時，pipewrite循環遍歷正在寫入的位元組 （addr\[0..n-1\]），依次將每個位元組添加到管道中 （kernel/pipe.c：95）。在此循環期間，可能會發生緩衝區填充 （kernel/pipe.c：88） 的情況。在這種情況下，pipewrite調用喚醒來提醒任何休眠的讀取器緩衝區中有數據正在等待，然後 sleeps on&pi->nwrite等待讀取器從緩衝區中取出一些位元組。sleep將管道的鎖作為 puttingpipewrite 進程的一部分釋放到 sleep 中。piperead現在獲取管道的鎖並進入其關鍵部分：它找到 thatpi->nread ！= pi->nwrite（kernel/pipe.c：113）（pipewrite進入睡眠狀態，因為pi->nwrite == pi->nread

*   PIPESIZE(kernel/pipe.c:88)), so it falls through to theforloop, copies data out of the pipe(ker- nel/pipe.c:120), and incrementsnreadby the number of bytes copied. That many bytes are now available for writing, sopipereadcallswakeup(kernel/pipe.c:127)to wake any sleeping writers before it returns.wakeupfinds a process sleeping on&pi->nwrite, the process that was running pipewritebut stopped when the buffer filled. It marks that process asRUNNABLE. The pipe code uses separate sleep channels for reader and writer (pi->nreadandpi->nwrite); this might make the system more efficient in the unlikely event that there are lots of readers and writers waiting for the same pipe. The pipe code sleeps inside a loop checking the sleep condition; if there are multiple readers or writers, all but the first process to wake up will see the condition is still false and sleep again.PIPESIZE（kernel/pipe.c：88）），因此它落入 for迴圈，將數據從 pipe（ker- nel/pipe.c：120） 中複製出來，並按複製的位元組數遞增 snread。現在有這麼多位元組可供寫入，sopipereadcallswakeup（kernel/pipe.c：127）在返回之前喚醒任何休眠的寫入器。wakeup找到一個休眠的進程&pi->nwrite，該進程正在運行 pipewrite，但在緩衝區填滿時停止了。它將該進程標記為 RUNNABLE。管道代碼對讀取器和寫入器使用單獨的休眠通道 （pi->nreadandpi->nwrite）;這可能會使系統在有大量讀取器和寫入器等待同一管道的不太可能的情況下更加高效。管道代碼在檢查休眠條件的迴圈中休眠;如果有多個讀取器或寫入器，則除了第一個喚醒的進程之外，所有進程都將看到條件仍為 FALSE 並再次休眠。

### 7.8 代碼：Wait、exit 和 kill

sleepandwakeupcan be used for many kinds of waiting. An interesting example, introduced in Chapter 1, is the interaction between a child’sexitand its parent’swait. At the time of the child’s death, the parent may already be sleeping inwait, or may be doing something else; in the latter case, a subsequent call towaitmust observe the child’s death, perhaps long after it callssleepAndwakeup可用於多種類型的等待。第 1 章中介紹的一個有趣的例子是 child'sexits 與其 parent's wait之間的交互。在孩子去世時，父母可能已經在等待睡覺，或者可能正在做其他事情;在後一種情況下，後續調用towait必須觀察孩子的死亡，可能在它調用

exit. The way that xv6 records the child’s demise untilwaitobserves it is forexitto put the caller into theZOMBIEstate, where it stays until the parent’swaitnotices it, changes the child’s state toUNUSED, copies the child’s exit status, and returns the child’s process ID to the parent. If the parent exits before the child, the parent gives the child to theinitprocess, which perpetually callswait; thus every child has a parent to clean up after it. A challenge is to avoid races and deadlock between simultaneous parent and childwaitandexit, as well as simultaneousexit andexit.退出。xv6 記錄子進程的消亡直到等待觀察的方式是 forexit將調用者置於 ZOMBIE 狀態，它一直停留在該狀態中，直到父進程的 swait注意到它，將子進程的狀態更改為 UNUSED，複製子進程的退出狀態，並將子進程 ID 返回給父進程。如果父級在子級之前退出，則父級將子級交給initprocess，initprocess永久調用wait;因此，每個孩子都有一個父母要清理。一個挑戰是避免同時 parent 和 childwaitandexit 之間以及同時 exit 和 exit 之間的競爭和僵局。

waitstarts by acquiringwait\_lock(kernel/proc.c:391), which acts as the condition lock that helps ensure thatwaitdoesn’t miss awakeupfrom an exiting child. Thenwaitscans the process table. If it finds a child inZOMBIEstate, it frees that child’s resources and itsprocstructure, copies the child’s exit status to the address supplied towait(if it is not 0), and returns the child’s process ID. Ifwaitfinds children but none have exited, it callssleepto wait for any of them to exit(kernel/proc.c:433), then scans again.waitoften holds two locks,wait\_lockand some process’spp->lock; the deadlock-avoiding order is firstwait\_lockand thenpp->lock.wait啟動acquiringwait\_lock（kernel/proc.c：391），它充當條件鎖，幫助確保 Wait不會錯過來自退出的子物件的 awakeUp。Thenwait掃描進程表。如果它在 ZOMBIE 狀態中找到一個子進程，它會釋放該子進程的資源和它的 proc結構，將子進程的退出狀態複製到提供給 wait的位址（如果它不是 0），並返回子進程的進程 ID。如果wait找到子進程但沒有退出，它會調用 sleep 等待其中任何一個退出（kernel/proc.c：433），然後再次掃描。wait\_lockand某個進程的 spp->lock;避免死鎖的順序是 firstwait\_lockand thenpp->lock。

exit(kernel/proc.c:347)records the exit status, frees some resources, callsreparentto give its children to theinitprocess, wakes up the parent in case it is inwait, marks the caller as a zombie, and permanently yields the CPU.exitholds bothwait\_lockandp->lockduring this sequence. It holdswait\_lockbecause it’s the condition lock for thewakeup(p->parent), preventing a parent inwaitfrom losing the wakeup.exitmust holdp->lockfor this sequence also, to prevent a parent inwaitfrom seeing that the child is in stateZOMBIEbefore the child has finally calledswtch.exitacquires these locks in the same order aswaitto avoid deadlock.exit（kernel/proc.c：347）記錄退出狀態，釋放一些資源，調用 reparent將其子進程提供給init進程，在父進程處於 inwait 狀態時喚醒父進程，將調用者標記為殭屍，並在此過程中永久產生 CPU.exitholds bothwait\_lockandp->lock。它holdswait\_lockbecause它是 wakeup（p->parent） 的條件鎖，防止父 inwaits 丟失 wakeup.exit必須持有p->lock對於此序列，以防止父 inwait在子 inwait最終調用 swtch.exit之前看到子 inwaits 處於狀態 ZOMBIE，以與 wait相同的順序獲取這些鎖以避免死鎖。

It may look incorrect forexitto wake up the parent before setting its state toZOMBIE, but that is safe: althoughwakeupmay cause the parent to run, the loop inwaitcannot examine the child until the child’sp->lockis released byscheduler, sowaitcan’t look at the exiting process until well afterexithas set its state toZOMBIE(kernel/proc.c:379).在將狀態設置為 ZOMBIE 之前喚醒父進程可能看起來不正確，但這是安全的：儘管 wakeup 可能會導致父進程運行，但迴圈 inwait無法檢查子進程，直到調度器釋放 child『sp->lock，因此在 good afterexit將其狀態設置為 ZOMBIE（kernel/proc.c：379） 之前無法查看退出進程。

Whileexitallows a process to terminate itself,kill(kernel/proc.c:598)lets one process re- quest that another terminate. It would be too complex forkillto directly destroy the victim process, since the victim might be executing on another CPU, perhaps in the middle of a sensitive sequence of updates to kernel data structures. Thuskilldoes very little: it just sets the victim’s p->killedand, if it is sleeping, wakes it up. Eventually the victim will enter or leave the kernel, at which point code inusertrapwill callexitifp->killedis set (it checks by callingkilled (kernel/proc.c:627)). If the victim is running in user space, it will soon enter the kernel by making a system call or because the timer (or some other device) interrupts.Exit允許一個進程終止自身，而kill（kernel/proc.c：598）允許一個進程重新請求另一個進程終止。kill直接銷毀受害者進程太複雜了，因為受害者可能正在另一個 CPU 上執行，可能正在對內核數據結構進行敏感的更新序列。因此kill的作用很小：它只是設置受害者的 p->killed，如果它正在睡覺，則將其喚醒。最終，受害者將進入或離開內核，此時 inusertrap 中的代碼將調用 exitifp->killed（它通過調用 killed （kernel/proc.c：627）） 進行檢查）。如果受害者在用戶空間中運行，它將很快通過進行系統調用或因為計時器（或其他設備）中斷而進入內核。

If the victim process is insleep,kill’s call towakeupwill cause the victim to return from sleep. This is potentially dangerous because the condition being waited for for may not be true. However, xv6 calls tosleepare always wrapped in awhileloop that re-tests the condition after sleepreturns. Some calls tosleepalso testp->killedin the loop, and abandon the current activity if it is set. This is only done when such abandonment would be correct. For example, the pipe read and write code(kernel/pipe.c:84)returns if the killed flag is set; eventually the code will return back to trap, which will again checkp->killedand exit.如果受害者進程處於睡眠狀態，kill 的 call towakeup 將導致受害者從睡眠中返回。這具有潛在危險，因為正在等待的條件可能不是 true。但是，xv6 調用 tosleep總是包裝在 awhile迴圈中，該迴圈在 sleepreturns 後重新測試條件。一些調用 tosleep還會在迴圈中 testp->killed，如果設置了當前 activity，則放棄當前 activity。僅當此類放棄是正確的時，才會執行此操作。例如，如果設置了 killed 標誌，則 pipe read and write code（kernel/pipe.c：84） 傳回;最終，代碼將返回給 trap，trap 將再次檢查 p->killed並退出。

Some xv6sleeploops do not checkp->killedbecause the code is in the middle of a multi- step system call that should be atomic. The virtio driver(kernel/virtio\_disk.c:285)is an example: it一些 xv6sleeploops 不檢查 p->killed，因為代碼處於多步驟系統調用的中間，應該是原子的。virtio 驅動程式（kernel/virtio\_disk.c：285）就是一個例子：它

does not checkp->killedbecause a disk operation may be one of a set of writes that are all needed in order for the file system to be left in a correct state. A process that is killed while waiting for disk I/O won’t exit until it completes the current system call andusertrapsees the killed flag.does not checkp->killed，因為磁碟操作可能是使文件系統保持正確狀態所需的一組寫入之一。在等待磁碟 I/O 時被終止的進程不會退出，直到它完成當前系統調用並且 usertrap 看到 killed 標誌。

### 7.9 Process Locking

The lock associated with each process (p->lock) is the most complex lock in xv6. A simple way to think aboutp->lockis that it must be held while reading or writing any of the following struct procfields:p->state,p->chan,p->killed,p->xstate, andp->pid. These fields can be used by other processes, or by scheduler threads on other CPUs, so it’s natural that they must be protected by a lock. However, most uses ofp->lockare protecting higher-level aspects of xv6’s process data struc- tures and algorithms. Here’s the full set of things thatp->lockdoes:與每個進程關聯的鎖 （p->lock） 是 xv6 中最複雜的鎖。一種簡單的思考 p->lock 的方法是，在讀取或寫入以下任何結構體 procfields 時必須持有它：p->state、p->chan、p->killed、p->xstate 和 p->pid。這些欄位可以被其他進程使用，也可以被其他 CPU 上的調度程式線程使用，因此它們必須由鎖保護是很自然的。然而，大多數 ofp->lock 的使用都是保護 xv6 的流程數據結構和演算法的更高級別方面。以下是 p->lock 所做的全套操作：

*   Along withp->state, it prevents races in allocatingproc\[\]slots for new processes.它與 p->state 一起，可以防止在為新進程分配 proc\[\]slot 時發生爭用。
*   It conceals a process from view while it is being created or destroyed.它在創建或銷毀進程時將其隱藏起來。
*   It prevents a parent’swaitfrom collecting a process that has set its state toZOMBIEbut has not yet yielded the CPU.它可以防止父級的 wait' 收集已將其狀態設置為 ZOMBIE 但尚未產生 CPU 的進程。
*   It prevents another CPU’s scheduler from deciding to run a yielding process after it sets its state toRUNNABLEbut before it finishesswtch.它可以防止另一個 CPU 的調度程式在將狀態設置為 RUNNABLE 之後但在完成切換之前決定運行讓步進程。
*   It ensures that only one CPU’s scheduler decides to run aRUNNABLEprocesses.它確保只有一個 CPU 的調度程式決定運行 aRUNNABLE進程。
*   It prevents a timer interrupt from causing a process to yield while it is inswtch.它可以防止計時器中斷導致進程在inswtch時產生。
*   Along with the condition lock, it helps preventwakeupfrom overlooking a process that is callingsleepbut has not finished yielding the CPU.與條件鎖定一起，它還有助於防止 wakeup忽略正在調用 sleep 但尚未完成生成 CPU 的進程。
*   It prevents the victim process ofkillfrom exiting and perhaps being re-allocated between kill’s check ofp->pidand settingp->killed.它可以防止 killing 的受害者進程退出，並可能在 kill 的檢查 ofp->pid和 settingp->killed 之間重新分配。
*   It makeskill’s check and write ofp->stateatomic.它使 skill 的 check 和 write ofp->stateatomic 的

Thep->parentfield is protected by the global lockwait\_lockrather than byp->lock. Only a process’s parent modifiesp->parent, though the field is read both by the process it- self and by other processes searching for their children. The purpose ofwait\_lockis to act as the condition lock whenwaitsleeps waiting for any child to exit. An exiting child holds either wait\_lockorp->lockuntil after it has set its state toZOMBIE, woken up its parent, and yielded the CPU.wait\_lockalso serializes concurrentexits by a parent and child, so that theinit process (which inherits the child) is guaranteed to be woken up from itswait.wait\_lockis a global lock rather than a per-process lock in each parent, because, until a process acquires it, it cannot know who its parent is.p->parentfield 受全域lockwait\_lockrather保護，而不是 byp->lock。只有進程的父進程 modifiesp->parent，儘管該欄位同時被進程 it- self 和其他搜索其子進程的進程讀取。其目的ofwait\_lockis充當 waitsleeps 等待任何子項退出時的條件鎖。退出的子進程持有 wait\_lockorp->lock，直到它將其狀態設置為 ZOMBIE，喚醒其父進程，併產生父子進程序列化 concurrentexits 的CPU.wait\_lockalso，以便保證 init 進程（繼承子進程）從itswait.wait\_lockis全域鎖中喚醒，而不是從每個父進程中的每個進程鎖中喚醒。 因為，在進程獲取它之前，它無法知道它的父進程是誰。

### 7.10 Real world

The xv6 scheduler implements a simple scheduling policy, which runs each process in turn. This policy is calledround robin. Real operating systems implement more sophisticated policies that, for example, allow processes to have priorities. The idea is that a runnable high-priority process will be preferred by the scheduler over a runnable low-priority process. These policies can become complex quickly because there are often competing goals: for example, the operating system might also want to guarantee fairness and high throughput. In addition, complex policies may lead to unintended interactions such aspriority inversionandconvoys. Priority inversion can happen when a low-priority and high-priority process both use a particular lock, which when acquired by the low-priority process can prevent the high-priority process from making progress. A long convoy of waiting processes can form when many high-priority processes are waiting for a low-priority process that acquires a shared lock; once a convoy has formed it can persist for long time. To avoid these kinds of problems additional mechanisms are necessary in sophisticated schedulers. sleepandwakeupare a simple and effective synchronization method, but there are many others. The first challenge in all of them is to avoid the “lost wakeups” problem we saw at the beginning of the chapter. The original Unix kernel’ssleepsimply disabled interrupts, which suf- ficed because Unix ran on a single-CPU system. Because xv6 runs on multiprocessors, it adds an explicit lock tosleep. FreeBSD’smsleeptakes the same approach. Plan 9’ssleepuses a callback function that runs with the scheduling lock held just before going to sleep; the function serves as a last-minute check of the sleep condition, to avoid lost wakeups. The Linux kernel’s sleepuses an explicit process queue, called a wait queue, instead of a wait channel; the queue has its own internal lock. Scanning the entire set of processes inwakeupis inefficient. A better solution is to replace thechanin bothsleepandwakeupwith a data structure that holds a list of processes sleeping on that structure, such as Linux’s wait queue. Plan 9’ssleepandwakeupcall that structure a rendezvous point. Many thread libraries refer to the same structure as a condition variable; in that context, the operationssleepandwakeupare calledwaitandsignal. All of these mechanisms share the same flavor: the sleep condition is protected by some kind of lock dropped atomically during sleep. The implementation ofwakeupwakes up all processes that are waiting on a particular chan- nel, and it might be the case that many processes are waiting for that particular channel. The operating system will schedule all these processes and they will race to check the sleep condition. Processes that behave in this way are sometimes called athundering herd, and it is best avoided. Most condition variables have two primitives forwakeup:signal, which wakes up one process, andbroadcast, which wakes up all waiting processes. Semaphores are often used for synchronization. The count typically corresponds to something like the number of bytes available in a pipe buffer or the number of zombie children that a process has. Using an explicit count as part of the abstraction avoids the “lost wakeup” problem: there is an explicit count of the number of wakeups that have occurred. The count also avoids the spurious wakeup and thundering herd problems. Terminating processes and cleaning them up introduces much complexity in xv6. In most op- erating systems it is even more complex, because, for example, the victim process may be deepxv6 調度程序實現了一個簡單的調度策略，該策略依次運行每個進程。此策略稱為 round robin。實際操作系統實施更複雜的策略，例如，允許進程具有優先順序。這個想法是，調度程式將優先於可運行的低優先順序進程。這些策略可能很快就會變得複雜，因為通常存在相互競爭的目標：例如，操作系統可能還希望保證公平性和高輸送量。此外，複雜的策略可能會導致意外的交互，例如優先順序倒置和convoys。當低優先順序和高優先順序進程都使用特定鎖時，可能會發生優先順序倒置，當低優先順序進程獲取該鎖時，可能會阻止高優先順序進程取得進展。當許多高優先順序進程正在等待獲取共用鎖的低優先順序進程時，可能會形成一個長長的等待進程保護隊;一旦形成護航，它就可以持續很長時間。為了避免這些類型的問題，在複雜的 scheduler 中需要額外的機制。sleepandwakeup是一種簡單而有效的同步方法，但還有許多其他方法。所有這些挑戰的第一個挑戰是避免我們在本章開頭看到的 「lost wakeups」 問題。最初的 Unix 內核的 sleep只是禁用了中斷，這很有效，因為 Unix 運行在單 CPU 系統上。因為 xv6 在多處理器上運行，所以它添加了一個顯式的 sleep 鎖。FreeBSD 的 smsleep 採用相同的方法。Plan 9'ssleep使用一個回調函數，該函數在進入睡眠狀態之前持有調度鎖的情況下運行;該函數用作睡眠條件的最後一分鐘檢查，以避免丟失喚醒。 Linux 內核的 sleeps 使用顯式進程佇列，稱為 wait queue，而不是 wait channel;佇列有自己的內部鎖。在 wakeup 中掃描整個進程集效率低下。更好的解決方案是將 thechanin both sleepandwakeup 替換為一個數據結構，該數據結構包含休眠在該結構上的進程清單，例如 Linux 的等待佇列。Plan 9'ssleepandwakeup調用該結構的集合點。許多線程庫將相同的結構引用為條件變數;在該上下文中，操作 SleepAndWakeUp 稱為 WaitAndSignal。所有這些機制都有相同的風格： 睡眠條件由某種在睡眠期間原子丟棄的鎖保護。wakeup的實現喚醒了所有正在等待特定通道的進程，並且可能有許多進程正在等待該特定通道。操作系統將安排所有這些進程，並且它們將爭分奪秒地檢查睡眠條件。以這種方式表現的進程有時稱為 athundering herid，最好避免。大多數條件變數有兩個原語 forwakeup：signal，它喚醒一個進程，和 broadcast，它喚醒所有等待的進程。信號量通常用於同步。計數通常對應於管道緩衝區中可用的位元元組數或進程具有的 zombie children 數。使用顯式計數作為抽象的一部分可以避免「丟失喚醒」問題：存在已發生的喚醒次數的顯式計數。計數還避免了虛假的喚醒和雷鳴般的羊群問題。終止進程並清理它們在 xv6 中會帶來很多複雜性。在大多數操作系統中，它甚至更加複雜，因為，例如，受害者過程可能很深

inside the kernel sleeping, and unwinding its stack requires care, since each function on the call stack may need to do some clean-up. Some languages help out by providing an exception mecha- nism, but not C. Furthermore, there are other events that can cause a sleeping process to be woken up, even though the event it is waiting for has not happened yet. For example, when a Unix process is sleeping, another process may send asignalto it. In this case, the process will return from the interrupted system call with the value -1 and with the error code set to EINTR. The application can check for these values and decide what to do. Xv6 doesn’t support signals and this complexity doesn’t arise. Xv6’s support forkillis not entirely satisfactory: there are sleep loops which probably should check forp->killed. A related problem is that, even forsleeploops that checkp->killed, there is a race betweensleepandkill; the latter may setp->killedand try to wake up the victim just after the victim’s loop checksp->killedbut before it callssleep. If this problem occurs, the victim won’t notice thep->killeduntil the condition it is waiting for occurs. This may be quite a bit later or even never (e.g., if the victim is waiting for input from the console, but the user doesn’t type any input). A real operating system would find freeprocstructures with an explicit free list in constant time instead of the linear-time search inallocproc; xv6 uses the linear scan for simplicity.在內核內部休眠並展開其堆疊需要小心，因為調用堆疊上的每個函數都可能需要進行一些清理。一些語言通過提供例外 mecha- nism 而不是 C 來提供説明。此外，還有其他事件可能導致休眠進程被喚醒，即使它正在等待的事件尚未發生。例如，當一個 Unix 進程處於休眠狀態時，另一個進程可能會向它發送一個信號。在這種情況下，進程將從中斷的系統調用中返回值為 -1 且錯誤代碼設置為 EINTR。應用程式可以檢查這些值並決定要做什麼。Xv6 不支援信號，因此不會出現這種複雜性。Xv6 對 kill 的支援並不完全令人滿意：有些睡眠迴圈可能應該檢查 forp->killed。一個相關的問題是，即使 forsleeploops 檢查 p->killed，sleepandkill 之間也存在競爭;後者可能會設置p->killed並嘗試在受害者的迴圈檢查之後喚醒受害者sp->killed，但在它調用睡眠之前。如果出現此問題，受害者不會注意到 p->killed，直到它正在等待的條件發生。這可能是很晚的事，甚至永遠不會（例如，如果受害者正在等待來自控制台的輸入，但使用者沒有輸入任何輸入）。一個真實的操作系統會在恆定時間內找到具有顯式空閒清單的 freeprocstructures，而不是線性時間搜索 inallocproc;為了簡單起見，XV6 使用線性掃描。

### 7.11 Exercises

1. Implement semaphores in xv6 without usingsleepandwakeup(but it is OK to use spin locks). Choose a few of xv6’s uses of sleep and wakeup and replace them with semaphores. Judge the result.在 xv6 中實現信號量，而不使用 sleepandwakeup（但可以使用旋轉鎖）。選擇 xv6 的一些 sleep 和 wakeup 用法，並將它們替換為信號量。判斷結果。
2. Fix the race mentioned above betweenkillandsleep, so that akillthat occurs after the victim’s sleep loop checksp->killedbut before it callssleepresults in the victim abandoning the current system call.修復上面提到的 killandsleep 之間的爭用，使得 akill這發生在受害者的睡眠循環之後 checksp->killed，但在調用 sleep之前會導致受害者放棄當前的系統調用。
3. Design a plan so that every sleep loop checksp->killedso that, for example, a process that is in the virtio driver can return quickly from the while loop if it is killed by another process.設計一個計劃，以便每個 sleep loop checksp->killed，例如，如果 virtio 驅動程式中的某個進程被另一個進程終止，則可以從 while 迴圈中快速返回。
4. Modify xv6 to use only one context switch when switching from one process’s kernel thread to another, rather than switching through the scheduler thread. The yielding thread will need to select the next thread itself and callswtch. The challenges will be to prevent multiple CPUs from executing the same thread accidentally; to get the locking right; and to avoid deadlocks.修改 xv6 以在從一個進程的內核線程切換到另一個進程的內核線程時僅使用一個上下文切換，而不是通過調度程式線程切換。生成線程需要選擇下一個線程本身並調用 wtch。挑戰將是防止多個 CPU 意外執行同一線程;正確鎖定;並避免死鎖。
5. Modify xv6’sschedulerto use the RISC-VWFI(wait for interrupt) instruction when no processes are runnable. Try to ensure that, any time there are runnable processes waiting to run, no CPUs are pausing inWFI.修改 xv6 的 scheduler，以便在沒有進程可運行時使用 RISC-VWFI（wait for interrupt） 指令。嘗試確保，每當有可運行的進程等待運行時，WFI 中沒有 CPU 暫停。

第八章
===

檔案系統
====

The purpose of a file system is to organize and store data. File systems typically support sharing of data among users and applications, as well aspersistenceso that data is still available after a reboot. The xv6 file system provides Unix-like files, directories, and pathnames (see Chapter 1), and stores its data on a virtio disk for persistence. The file system addresses several challenges:文件系統的目的是組織和存儲數據。檔案系統通常支援在使用者和應用程式之間共享數據，以及持久性，以便數據在重新啟動后仍然可用。xv6 文件系統提供類似 Unix 的文件、目錄和路徑名（參見第 1 章），並將其數據存儲在 virtio 磁碟上以實現持久性。該檔案系統解決了幾個挑戰：

*   The file system needs on-disk data structures to represent the tree of named directories and files, to record the identities of the blocks that hold each file’s content, and to record which areas of the disk are free.文件系統需要磁碟上的數據結構來表示命名目錄和檔的樹，記錄保存每個檔內容的塊的標識，並記錄磁碟的哪些區域是空閒的。
*   The file system must supportcrash recovery. That is, if a crash (e.g., power failure) occurs, the file system must still work correctly after a restart. The risk is that a crash might interrupt a sequence of updates and leave inconsistent on-disk data structures (e.g., a block that is both used in a file and marked free).檔系統必須支持崩潰恢復。也就是說，如果發生崩潰（例如，電源故障），文件系統在重啟后仍必須正常工作。風險在於崩潰可能會中斷一系列更新並留下不一致的磁碟數據結構（例如，一個既在檔中使用又標記為free的塊）。
*   Different processes may operate on the file system at the same time, so the file-system code must coordinate to maintain invariants.不同的進程可以同時在文件系統上運行，因此檔系統代碼必須協調以保持不變性。
*   Accessing a disk is orders of magnitude slower than accessing memory, so the file system must maintain an in-memory cache of popular blocks.訪問磁碟比訪問記憶體慢幾個數量級，因此檔系統必須維護常用塊的記憶體緩存。

The rest of this chapter explains how xv6 addresses these challenges.


### 8.1 概述

The xv6 file system implementation is organized in seven layers, shown in Figure 8.1. The disk layer reads and writes blocks on an virtio hard drive. The buffer cache layer caches disk blocks and synchronizes access to them, making sure that only one kernel process at a time can modify the data stored in any particular block. The logging layer allows higher layers to wrap updates to several blocks in atransaction, and ensures that the blocks are updated atomically in the face of crashes (i.e., all of them are updated or none). The inode layer provides individual files, eachxv6 文件系統實現分為 7 層，如圖 8.1 所示。磁碟層在 virtio 硬碟驅動器上讀取和寫入塊。緩衝區緩存層緩存磁碟塊並同步對它們的訪問，確保一次只有一個內核進程可以修改存儲在任何特定塊中的數據。日誌層允許更高層將更新包裝到事務中的多個區塊，並確保這些區塊在崩潰時被原子更新（即，所有區塊都被更新或沒有更新）。inode 層提供單獨的檔，每個

Directory


Inode


Logging


Buffer cache


Pathname


File descriptor


(^)磁碟^ 圖 8.1： xv6 檔案系統的層。表示為 aninode，具有唯一的 i 編號和一些保存文件數據的塊。目錄層將每個目錄實現為一種特殊類型的 inode，其內容是一系列目錄條目，每個目錄條目都包含一個檔名和 i 編號。pathname 層提供分層路徑名，如 /usr/rtm/xv6/fs.c，並通過遞歸查找來解析它們。檔描述符層使用檔系統介面抽象出許多 Unix 資源（例如，管道、設備、檔等），從而簡化了應用程式程式師的工作。傳統上，磁碟硬體將磁碟上的數據顯示為512位元組塊（也稱為扇區）的編號序列：扇區0是前512位元組，扇區1是下一個字節，依此類推。操作系統用於其文件系統的塊大小可能與磁碟使用的扇區大小不同，但通常塊大小是扇區大小的倍數。Xv6 保存已讀入記憶體的 typestruct buf（kernel/buf.h：1） 物件中的塊副本。存儲在此結構中的數據有時與磁碟不同步：它可能尚未從磁碟讀入（磁碟正在處理它，但尚未返回扇區的內容），或者它可能已被軟體更新但尚未寫入磁碟。文件系統必須有一個計劃，用於確定它在磁碟上的存儲 inode 和內容塊的位置。為此，xv6 將磁碟劃分為幾個部分，如圖 8.2 所示。檔系統不使用塊 0（它保存引導扇區）。區塊 1 稱為超級區塊;它包含有關文件系統的元數據（以塊為單位的文件系統大小、數據塊數、索引節點數和日誌中的塊數）。 從 2 開始的塊保存對數。日誌之後是 inode，每個數據塊有多個 inode。在這些之後是 bitmap 塊，跟蹤哪些數據塊正在使用。其餘塊是數據塊;每個 Cookie 要麼在 Bitmap 塊中標記為 free，要麼保存檔或目錄的內容。超級塊由一個名為 mkfs 的單獨程式填充，該程式構建一個初始文件系統。本章的其餘部分將討論每個層，從緩衝區緩存開始。注意在較低層精心選擇的抽象可以簡化較高層的設計的情況。

0


bootsuper log inodes bit map data


1


.... data


2


Figure 8.2: Structure of the xv6 file system.


### 8.2 Buffer cache layer

緩衝區緩存有兩個工作：（1） 同步對磁碟塊的訪問，以確保記憶體中只有一個塊的副本，並且一次只有一個內核線程使用該副本;（2） 快取流行的塊，這樣它們就不需要從慢速磁盤中重新讀取。代碼為 inbio.c。緩衝區緩存導出的主介面由 breadandbwrite 組成;前者獲取 abuf包含可以在記憶體中讀取或修改的塊的副本，後者將修改後的緩衝區寫入磁碟上的相應塊。內核線程必須通過調用 brelsewhen 釋放緩衝區。緩衝區緩存使用每個緩衝區的休眠鎖來確保一次只有一個線程使用每個緩衝區（因此每個磁碟塊）;bread 會返回一個鎖定的緩衝區，而 brelse會釋放該鎖。我們回到緩衝區緩存。緩衝區緩存具有固定數量的緩衝區來保存磁碟塊，這意味著如果檔系統請求緩存中尚未存在的塊，緩衝區緩存必須回收當前保存其他塊的緩衝區。緩衝區緩存為新塊回收最近使用最少的緩衝區。假設是最近最少使用的緩衝區是最不可能很快再次使用的緩衝區。

### 8.3 Code: Buffer cache

緩衝區緩存是緩衝區的雙向連結清單。調用 bymain（kernel/- main.c：27） 的函數binit 使用靜態 arraybuf（kernel/bio.c：43-52） 中的 NBUFbuffers 初始化清單。對緩衝區緩存的所有其他訪問都引用鏈表 viabcache.head，而不是 thebufarray。緩衝區有兩個與之關聯的狀態欄位。fieldvalid表示緩衝區包含塊的副本。欄位 disk 表示緩衝區內容已交給磁碟，磁碟可能會更改緩衝區（例如，將數據從磁碟寫入 data）。bread（kernel/bio.c：93）調用bget來獲取給定扇區的緩衝區（kernel/bio.c：97）。如果需要從磁碟讀取緩衝區，breadcallsvirtio\_disk\_rwto在返回緩衝區之前執行此操作。bget（kernel/bio.c：59）掃描緩衝區清單，查找具有給定設備和扇區號的緩衝區 （kernel/bio.c：65-73）。如果存在這樣的緩衝區，bget獲取 buffer.bget 的睡眠鎖，然後返回鎖定的緩衝區。如果給定扇區沒有緩存的緩衝區，bget必須創建一個，可能會重用保存不同扇區的緩衝區。它再次掃描緩衝區清單，查找未使用的緩衝區 （b->refcnt = 0）;可以使用任何這樣的緩衝區。bget編輯緩衝區元數據以記錄新的設備和扇區號，並獲取其睡眠鎖。請注意，assignmentb->valid = 0 確保 bread 將從磁碟讀取塊數據，而不是錯誤地使用緩衝區的

以前的內容。重要的是每個磁碟扇區最多有一個緩存的緩衝區，以確保讀者看到寫入，並且因為文件系統在緩衝區上使用鎖進行 synchronization.bget.bget 通過保持 thebache.lock bcache.lock來確保這種不變性，從第一個循環檢查塊是否被緩存到第二個循環的聲明，該塊現在被緩存（通過設置 dev，blockno， andrefcnt） 的這會導致檢查塊是否存在以及（如果不存在）用於保存塊的緩衝區的指定是原子的。在 bcache.lockcritical 部分之外獲取緩衝區的休眠鎖是安全的，因為非 zerob->refcnt 可以防止緩衝區被重新用於不同的磁碟塊。sleep-lock 保護塊緩衝內容的讀取和寫入，而 bcache.lock 保護有關緩存哪些塊的資訊。如果所有緩衝區都繁忙，則太多進程同時執行文件系統調用;bgetpanics 的更優雅的回應可能是休眠，直到緩衝區空閒，儘管那時可能會發生死鎖。一旦bread讀取了磁碟（如果需要）並將緩衝區返回給其調用者，則調用者獨佔使用緩衝區，並且可以讀取或寫入數據位元組。如果調用者確實修改了緩衝區，它必須在釋放 buffer.bwrite （kernel/bio.c：107） 之前調用 bwrite將更改的數據寫入磁碟callsvirtio\_disk\_rwto與磁碟硬體通信。當調用方完成緩衝區時，它必須調用 brelse來釋放它。（namebrelse 是 b-release 的縮寫，很神秘，但值得學習：它起源於 Unix，也用於 BSD、Linux 和 Solaris。brelse（kernel/bio.c：117）釋放 sleep-lock 並將緩衝區移動到鏈表的前面（kernel/bio.c：128-133）。移動緩衝區會導致清單按緩衝區的最近使用時間排序（意味著已釋放）：清單中的第一個緩衝區是最近使用的緩衝區，最後一個緩衝區是最近使用最少的緩衝區。兩個迴圈 inbget 利用了這一點：在最壞的情況下，對現有緩衝區的掃描必須處理整個清單，但是當有良好的引用位置時，首先檢查最近使用的緩衝區（啟動 atbcache.head 和 followingnextpointers）將減少掃描時間。選擇要重用的緩衝區的掃描通過向後掃描來選擇最近最少使用的緩衝區 （followingprevpointers）。

### 8.4 Logging layer

檔系統設計中最有趣的問題之一是崩潰恢復。出現此問題的原因是，許多文件系統操作涉及對磁碟的多次寫入，並且寫入子集之後的崩潰可能會使磁碟上的文件系統處於不一致的狀態。例如，假設在檔截斷期間發生崩潰（將檔的長度設置為零並釋放其內容塊）。根據磁碟寫入的順序，崩潰可能會使 inode 引用標記為free的內容塊，也可能留下已分配但未引用的內容塊。後者相對良性，但引用已釋放塊的 inode 可能會在重啟后導致嚴重問題。重啟后，內核可能會將該塊分配給另一個文件，現在我們有兩個不同的檔無意中指向同一個塊。如果 xv6 支援多個使用者，則這種情況可能是安全問題，因為舊檔的擁有者將能夠讀取

並在其他用戶擁有的新檔中寫入塊。Xv6 通過一種簡單的紀錄記錄形式解決了檔案系統操作期間的崩潰問題。xv6 系統調用不會直接寫入磁碟上的文件系統數據結構。相反，它將它希望進行的所有磁碟寫入的描述放在磁碟上 alog.一旦系統調用記錄了它的所有寫入，它就會向磁碟寫入一個specialcommitrecord，指示日誌包含完整的操作。此時，系統調用將寫入複製到磁碟上的檔系統數據結構。完成這些寫入后，系統調用將擦除磁碟上的日誌。如果系統崩潰並重新啟動，則檔系統代碼將在運行任何進程之前按如下方式從崩潰中恢復。如果日誌標記為包含完整操作，則恢復代碼會將寫入內容複製到它們在磁碟檔系統中所屬的位置。如果日誌未標記為包含完整操作，則恢復代碼將忽略該日誌。恢復代碼通過擦除日誌來完成。為什麼 xv6 的日誌解決了文件系統運行過程中的崩潰問題？如果崩潰發生在操作提交之前，則磁碟上的日誌不會標記為完成，重新編碼將忽略它，並且磁碟的狀態將好像操作甚至未開始一樣。如果崩潰發生在操作提交之後，則恢復將重放操作的所有寫入，如果操作已開始將它們寫入磁碟上的數據結構，則可能會重複這些寫入。無論哪種情況，日誌都會使操作在崩潰方面具有原子性：恢復后，操作的所有寫入都顯示在磁碟上，或者沒有寫入。

### 8.5 Log design

日誌駐留在超級塊中指定的已知固定位置。它由一個 header 塊和一系列更新的塊副本（“記錄的塊”）組成。header 塊包含一個扇區號陣列，每個記錄的塊對應一個扇區號，以及日誌塊的計數。磁碟上 Headers 塊中的計數為零，表示日誌中沒有事務，或者非零，表示日誌包含具有指示數量的記錄塊的完整提交事務。Xv6 在事務提交時寫入頭塊，但不在事務提交之前寫入，並在將記錄的塊複製到文件系統後將計數設置為零。因此，事務中途的崩潰將導致日誌的 header 塊中的計數為零;提交后的崩潰將導致非零計數。每個系統調用的代碼都指示寫入序列的開始和結束，這些寫入序列對於崩潰必須是原子的。為了允許通過不同的過程併發執行文件系統操作，日誌記錄系統可以將多個系統調用的寫入累積到一個事務中。因此，單個提交可能涉及多個完整系統調用的寫入。為避免跨事務拆分系統調用，日誌記錄系統僅在沒有文件系統系統調用進行時提交。將多個事務一起提交的想法稱為 group commit。組提交減少了磁碟操作的數量，因為它將提交的固定成本分攤到多個操作中。Group commit 還會同時為磁碟系統提供更多的併發寫入，可能允許磁碟在單個磁碟輪換期間寫入所有寫入。Xv6 的 virtio 驅動程式不支援這種批處理，但 xv6 的檔案系統設計允許這樣做。

Xv6 在磁碟上留出一定量的空間來保存日誌。交易中系統調用寫入的區塊總數必須適合該空間。這有兩個後果。不允許單個系統調用寫入超過日誌中空間的不同塊。對於大多數系統調用來說，這不是問題，但其中兩個調用可能會寫入許多塊：writeandunlink。大檔寫入可能會寫入許多數據塊和許多點陣圖塊以及一個 inode 塊;取消連結大型檔可能會寫入許多位圖塊和一個 inode。Xv6 的寫入系統調用將大型寫入分解為多個適合日誌的較小寫入，並且取消連結不會引起問題，因為在實踐中 xv6 文件系統只使用一個位圖塊。日誌空間有限的另一個後果是，日誌記錄系統不允許系統調用啟動，除非確定系統調用的寫入將適合日誌中剩餘的空間。

### 8.6 Code: logging

在系統調用中log的典型用法如下所示：

begin\_op（）;...bp = 麵包（...）;bp->data\[...\] = ...;log\_write（bp）;...end\_op（）;begin\_op（kernel/log.c：127）等到日誌系統當前沒有提交，並且直到有足夠的未保留的日誌空間來保存來自此 call.log.outstanding 計算具有保留日誌空間的系統調用次數;總預留空間 islog.outstanding timesMAXOPBLOCKS。Incrementinglog.outstanding既保留空間，又防止在此系統調用期間發生 com- mit。該代碼保守地假設每個系統調用都可能寫入 toMAXOPBLOCKSdistinct 塊。log\_write（kernel/log.c：215）充當 bwrite 的代理。它將塊的扇區號記錄在記憶體中，在磁碟上的日誌中為其保留一個插槽，並將緩衝區固定在塊緩存中以防止塊緩存逐出它。塊必須保留在緩存中，直到提交：在此之前，緩存的副本是修改的唯一記錄;在 commit 之前，它不能寫入磁碟上的位置;和同一事務中的其他讀取在單個事務中多次寫入塊時必須看到 modifications.log\_writenotices，並在日誌中為該塊分配相同的插槽。這種優化通常稱為吸收。例如，包含多個檔的 inode 的磁碟塊在一個事務中被寫入多次是很常見的。通過將多個磁碟寫入合併為一個，檔案系統可以節省日誌空間並獲得更好的性能，因為只需要將磁碟塊的一個副本寫入磁碟。end\_op（kernel/log.c：147）首先遞減未完成的系統調用的計數。如果計數現在為零，則通過調用 commit（） 提交當前事務。此 process.write\_log （）（kernel/log） 有四個階段。c：179）將事務中修改的每個塊從緩衝區緩存複製到其在日誌中的插槽 disk.write\_head（）（kernel/log.c：103）將頭塊寫入磁碟：這是提交點，寫入后崩潰將導致恢復重放

事務從 log.install\_trans （kernel/log.c：69） 寫入日誌中讀取每個塊並將其寫入文件系統中的適當位置。Finallyend\_opwrites count 為零的log標頭;這必須在下一個事務開始寫入記錄的區塊之前發生，這樣崩潰不會導致使用一個事務的 Headers 和後續事務的記錄區塊進行恢復。

recover\_from\_log（kernel/log.c：117）稱為 frominitlog（kernel/log.c：55），在第一個用戶進程運行 （kernel/proc.c：535） 之前，在啟動時調用 fromfsinit（kernel/fs.c：42）。它讀取日誌標頭，並類比ofend\_opif標頭指示日誌包含已提交事務的操作。

日誌的一個示例用法出現在 filewrite（kernel/file.c：135） 中。事務如下所示：

begin_op();
ilock(f->ip);
r = writei(f->ip, ...);
iunlock(f->ip);
end_op();


此代碼包裝在一個迴圈中，該迴圈將大型寫入一次分解為幾個扇區的單個事務，以避免日誌溢出。調用towritei將許多塊作為此事務的一部分寫入：檔的inode、一個或多個 bitmap 塊以及一些數據塊。

### 8.7 Code: Block allocator

文件和目錄內容存儲在磁碟塊中，必須從空閒池中分配。Xv6 的塊分配器在磁碟上維護一個空閑點陣圖，每個塊1位。零位表示相應的塊是空閒的;一位表示它正在使用中。programmkfs設置與引導扇區、超級塊、日誌塊、inode 塊和 bitmap 塊對應的位。

區塊分配器提供了兩個功能：balloc分配一個新的磁碟塊，以及 bfree 釋放一個 block.balloc 迴圈 inballocat（kernel/fs.c：72）考慮每個區塊，從區塊 0 開始到 tosb.size，文件系統中的區塊數量。它查找位圖位為零的塊，表示該塊是空閒的。Ifballoc找到這樣的塊，它會更新位圖並返回該塊。為了提高效率，該迴路分為兩部分。外部迴圈讀取每個點陣圖塊。內部迴圈檢查單個點陣圖塊中的所有每塊位 （BPB） 位。如果兩個進程嘗試同時分配一個塊，則可能會發生爭用，因為緩衝區緩存一次只允許一個進程使用任意一個位圖塊。

bfree（kernel/fs.c：92）找到正確的位圖塊並清除正確的位。同樣，breadandbrelse隱含的獨佔使用避免了顯式鎖定的需要。

與本章其餘部分中描述的大部分代碼一樣，必須在事務中調用 ballocandbfree。

### 8.8 Inode layer

terminode 可以具有以下兩個相關含義之一。它可能是指包含檔案大小和數據塊號清單的磁碟數據結構。或者 「inode」 可能是指記憶體中的 inode，其中包含磁碟上 inode 的副本以及內核中所需的額外資訊。磁碟上的 inode 被打包到磁碟的連續區域（稱為 inode 塊）中。每個 inode 的大小都相同，因此在給定數位 n 的情況下，很容易找到磁碟上的第 n 個 inode。事實上，這個數位 n，稱為 inode 編號或 i-number，是 inode 在實現中的標識方式。磁碟上的 inode 由 astruct dinode（kernel/fs.h：32） 定義。類型欄位區分檔、目錄和特殊檔案（設備）。類型 0 表示磁碟上 inode 可用。Thenlink欄位計算引用此 inode 的目錄條目數，以便識別何時應釋放磁碟上的 inode 及其數據塊。thesize位元段記錄檔中內容的位元元組數。addrsarray 記錄保存文件內容的磁碟塊的塊號。內核將活動 inode 集保存在記憶體中的 table callitable 中;struct inode （kernel/file.h：17）是 astruct dinodeon disk 的記憶體副本。僅當有 C 指標引用該 inode 時，內核才會將 inode 儲存在記憶體中。Thereffield 對引用記憶體中 inode 的 C 指標的數量進行計數，如果引用計數下降到零，內核將從記憶體中丟棄該 inode。igetandiput函數獲取和釋放指向 inode 的指標，從而修改引用計數。指向 inode 的指標可以來自檔描述符、當前工作目錄和瞬態內核代碼，例如 exec。 xv6 的 inode 中有四種鎖或類似鎖的機制 code.itable.lock保護 inode 在 inode 表中最多出現一次的不變量，以及記憶體中 inode 的 sreffield 計算指向 inode 的記憶體中指標數的不變量。每個記憶體中的 inode 都有一個包含 sleep-lock 的 alockfield，它確保對 inode 的字段（例如文件長度）以及 inode 的文件或目錄內容塊的獨佔訪問。如果 inode 的 sref 大於零，則會導致系統在表中維護該 inode，並且不會將表條目重新用於其他 inode。最後，每個 inode 都包含一個 anlinkfield（在磁碟上，如果在記憶體中，則複製到記憶體中），該字段計算引用文件的目錄條目的數量;如果 inode 的連結計數大於零，則 xv6 不會釋放 inode。保證 iget（） 傳回的 Astruct inodepointer 在相應的調用 toiput（） 之前有效;inode 不會被刪除，並且指標引用的記憶體不會被重新用於不同的 inode.iget（）提供對 inode 的非獨佔訪問，因此可以有許多指標指向同一個 inode。文件系統代碼的許多部分都依賴於iget（） 的這種行為，既可以保存對inode的長期引用（作為打開的檔和當前目錄），也可以防止爭用，同時避免在操作多個 inode 的代碼中死鎖（例如路徑名查找）。struct inodethatiget返回可能沒有任何有用的內容。為了確保它包含磁碟上 inode 的副本，代碼必須 callilock。這將鎖定 inode（以便沒有其他進程 canilockit）並從磁碟讀取 inode（如果尚未讀取）。 將 inode 指標的獲取與鎖定分開有助於避免在某些情況下（例如在目錄查找期間）死鎖。多個進程可以保存

指向 inode 的 C 指標返回 iget，但一次只有一個進程可以鎖定該 inode。inode 表僅存儲內核代碼或數據結構保存 C 指標的 inode。它的主要工作是同步多個進程的訪問。inode 表也恰好緩存了常用的 inode，但緩存是次要的;如果經常使用 inode，緩衝區緩存可能會將其保存在記憶體中。修改記憶體中 inode 的代碼使用 iupdate 將其寫入磁碟。

### 8.9 Code: Inodes

要分配新的 inode（例如，在創建檔時），xv6 調用 ialloc（kernel/fs.c：199）。ialloc與 balloc 類似：它遍歷磁碟上的 inode 結構，一次一個塊，尋找標記為free的 inode 結構。當它找到一個條目時，它通過將 newtype 寫入磁碟來聲明它，然後返回帶有尾部調用 toiget（kernel/fs.c：213） 的 inode 表中的條目。ialloc 的正確操作取決於一次只有一個進程可以持有引用 tobp：ialloc可以確保其他進程不會同時看到 inode 可用並嘗試聲明它。iget（kernel/fs.c：247）在 inode 表中查找具有所需設備和 inode 編號的活動條目 （ip->ref > 0）。如果找到一個節點，則返回對該 inode 的新引用 （kernel/fs.c：256-260）。Asigetscans 中，它會記錄第一個空 slot（kernel/fs.c：261- 262）的位置，如果需要分配表項，它會使用這個位置。代碼必須在讀取或寫入其元數據或 content.ilock （kernel/fs.c：293） 之前使用 ilock 鎖定 inode。Onceilock具有對 inode 的獨佔訪問許可權，如果需要，它會從磁碟（更有可能是緩衝區緩存）讀取 inode。functioniunlock （kernel/fs.c：321） 釋放休眠鎖，這可能會導致任何休眠的進程被喚醒。iput（kernel/fs.c：337）通過遞減引用計數 （kernel/fs.c：360） 來釋放指向 inode 的 C 指標。如果這是最後一個引用，則 inode 在 inode 表中的插槽現在是空閒的，可以重新用於其他 inode。Ifiput看到沒有指向 inode 的 C 指標引用，並且 inode 沒有指向它的連結（出現在任何目錄中），則必須釋放 inode 及其數據塊。iputcallsitrunc 將檔截斷為零位元組，從而釋放數據塊;將 inode type 設置為 0 （unallocated）;並將 inode 寫入磁碟 （kernel/fs.c：342）。鎖定協議在釋放 inode 的情況下值得仔細研究。一種危險是併發線程可能正在等待 inilock 使用此 inode（例如，讀取檔或列出目錄），並且不會準備好發現 inode 不再分配。這不會發生，因為如果 in-memory inode 沒有連結，則系統調用無法獲取指向該 inode 的指標，並且 ip->ref為 1。該引用是調用 iput 的線程所擁有的引用。另一個主要危險是併發調用 toialloc 可能會選擇與 iputis 釋放的相同的 inode。只有在 iupdate 寫入磁碟以使 inode 的類型為零之後，才會發生這種情況。這場競賽是良性的;分配線程將禮貌地等待獲取 inode 的 sleep-lock，然後再讀取或寫入 inode，此時 pointiputis 完成它。iput（） 可以寫入磁碟。這意味著任何使用檔系統的系統調用都可能寫入磁碟，因為系統調用可能是最後一個引用該檔的調用。甚至

調用似乎是只讀的 Read（） 可能最終會調用 iput（）。反過來，這意味著如果唯讀系統調用使用文件系統，則它們也必須包裝在事務中。iput（） 和 crashes.iput（） 之間有一個具有挑戰性的交互，當檔的連結計數降至零時，它不會立即截斷檔，因為某些進程可能仍將對 inode 的引用保存在記憶體中：進程可能仍在讀取和寫入檔，因為它成功打開了該檔。但是，如果在最後一個進程關閉檔的檔描述符之前發生崩潰，則檔將在磁碟上標記為 distributed，但沒有目錄條目指向它。檔系統通過以下兩種方式之一處理這種情況。簡單的解決方案是，在恢復時，在重新引導后，文件系統會掃描整個文件系統，以查找標記為已分配但沒有指向它們的目錄條目的檔。如果存在任何此類檔，則它可以釋放這些檔。第二種解決方案不需要掃描檔系統。在此解決方案中，文件系統在磁碟上（例如，在super塊中）記錄連結計數降至零但引用計數不為零的檔的inode inumber。如果檔案系統在引用計數達到 0 時刪除檔，則會通過從清單中刪除該 inode 來更新磁碟上的清單。在恢復時，檔案系統將釋放清單中的任何檔。Xv6 沒有實現這兩種解決方案，這意味著 inode 可以在磁碟上標記為已分配，即使它們不再使用。這意味著隨著時間的推移，xv6 可能會耗盡磁碟空間。

### 8.10 Code: Inode content

磁碟上的 inode 結構 struct dinode 包含一個大小和一個塊號陣列（參見圖 8.3）。inode 數據位於 dinode 的 saddrsarray 中列出的塊中。數據的第一個 NDIRECTblocks 列在數位的 firstNDIRECTentries 中;這些塊稱為 直接塊。數據的 nextNINDIRECT塊不在 inode 中列出，而是在稱為 indirect 塊的數據塊中列出。addrsarray 中的最後一個條目給出了間接塊的位址。因此，檔的前 12 kB （NDIRECT x BSIZE） 位元組可以從 inode 中列出的塊載入，而接下來的 256 kB （NINDIRECT x BSIZE） 位元組只能在查詢間接塊後載入。這是一個很好的磁碟表示形式，但對客戶端來說是一個複雜的表示形式。函數 bmap管理表示，以便更高級別的例程，例如 readiandwritei，我們稍後會看到，不需要管理這種複雜性。bmap返回 inodeip 的第 bn 個數據塊的磁碟塊號。Ifip還沒有這樣的塊，bmap分配一個。functionbmap（kernel/fs.c：383）首先挑選一個簡單的情況：第一個 NDIRECT 塊列在 inode 本身（kernel/fs.c：388-396）中。nextNINDIRECT塊列在間接塊 atip->addrs\[NDIRECT\].bmap 中讀取間接塊 （kernel/fs.c：407），然後從塊中的正確位置讀取塊號 （kernel/fs.c：408）。如果區塊號超過 NDIRECT+NINDIRECT，bmappanics;writei包含防止這種情況發生的檢查 （kernel/fs.c：513）。bmap分配塊。Anip->addrs\[\]或間接輸入零表示未分配區塊。Asbmapen遇到零，它會用按需分配的新塊的數量替換它們 （kernel/fs.c：389-390） （kernel/fs.c：401-402）。 itrunc釋放文件的塊，將 inode 的大小重置為 zero.itrunc（kernel/fs.c：426）開始於

type
major
minor
nlink
size
address 1


address 12
indirect


dinode


address 1


address 256


indirect block


data


data


data


data


Figure 8.3: The representation of a file on disk.


釋放直接塊 （kernel/fs.c：432-437），然後釋放間接塊中列出的塊 （kernel/fs.c：442- 445），最後釋放間接塊本身 （kernel/fs.c：447-448）。bmap使 ReadiAndWriteiTo 獲取 inode 的 data.readi（kernel/fs.c：472） 首先確保 offset 和 count 不超過檔末尾。從檔末尾開始的讀取返回錯誤 （kernel/fs.c：477-478），而從檔末尾開始或越過檔末尾的讀取返回的位元組數少於請求的位元組數 （kernel/fs.c：479-480）。主循環處理檔的每個塊，從緩衝區 intodst（kernel/fs.c：482-494）.writei （kernel/fs.c：506）複製數據與 readi 相同，但有三個例外：從檔末尾開始或跨越檔末尾的寫入會使檔增大，直到達到最大檔大小 （kernel/fs.c：513-514）;迴圈將數據複製到緩衝區中，而不是 out（kernel/fs.c：522）;如果寫入擴展了檔，writei必須更新它的大小（kernel/fs.c：530-531）。functionstati（kernel/fs.c：458） 將 inode 元數據複製到 statstructure 中，該結構通過 statsystem 調用公開給用戶程式。

### 8.11 代碼：directory layer

目錄在內部實現，與檔非常相似。它的 inode has typeT\_DIRand其數據是一系列目錄條目。每個條目都是 astruct dirent（kernel/fs.h：56），其中包含一個

name 和 inode 編號。名稱最多為 DIRSIZ（14） 個字元;如果較短，則以 NULL （0） 位元組終止。inode 編號為零的目錄條目是免費的。functiondirlookup（kernel/fs.c：552） 在目錄中搜索具有給定名稱的條目。如果找到一個，則返回指向相應 inode 的指標 unlocked，並將_poffto 設置為位元組 offset 目錄中的條目，以防調用方希望編輯它。Ifdirlookup查找 具有正確名稱的條目 it updates_poff並返回通過 iGet 獲取的未鎖定 inode。dirlookup是iget 傳回未鎖定的inode 的原因。調用方已鎖定dp，因此，如果查找的是當前目錄的別名。嘗試在返回之前鎖定 inode 將嘗試重新鎖定dp並死鎖。（還有更複雜的死鎖方案，涉及多個進程和 ..，父目錄的別名;。並不是唯一的問題。調用者可以解鎖 dp 然後lockip，確保它一次只持有一個鎖。functiondirlink（kernel/fs.c：580） 將具有給定名稱和索引號的新目錄條目寫入 directorydp。如果名稱已存在，dirlink 將返回錯誤 （kernel/fs.c：586- 590）。主循環讀取目錄條目，查找未分配的條目。當它找到一個時，它會提前停止迴圈（kernel/fs.c：592-597），偏移量為可用條目的偏移量。否則，迴圈以偏移 todp->size 結束。無論哪種方式，dirlink都會通過在 offsetoff（kernel/fs.c：602-603） 處寫入來向目錄添加新條目。

### 8.12 Code: Path names

路徑名查找涉及一系列對 dirlookup 的調用，每個路徑元件一個調用。namei（kernel/fs.c：687）evaluatespath並返回相應的 inode。functionnameiparent 是一個變體：它在最後一個元素之前停止，返回父目錄的 inode 並將最後一個元素複製到 name 中。兩者都調用廣義的 functionnamex 來執行實際工作。namex（kernel/fs.c：652）首先決定路徑評估的開始位置。如果路徑以斜杠開頭，則 evaluation 從根開始;否則為當前目錄（kernel/fs.c：656-659）。然後它使用 skipelem依次考慮路徑的每個元素 （kernel/fs.c：661）。迴圈的每次反覆運算都必須在當前 inodeip 中查找 upname。反覆運算從 lockingip 並檢查它是否為目錄開始。否則，查找失敗 （kernel/fs.c：662-666）。（Lockingipis necessary 不是因為 ip->type可以在 foot-down-it 不能改變，而是因為 untililockruns，ip->type 不能保證是從磁碟載入的。如果調用 isnameiparent並且這是最後一個 path 元素，則根據 nameiparent 的定義，迴圈會提前停止;最後一個 path 元素已經被複製到 name 中，sonamex只需要返回 unlockedip（kernel/fs.c：667-671）。最後，迴圈使用 dirlookup 查找路徑元素，並通過設置 ip = next（kernel/fs.c：672-677） 為下一次反覆運算做準備。當迴圈用完 path 元素時，它會返回 ip。procedurenamex可能需要很長時間才能完成：它可能涉及多個磁碟操作，以讀取路徑名中遍歷的目錄的 inode 和目錄塊（如果它們不在緩衝區緩存中）。 Xv6 經過精心設計，如果一個內核線程在磁碟 I/O 上阻塞了 namex，則另一個查找不同路徑名的內核線程可以併發地進行。namexlocks 路徑中的每個目錄，以便可以並行進行不同目錄中的查找。這種併發帶來了一些挑戰。例如，當一個內核線程正在查找

向上移動路徑名：另一個內核線程可能正在通過取消連結目錄來更改目錄樹。一個潛在的風險是，查找可能正在搜索已被另一個內核線程刪除的目錄，並且其塊已被另一個目錄或檔重新使用。Xv6 避免了這樣的比賽。例如，在執行 dirlookupinnamex 時，查找線程將持有目錄上的鎖，並且 dirlookup 會返回使用 iget 獲取的 inode。iget增加 inode 的引用計數。只有在從 dirlookup 收到 inode 后，amex 才會釋放對目錄的鎖。現在，另一個線程可能會取消 inode 與目錄的連結，但 xv6 不會刪除 inode，因為 inode 的引用計數仍然大於零。另一個風險是死鎖。例如，next在查找 “.” 時指向同一個 inode asip。Lockingnext，否則會導致死鎖。為避免此死鎖，namex會在獲取鎖 onnext 之前解鎖目錄。在這裏，我們再次看到了為什麼 igetandilocke 之間的分離很重要。

### 8.13 File descriptor layer

Unix 介面的一個很酷的方面是，Unix 中的大多數資源都表示為檔，包括控制台、管道等設備，當然還有真實檔。檔描述符層是實現這種一致性的層。Xv6 為每個進程提供了自己的打開檔表或檔描述符，正如我們在第 1 章中看到的那樣。每個打開的檔都由 astruct file（kernel/file.h：1） 表示，它是 inode 或管道的包裝器，外加 I/O 偏移量。每次調用 open都會創建一個新的打開檔（newstruct 檔）：如果多個進程獨立打開同一個檔，則不同的實例將具有不同的 I/O 偏移量。另一方面，單個打開的檔（samestruct 檔）可以在一個進程的檔表中多次出現，也可以在多個進程的檔表中出現多次。如果一個進程使用 open打開檔，然後使用 dupor 創建別名，則將其與 using fork 的子進程共用，則會發生這種情況。引用計數跟蹤對特定打開檔的引用數。檔可以打開以進行讀取和/或寫入。thereadableandwritable字段會跟蹤此內容。系統中的所有打開檔都保存在一個全域檔表中，可被盜。檔表具有分配檔 （filealloc）、創建重複引用 （filedup）、釋放引用 （fileclose） 以及讀取和寫入數據 （filereadandfilewrite） 的函數。前三個遵循現在熟悉的形式.filealloc（kernel/file.c：30）掃描檔表以查找未引用的檔 （f->ref == 0） 並返回新的引用;filedup（kernel/file.c：48）增加引用計數;andfileclose（kernel/file.c：60）遞減它。當檔的引用計數達到零時，fileclose會根據類型釋放底層管道或 inode。 函數filestat、fileread 和 filewrite實現對 files.filestat（kernel/file.c：88）的統計、讀取和寫入操作只允許在 inode 上執行，並調用 stati.fileread 和 filewrite檢查打開模式是否允許該操作，然後將調用傳遞給 pipe 或 inode 實現。如果檔表示 inode，fileread和 filewrite使用 I/O 偏移量作為操作的偏移量，然後將其推進 （kernel/file.c：122- 123） （kernel/file.c：153-154）。管道沒有偏移的概念。回想一下，inode 函數需要

處理鎖定的調用方 （kernel/file.c：94-96） （kernel/file.c：121-124） （kernel/file.c：163-166）。in- ode 鎖定具有方便的副作用，即讀取和寫入偏移量以原子方式更新，因此同時對同一檔的多個寫入無法覆蓋彼此的數據，儘管它們的寫入最終可能會交錯。

### 8.14 Code: System calls

使用較低層提供的函數，大多數系統調用的實現都很簡單（參見（kernel/sysfile.c））。有幾個電話值得仔細研究。functionssys\_linkandsys\_unlinkedit 目錄，用於創建或移除對 inode 的引用。它們是使用 transactions.sys\_link（kernel/sys- file.c：124）的另一個很好的例子，首先獲取其參數，兩個 stringsoldandnew（kernel/sysfile.c：129）。假設 oldexists 且不是一個目錄 （kernel/sysfile.c：133-136），sys\_linkincrements itsip->nlink 計數。Thensys\_linkcallsnameiparentto找到 new（kernel/sysfile.c：149） 的父目錄和最終路徑元素，並創建一個指向 atold 的 inode（kernel/sys- file.c：152） 的新目錄條目。新的父目錄必須存在，並且與現有 inode 位於同一設備上：inode 編號僅在單個磁碟上具有唯一含義。如果發生這樣的錯誤，sys\_link必須返回並遞減ip->nlink。事務簡化了實現，因為它需要更新多個磁碟塊，但我們不必擔心執行它們的順序。他們要麼都會成功，要麼都不會成功。例如，如果沒有事務，在創建連結之前 updatingip->nlink 會使文件系統暫時處於不安全狀態，中間的崩潰可能會導致嚴重破壞。有了交易，我們就不必擔心這個。sys\_linkcreates現有 inode 的新名稱。函數create（kernel/sysfile.c：246） 為新 inode 創建一個新名稱。它是三種檔創建系統調用的泛化：openwith theO\_CREATEflag創建一個新的普通檔，mkdir創建一個新的目錄，mkdev創建一個新的設備檔。Likesys\_link，create首先調用 NameiParent以獲取父目錄的 inode。 然後調用 dirlookup 檢查名稱是否已經存在 （kernel/sysfile.c：256）。如果名稱確實存在，create 的行為取決於它用於哪個系統調用：open與 mkdirandmkdev 具有不同的語義。如果 create代表 open（type == T\_FILE） 使用，並且存在的名稱本身就是一個常規文件，那麼 open會將其視為成功，socreate也會這樣做（kernel/sysfile.c：260）。否則，它是一個錯誤 （kernel/sysfile.c：261-262）。如果該名稱尚不存在，createnow 會使用 ialloc（kernel/sysfile.c：265） 分配一個新的 inode。如果新 inode 是一個目錄，create會用 .和 ..條目。最後，現在數據已經正確初始化了，create可以將其連結到父目錄（kernel/sysfile.c：278）.create，likesys\_link同時持有兩個 inode 鎖：ip 和 dp。沒有死鎖的可能性，因為 inodeipis 是新分配的：系統中沒有其他進程會 holdip 的鎖，然後嘗試 lockdp。使用 create，很容易implementsys\_open，sys\_mkdir，andsys\_mknod.sys\_open （kernel/sysfile.c：305） 是最複雜的，因為創建新檔只是它能做的一小部分。如果 open theO\_CREATEflag傳遞，它會調用 create（kernel/sysfile.c：320）。否則，它會調用 namei（kernel/sysfile.c：326）。create會返回鎖定的 inode，butnamei不會返回，sosys\_open

必須鎖定 inode 本身。這提供了一個方便的位置來檢查目錄是否僅用於讀取，而不是寫入。假設 inode 是通過某種方式獲得的，sys\_open 分配一個檔和一個檔描述符 （kernel/sysfile.c：344），然後填寫檔 （kernel/sysfile.c：356- 361）。請注意，沒有其他進程可以訪問部分初始化的檔，因為它僅在當前進程的表中。第 7 章研究了管道的實現，甚至在我們有了文件系統之前。該函數通過提供一種創建管道對的方法，將該實現sys\_pipeconnects文件系統。它的參數是指向兩個整數的空格的指標，它將在其中記錄兩個新的檔描述符。然後，它分配管道並安裝檔描述符。

### 8.15 Real world

實際操作系統中的緩衝區緩存比 xv6 的要複雜得多，但它具有相同的兩個目的：緩存和同步對磁碟的訪問。Xv6 的緩衝區緩存與 V6 的緩衝區緩存一樣，使用簡單的最近最少使用 （LRU） 驅逐策略;可以實施許多更複雜的策略，每種策略都適用於某些工作負載，而適用於其他工作負載則不那麼好。更高效的 LRU 快取將消除鏈錶，而是使用哈希表進行查找，使用堆進行 LRU 驅逐。現代緩衝區緩存通常與虛擬記憶體系統集成，以支援記憶體映射檔。Xv6 的日誌記錄系統效率低下。提交不能與文件系統系統調用同時發生。系統會記錄整個數據塊，即使數據塊中只有幾個位元組被更改。它執行同步日誌寫入，一次一個塊，每個寫入都可能需要整個磁碟輪換時間。真正的測井系統解決了所有這些問題。日誌記錄並不是提供崩潰恢復的唯一方法。早期的文件系統在重新引導期間使用清道夫（例如 UNIXfsckprogram）來檢查每個文件和目錄以及塊和 inode 空閒清單，以查找和解決不一致問題。對於大型文件系統，清理可能需要數小時，並且在某些情況下，無法以導致原始系統調用為原子的方式解決不一致。從日誌中恢復的速度要快得多，並且會導致系統調用在崩潰時是原子的。Xv6 使用與早期 UNIX 相同的 inode 和目錄的基本磁碟佈局;多年來，這個計劃一直非常持久。BSD 的 UFS/FFS 和 Linux 的 ext2/ext3 基本上使用相同的數據結構。 文件系統佈局中效率最低的部分是目錄，它需要在每次查找期間對所有磁碟塊進行線性掃描。當目錄只有幾個磁碟塊時，這是合理的，但對於包含許多文件的目錄來說，這是昂貴的。僅舉幾例，Microsoft Windows 的 NTFS、macOS 的 HFS 和 Solaris 的 ZFS 將目錄實現為磁碟上平衡的塊樹。這很複雜，但可以保證對數時間目錄查找。Xv6 對磁碟故障很幼稚：如果磁碟操作失敗，XV6 會崩潰。這是否合理取決於硬體：如果操作系統位於使用冗餘來掩蓋磁碟故障的特殊硬體之上，那麼操作系統看到故障的頻率可能非常低，以至於恐慌是可以的。另一方面，使用普通磁碟的操作系統應該預料到故障並更優雅地處理它們，以便一個檔中塊的丟失不會影響其餘部分的使用。

檔案系統。Xv6 要求文件系統適合一個磁碟設備，並且大小不能改變。隨著大型資料庫和多媒體檔對存儲的要求越來越高，操作系統正在開發消除“每個文件系統一個磁碟”瓶頸的方法。基本方法是將多個磁碟合併到一個邏輯磁碟。RAID 等硬體解決方案仍然是最流行的，但當前的趨勢是盡可能多地在軟體中實現這種邏輯。這些軟體實現通常允許豐富的功能，例如通過動態添加或刪除磁碟來增大或縮小邏輯設備。當然，可以動態擴展或收縮的存儲層需要一個可以執行相同操作的文件系統：xv6 使用的固定大小的 inode 塊陣列在此類環境中無法正常工作。將磁碟管理與文件系統分離可能是最簡潔的設計，但兩者之間的複雜介面導致一些系統（如 Sun 的 ZFS）將它們組合在一起。Xv6 的文件系統缺少現代文件系統的許多其他功能;例如，它缺少快照和增量備份的支援。現代 Unix 系統允許使用與磁碟存儲相同的系統調用來存取多種資源：命名管道、網路連接、遠端訪問的網路文件系統以及監視和控制介面，例如 /proc。這些系統通常為每個打開的檔提供一個函數指標表，每個操作一個，而不是 xv6 的 sifstatements infileread 和 filewrite，並調用函數指標來調用該 inode 的調用實現。網路檔案系統和使用者級檔系統提供了將這些調用轉換為網路 RPC 並在返回之前等待回應的功能。

### 8.16 Exercises

1. 為什麼 panic inballoc？xv6 可以恢復嗎？
2. 為什麼 panic inialloc？xv6 可以恢復嗎？
3. 為什麼當檔用完時不會 fileallocpanic 呢？為什麼這種情況更常見，因此值得處理？
4. 假設與toips相對應的檔被另一個進程取消連結，betweensys\_link調用了 toiunlock（ip）anddirlink。連結是否會正確創建？為什麼或為什麼不？
5. create進行 4 次函數調用（1 次 toialloc 和 3 次 todirlink），成功。如果有沒有，createcallspanic。為什麼這是可以接受的？為什麼這四個調用中的任何一個都不會失敗？
6. sys\_chdircallsiunlock（ip）beforeiput（cp->cwd），它可能會嘗試鎖定cp->cwd，但將iunlocking（ip）推遲到iput之後不會造成死鎖。為什麼不呢？
7. 實現 thelseeksystem 調用。Supportinglseek將還要求您修改 filewrite，以填充檔中的空洞 iflseeksetsoffbeyondf->ip->size。
8. AddO\_TRUNCandO\_APPENDtoopen，以便>and>>運算符在shell中工作。
9. 修改檔案系統以支援符號連結。
10. 修改檔案系統以支援命名管道。
11. 修改檔和 VM 系統以支援記憶體映射檔。

第 9 章
=====

重新審視併發性
=======

同時獲得良好的並行性能、併發性的正確性和可理解的代碼是內核設計中的一大挑戰。直接使用鎖是實現正確性的最佳途徑，但並不總是可能的。本章重點介紹 xv6 被迫以複雜方式使用鎖的示例，以及 xv6 使用類似鎖的技術但不使用鎖的範例。

### 9.1 Locking patterns

緩存的專案通常很難鎖定。例如，文件系統的塊緩存 （ker- nel/bio.c：26） 最多可存儲 NBUFdisk 塊的副本。給定的磁碟塊在緩存中最多有一個副本，這一點至關重要;否則，不同的進程可能會對本應是同一塊的不同副本進行衝突的更改。每個緩存的塊都存儲在 astruct buf （kernel/buf.h：1） 中。Astruct buf具有一個lock欄位，有助於確保一次只有一個進程使用給定的磁碟塊。然而，這個鎖是不夠的：如果緩存中根本不存在一個塊，並且兩個進程想同時使用它怎麼辦？有 nostruct buf （因為塊尚未緩存），因此沒有什麼可以鎖定的。Xv6 通過將額外的鎖 （bcache.lock） 與緩存塊的標識集相關聯來處理這種情況。需要檢查塊是否被緩存的代碼（例如，bget（kernel/bio.c：59））或更改緩存塊的集合，必須 holdbcache.lock;在該代碼找到所需的塊和結構buf後，它可以釋放bcache.lock並僅鎖定特定塊。這是一種常見的模式：一組項一個鎖，每個項一個鎖。

通常，獲取鎖的相同函數將釋放它。但更精確的看待事物的方法是，在序列的開頭獲取鎖，該鎖必須顯示為原子，並在該序列結束時釋放。如果序列以不同的函數、不同的線程或不同的 CPU 開始和結束，則鎖 acquire 和 release 必須執行相同的操作。鎖的功能是強制其他使用者等待，而不是將一段數據固定到特定的代理。一個例子是 acquireinyield（kernel/proc.c：512），它在調度程式線程中釋放，而不是在採集進程中釋放。另一個例子是 acquiresleepinilock（kernel/fs.c：293）;此代碼通常在讀取磁碟時處於休眠狀態;它可能會在不同的CPU上喚醒，這意味著可以在不同的CPU上獲取和釋放鎖。

釋放受物件中嵌入的鎖保護的對像是一項微妙的工作，因為擁有鎖不足以保證釋放是正確的。當其他線程正在等待 inacquire以使用該物件時，就會出現問題情況;釋放物件會隱式釋放嵌入的鎖，這將導致等待線程出現故障。一種方法是跟蹤存在對物件的引用數量，以便僅在最後一個引用消失時釋放它。請參閱 pipeclose（kernel/pipe.c：59）;pi->readopen和 pi->writeopen跟蹤管道是否有引用它的檔描述符。通常，人們會看到圍繞相關項集的讀取和寫入序列的鎖;這些鎖確保其他線程只能看到已完成的更新序列（只要它們也鎖定）。如果更新只是簡單地寫入單個共用變數，該怎麼辦？例如，setkilledandkilled（kernel/proc.c：619）會鎖定它們的簡單用法 ofp->killed。如果沒有鎖，則一個線程可以在另一個線程讀取它的同時寫入 p->killed。這是一場競賽，C 語言規範指出，一場競賽會產生sundefined 的行為，這意味著程式可能會崩潰或產生不正確的結果^1。鎖可以防止爭用並避免未定義的行為。爭用可以破壞程式的一個原因是，如果沒有鎖或等效結構，編譯器可能會生成以與原始 C 代碼完全不同的方式讀取和寫入記憶體的機器代碼。例如，調用 killed 的線程的機器代碼可以將 p->killed複製到寄存器，並僅讀取該緩存的值;這意味著線程可能永遠不會看到任何寫入 top->killed。鎖會阻止此類緩存。

### 9.2 Lock-like patterns

在許多地方，xv6 以類似鎖的方式使用引用計數或標誌來指示物件已分配，不應釋放或重用。進程 sp->state以這種方式運行，引用計數 infile、inode 和 bufstructures 也是如此。雖然在每種情況下，鎖都會保護標誌或引用計數，但後者可以防止物件過早釋放。

文件系統使用 struct inode引用計數作為一種可由多個進程持有的共用鎖，以避免在代碼使用普通鎖時發生死鎖。例如，迴圈 innamex（kernel/fs.c：652） 依次鎖定每個 pathname 元件命名的目錄。但是，namex必須在循環結束時釋放每個鎖，因為如果它持有多個鎖，並且路徑名包含一個點（例如，a/./b），則它可能會與自身死鎖。它還可能會因涉及目錄的併發查找而死鎖，並且...正如第 8 章所解釋的，解決方案是讓迴圈將目錄 inode 帶到下一次反覆運算，其引用計數增加，但不被鎖定。某些數據項在不同時間受到不同機制的保護，有時可能通過 xv6 代碼的結構而不是顯式鎖隱式地防止併發訪問。例如，當物理頁空閒時，它受 kmem.lock（kernel/kalloc.c：24） 保護。如果該頁隨後被分配為pipe（kernel/pipe.c：23），則它由不同的鎖 （em- beddedpi->lock） 保護。如果為新進程的用戶記憶體重新分配該頁，則它不會受到保護

（^1）[https://en.cppreference.com/w/c/language/memory\_model](https://en.cppreference.com/w/c/language/memory_model) 中的“線程和數據爭用”

根本沒有鎖。相反，分配器不會將該頁提供給任何其他進程（直到它被釋放）這一事實可以保護它免受併發訪問。新進程記憶體的擁有權很複雜：首先，父進程在 fork 中分配和操作它，然後子進程使用它，然後（在子進程退出后）父進程再次擁有記憶體並將其傳遞給 tokfree。這裡有兩個教訓：數據物件在其生命週期的不同時間點可能會以不同的方式受到併發保護，並且保護可能採用隱式結構而不是顯式鎖的形式。最後一個類似鎖的例子是需要禁用調用 tomycpu（） 的中斷（ker- nel/proc.c：83）。禁用中斷會導致調用代碼相對於計時器輸入是原子的，這可能會強制上下文切換，從而將進程移動到不同的CPU。

### 9.3 No locks at all

在一些地方，xv6 共用可變數據，根本沒有鎖。一個是自旋鎖的實現，儘管人們可以將 RISC-V 原子指令視為依賴於硬體中實現的鎖。另一個是 started 變數 inmain.c（kernel/main.c：7），用於防止其他 CPU 運行，直到 CPU 0 完成初始化 xv6;TheVolatile 確保編譯器實際生成load和 store 指令。Xv6 包含一個 CPU 或線程寫入一些數據，另一個 CPU 或線程讀取數據的情況，但沒有專門用於保護該數據的特定鎖。例如，在 fork 中，父級寫入子級的用戶記憶體頁，而子級（不同的線程，可能在不同的 CPU 上）讀取這些頁面;No lock 明確保護這些頁面。嚴格來說，這並不是一個鎖定問題，因為在父級完成寫入之前，子級不會開始執行。這是一個潛在的記憶體排序問題（參見第 6 章），因為如果沒有記憶體屏障，就沒有理由期望一個 CPU 看到另一個 CPU 的寫入。但是，由於父級釋放鎖，而子級在啟動時獲取鎖，因此記憶體屏障 inacquireandrelease 確保子級的 CPU 看到父級的寫入。

### 9.4 並行度

鎖定主要是為了正確性而抑制並行性。因為性能也很重要，所以內核設計人員經常不得不考慮如何以一種既能實現正確性又能實現並行性的方式使用鎖。雖然 xv6 不是系統地為高性能而設計的，但仍然值得考慮哪些 xv6 操作可以並行執行，哪些操作可能在鎖上發生衝突。xv6 中的管道是相當好的並行性的一個例子。每個管道都有自己的鎖，因此不同的進程可以在不同的CPU上並行讀取和寫入不同的管道。但是，對於給定的管道，寫入器和讀取器必須等待彼此釋放鎖;它們不能同時讀/寫同一個管道。還有一種情況是，從空管道讀取（或寫入完整管道）必須阻塞，但這並不是由於鎖定方案。上下文切換是一個更複雜的範例。兩個內核線程（每個線程都在自己的CPU上執行）可以同時調用yield、sched和 swtchat，並且調用將並行執行。

每個線程都持有一個鎖，但它們是不同的鎖，因此它們不必相互等待。但是，一旦 inscheduler，兩個 CPU 可能會在鎖上發生衝突，同時在進程表中搜索 isRUNNABLE 的進程。也就是說，xv6 在上下文切換期間可能會從多個 CPU 獲得性能優勢，但可能不會達到應有的程度。另一個例子是從不同CPU上的不同進程併發調用 fork。這些調用可能必須彼此等待 forpid\_lockandkmem.lock，以及在進程表中搜索 UNUSEDprocess 所需的每個進程鎖。另一方面，這兩個分叉進程可以完全並行地複製用戶記憶體頁和格式化頁表頁。在某些情況下，上述每個示例中的鎖定方案都會犧牲並行性能。在每種情況下，都可以使用更精細的設計獲得更多的並行度。是否值得取決於細節：調用相關操作的頻率、代碼在持有爭用鎖的情況下花費的時間、可能同時運行衝突操作的CPU數量、代碼的其他部分是否是限制性更強的瓶頸。可能很難猜測給定的鎖定方案是否會導致性能問題，或者新設計是否明顯更好，因此通常需要對實際工作負載進行測量。

### 9.5 Exercises

1. 修改 xv6 的管道實現，以允許對同一管道的讀取和寫入在不同的 CPU 上並行進行。
2. 修改 xv6 的 sscheduler（） 以減少不同 CPU 同時尋找可運行進程時的鎖爭用。
3. 消除 xv6 的 sfork（） 中的一些序列化。

第十章
===

Summary
=======

本文通過逐行研究一個操作系統 xv6 來介紹操作系統中的主要思想。一些代碼行體現了主要思想的本質（例如，上下文切換、使用者/用戶邊界、鎖等），每一行都很重要;其他代碼行提供了如何實現特定操作系統思想的例證，並且可以很容易地以不同的方式完成（例如，更好的調度演算法、更好的磁碟數據結構來表示檔、更好的日誌記錄以允許併發事務等）。所有的想法都在一個特定的、非常成功的系統調用介面 Unix 介面的上下文中進行了說明，但這些想法也延續到了其他操作系統的設計中。

Bibliography
============

[1] Linux common vulnerabilities and exposures (CVEs). https://cve.mitre.org/
cgi-bin/cvekey.cgi?keyword=linux.


[2] The RISC-V instruction set manual Volume I: unprivileged specification ISA. https:
//drive.google.com/file/d/17GeetSnT5wW3xNuAHI95-SI1gPGd5sJ_
/view?usp=drive_link, 2024.


[3] The RISC-V instruction set manual Volume II: privileged specification. https:
//drive.google.com/file/d/1uviu1nH-tScFfgrovvFCrj7Omv8tFtkp/
view?usp=drive_link, 2024.


[4] Hans-J Boehm. Threads cannot be implemented as a library.ACM PLDI Conference, 2005.


[5] Edsger Dijkstra. Cooperating sequential processes. https://www.cs.utexas.edu/
users/EWD/transcriptions/EWD01xx/EWD123.html, 1965.


[6] Maurice Herlihy and Nir Shavit. The Art of Multiprocessor Programming, Revised Reprint.
2012.


[7] Brian W. Kernighan. The C Programming Language. Prentice Hall Professional Technical
Reference, 2nd edition, 1988.


[8] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin,
Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell,
Harvey Tuch, and Simon Winwood. Sel4: Formal verification of an OS kernel. InProceedings
of the ACM SIGOPS 22nd Symposium on Operating Systems Principles, page 207–220, 2009.


[9] Donald Knuth.Fundamental Algorithms. The Art of Computer Programming. (Second ed.),
volume 1. 1997.


\[10\] L 蘭波特。dijkstra 的併發程式設計問題的新解決方案。ACM 通訊，1974 年。

\[11\] John Lions.《UNIX 第 6 版評論》。點對點通信，2000 年。

\[12\] Paul E. Mckenney、Silas Boyd-wickizer 和 Jonathan Walpole。RCU 在 linux 內核中的使用：十年後的 2013 年。

\[13\] 馬丁·邁克爾和丹尼爾·杜裡奇。NS16550A：UART 設計和應用構想。[http://bitsavers.trailing-edge.com/components/national/](http://bitsavers.trailing-edge.com/components/national/) \_appNotes/AN-0491.pdf，1987 年。

\[14\] 阿萊夫一號。砸碎堆疊以獲得樂趣和利潤。[http://phrack.org/issues/49/](http://phrack.org/issues/49/) 14.html#文章。

\[15\] 大衛·派特森和安德魯·沃特曼。RISC-V Reader ：開放式架構 Atlas。草莓峽谷，2017 年。

\[16\] 戴夫·普雷索托、羅伯·派克、肯·湯普森和霍華德·特裡基。計劃9，分散式系統。InIn Proceedings of the Spring 1991 EurOpen Conference，第 43-50 頁，1991 年。

\[17\] 鄧尼斯·裡奇和肯·湯普森。UNIX 分時系統。公社。ACM，17（7）：365–375,1974 年 7 月。

Index
=====

#### ., 96, 98

#### .., 96, 98

/init、28、40 \_entry、28

absorption, 90 acquire, 63, 67 address space, 26 argc, 41 argv, 41 atomic, 63

balloc, 91, 93 batching, 89 bcache.head, 87 begin\_op, 90 bfree, 91 bget, 87 binit, 87 block, 86 bmap, 94 bottom half, 53 bread, 87, 88 brelse, 87, 88 BSIZE, 94 buf, 87 busy waiting, 75 bwrite, 87, 88, 90

chan， 76， 78 child， 10 commit， 89 concurrency， 59 concurrency control， 59

condition lock, 77
conditional synchronization, 75
conflict, 62
contention, 62
contexts, 72
convoys, 82
copy-on-write (COW) fork, 49
copyinstr, 47
copyout, 41
coroutines, 74
CPU, 9
cpu->context, 72, 73
crash recovery, 85
create, 98
critical section, 62
current directory, 17


deadlock, 64
demand paging, 50
direct blocks, 94
direct memory access (DMA), 56
dirlink, 96
dirlookup, 96, 98
DIRSIZ, 96
disk, 87
driver, 53
dup, 97


ecall, 23, 27
ELF format, 40
ELF_MAGIC, 40
end_op, 90
exception, 43
exec, 12–14, 28, 41, 47


exit, 11, 79

file descriptor, 13 filealloc, 97 fileclose, 97 filedup, 97 fileread, 97, 100 filestat, 97 filewrite, 91, 97, 100 fork, 10, 12–14, 97 forkret, 74 freerange, 37 fsck, 99 fsinit, 91 ftable, 97

getcmd， 12 組提交， 89 保護頁， 35

handler, 43 hartid, 74

I/O、13 I/O 併發、55 I/O 重定向、14 ialloc、93、98 iget、92、93、96 ilock、92、93、96 間接塊、94 initcode。S、28、47 initlog、91 inode、18、86、92 install\_trans、91 介面設計、9 中斷、43 iput、92、93 隔離、21 itable、92 itrunc、93、94 iunlock、93

kalloc, 38 kernel, 9, 23

kernel space, 9, 23
kfree, 37
kinit, 37
kvminit, 36
kvminithart, 36
kvmmake, 36
kvmmap, 36


lazy allocation, 49
links, 18
loadseg, 40
lock, 59
log, 89
log_write, 90
lost wake-up, 76


machine mode, 23
main, 36, 37, 87
malloc, 13
mappages, 36
memory barrier, 68
memory model, 68
memory-mapped, 35, 53
memory-mapped files, 50
metadata, 18
microkernel, 24
mkdev, 98
mkdir, 98
mkfs, 86
monolithic kernel, 21, 23
multi-core, 21
multiplexing, 71
multiprocessor, 21
mutual exclusion, 61
mycpu, 74
myproc, 74


namei, 40, 98
nameiparent, 96, 98
namex, 96
NBUF, 87
NDIRECT, 94
NINDIRECT, 94


#### O\_CREATE, 98

open, 97, 98

p->killed， 80 p->kstack， 27 p->lock， 73， 74， 78 p->pagetable， 27 p->state， 27 p->xxx， 27 頁， 31 頁表條目 （PTE）， 31 頁錯誤異常， 32， 49 分頁區域， 50 分頁到磁碟， 50 父， 10 路徑， 17 持久性， 85 PGROUNDUP， 37 物理位址， 26 PHYSTOP， 36， 37 PID， 10 管道， 16 管道讀取， 79 管道寫入， 79 輪詢， 56， 75 pop\_off， 67 printf， 12 優先順序反轉， 82 特權指令， 23 proc\_mapstacks， 36 proc\_pagetable， 40 進程， 9， 26 程式設計 I/O， 56 PTE\_R， 33 PTE\_U， 33 PTE\_V， 33 PTE\_W， 33 PTE\_X， 33 push\_off， 67

race, 61, 104 re-entrant locks, 66 read, 97

readi, 40, 94, 95
recover_from_log, 91
recursive locks, 66
release, 63, 67
root, 17
round robin, 82
RUNNABLE, 78, 79


satp, 33
sbrk, 13
scause, 44
sched, 72–74, 78
scheduler, 73, 74
sector, 86
semaphore, 75
sepc, 44
sequence coordination, 75
serializing, 62
sfence.vma, 37
shell, 10
signal, 83
skipelem, 96
sleep, 76–78
sleep-locks, 68
SLEEPING, 78
sret, 27
sscratch, 44
sstatus, 44
stat, 95, 97
stati, 95, 97
struct context, 72
struct cpu, 74
struct dinode, 92, 94
struct dirent, 95
struct elfhdr, 40
struct file, 97
struct inode, 92
struct pipe, 79
struct proc, 27
struct run, 37
struct spinlock, 63
stval, 49
stvec, 44


超級塊、86 管理引擎模式、23 Swtch、72–74 SYS\_exec、47 sys\_link、98 sys\_mkdir、98 sys\_mknod、98 sys\_open、98 sys\_pipe、99 sys\_sleep、67 sys\_unlink、98 系統調用、47 系統調用、9

T\_DIR、95 T\_FILE、98 線程、27 雷霆群、82 滴答聲、67 滴答聲、67 分時、10、21 上半部分、53 TRAMPOLINE、45 蹦床、27、45 事務、85 轉換後備緩衝區 （TLB）、32、36 傳輸完成、54 陷阱、43

trapframe, 27
type cast, 37


UART, 53
undefined behavior, 104
unlink, 90
user memory, 26
user mode, 23
user space, 9, 23
usertrap, 72
ustack, 41
uvmalloc, 40, 41


valid, 87
vector, 43
virtio_disk_rw, 87, 88
virtual address, 26


wait, 11, 12, 79
wait channel, 76
wakeup, 65, 76, 78
walk, 36
walkaddr, 40
write, 90, 97
writei, 91, 94, 95


yield, 72, 73


ZOMBIE, 80


