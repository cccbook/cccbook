import ctypes

# 模擬 C 程式中的緩衝區溢出
def buffer_overflow():
    buffer_size = 10
    # 使用 ctypes 模擬一個固定大小的緩衝區
    buffer = ctypes.create_string_buffer(buffer_size)
    
    try:
        # 嘗試將超過緩衝區大小的數據寫入
        buffer.value = b"A" * 20  # 超過緩衝區大小，這將觸發溢出
        print("Buffer:", buffer.value)
    except Exception as e:
        print("Error:", e)

buffer_overflow()
