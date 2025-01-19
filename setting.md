本專案書籍，大部分都是用 ChatGPT 寫的，ChatGPT 預設支援的 markdown 是 brackets style ，所以請安裝

https://marketplace.visualstudio.com/items?itemName=goessner.mdmath

然後設定 mdmath.delimiters 為 "brackets"

```json
{
    "haskell.manageHLS": "GHCup",
    "mdmath.delimiters": "brackets",
    "mdmath.autosave": true,
    "editor.pasteAs.preferences": [
        
    ]
}
```
