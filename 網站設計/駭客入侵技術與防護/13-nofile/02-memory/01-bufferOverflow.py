import ctypes

# 模擬一個緩衝區溢出情況
def buffer_overflow():
    # 在 C 語言中，這是 C-style 字符串
    buffer = ctypes.create_string_buffer(10)  # 預留10個字節的空間
    print("Initial buffer:", buffer.raw)

    # 嘗試寫入超過緩衝區大小的數據，會導致緩衝區溢出
    ctypes.memmove(buffer, b"A" * 20, 20)  # 寫入20個字節，超出10個字節的緩衝區

    print("Buffer after overflow:", buffer.raw)

buffer_overflow()
