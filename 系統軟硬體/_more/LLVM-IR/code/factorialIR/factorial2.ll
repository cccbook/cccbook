define i32 @factorial(i32 %n) {
  %result = alloca i32
  store i32 1, i32* %result
  br label %loop

loop:
  %current = load i32, i32* %result
  %cmp = icmp sgt i32 %n, 1
  br i1 %cmp, label %body, label %exit

body:
  %next = mul i32 %n, %current
  store i32 %next, i32* %result
  %prev = sub i32 %n, 1
  store i32 %prev, i32* %n
  br label %loop

exit:
  %final_result = load i32, i32* %result
  ret i32 %final_result
}