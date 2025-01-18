<?php
    $page = $_GET['page'];  // 用戶控制的參數
    include($page);         // 包含並執行該文件
?>


攻擊者

<?php
    system('id');  // 執行操作系統命令
?>

禁用遠程文件包含（RFI）


allow_url_include = Off

2. 使用絕對文件路徑


<?php
    $page = $_GET['page'];
    $allowed_pages = ['home.php', 'about.php', 'contact.php'];
    
    if (in_array($page, $allowed_pages)) {
        include($page);
    } else {
        echo "Page not found.";
    }
?>

3. 對用戶輸入進行驗證和過濾

<?php
    $page = $_GET['page'];
    
    // 只允許包含特定文件
    if (preg_match('/^[a-zA-Z0-9_-]+\.php$/', $page)) {
        include($page);
    } else {
        echo "Invalid page.";
    }
?>
