# 附錄：LLVM的API和文檔

## LLVM的C++ API和命令行接口的使用方法和範例

以下是LLVM的C++ API和命令行接口的使用方法和範例：

### C++ API
LLVM的C++ API提供了一個方便的方式來創建、修改和使用LLVM IR。這裡是一個簡單的示例，展示如何使用LLVM API來創建一個簡單的函數，將兩個整數相加：

```cpp
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Verifier.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

int main() {
  LLVMContext context;
  Module* module = new Module("test", context);

  FunctionType* funcType = FunctionType::get(Type::getInt32Ty(context), {Type::getInt32Ty(context), Type::getInt32Ty(context)}, false);
  Function* func = Function::Create(funcType, Function::ExternalLinkage, "add", module);
  BasicBlock* bb = BasicBlock::Create(context, "entry", func);
  IRBuilder<> builder(bb);

  Value* x = &*(func->arg_begin());
  Value* y = &*(++(func->arg_begin()));

  Value* result = builder.CreateAdd(x, y);
  builder.CreateRet(result);

  verifyFunction(*func);
  module->print(outs(), nullptr);

  delete module;
  return 0;
}

```

### 命令行接口

LLVM還提供了一個命令行接口，可以通過命令行將LLVM IR轉換為目標代碼。以下是一個示例，展示如何使用命令行接口將LLVM IR編譯為本機代碼：

```
$ llvm-as hello.ll -o hello.bc
$ llc hello.bc -o hello.s
$ gcc hello.s -o hello

```

這將生成一個可執行文件"hello"，該文件包含由LLVM IR生成的本機代碼。

## LLVM的文檔和資源的整理和介紹

以下是LLVM的一些文檔和資源，供參考：

* 官方網站：http://llvm.org/
* 官方文檔：http://llvm.org/docs/
* 官方API文檔：http://llvm.org/docs/doxygen/html/index.html
* LLVM社區：https://discourse.llvm.org/
* LLVM IR指令參考：http://llvm.org/docs/LangRef.html
* LLVM IR設計原則：http://llvm.org/docs/ProgrammersManual.html#the-llvm-ir-design-principles
* LLVM教程：http://llvm.org/docs/tutorial/
* LLVM開發者指南：https://mlir.llvm.org/getting_started/DeveloperGuide/
* LLVM開發者會議錄像：http://llvm.org/devmtg/
* LLVM GitHub存儲庫：https://github.com/llvm/llvm-project


這些文檔和資源提供了豐富的信息和示例，可以幫助開發人員學習和使用LLVM編譯器。