## 常用的 Linux 命令和用法

以下是一些常用的 Linux 命令及其用法：

1. cd：改變當前工作目錄。例如，cd ~ 會將工作目錄更改為當前用戶的家目錄。

2. ls：列出當前目錄中的所有文件和子目錄。例如，ls -l會以長格式列出文件。

3. pwd：顯示當前工作目錄的完整路徑名。

4. man：顯示關於指定命令的手冊頁面。例如，man ls將顯示有關ls命令的詳細信息。

5. mkdir：創建新目錄。例如，mkdir mydirectory將創建一個名為mydirectory的新目錄。

6. rm：刪除文件或目錄。例如，rm myfile.txt將刪除名為myfile.txt的文件。

7. cp：復制文件或目錄。例如，cp myfile.txt myotherfile.txt將復制名為myfile.txt的文件並將其命名為myotherfile.txt。

8. mv：移動文件或目錄或將文件或目錄重命名。例如，mv myfile.txt mydirectory/將移動名為myfile.txt的文件到名為mydirectory的目錄中。

9. cat：顯示文件的內容。例如，cat myfile.txt將顯示名為myfile.txt的文件的內容。

10. chmod：更改文件或目錄的權限。例如，chmod 777 myfile.txt將使名為myfile.txt的文件對所有用戶都具有讀取，寫入和執行權限。

以下是一個簡單的C語言程式，可以將字符串反轉：

```
#include <stdio.h>
#include <string.h>

void reverse(char *str) {
    int i, j;
    char temp;
    for (i = 0, j = strlen(str) - 1; i < j; i++, j--) {
        temp = str[i];
        str[i] = str[j];
        str[j] = temp;
    }
}

int main() {
    char str[100];
    printf("Enter a string: ");
    scanf("%s", str);
    reverse(str);
    printf("Reversed string is: %s\n", str);
    return 0;
}
```