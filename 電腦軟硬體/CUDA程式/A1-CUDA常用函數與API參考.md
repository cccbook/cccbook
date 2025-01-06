### A1 - CUDA 常用函數與 API 參考

CUDA 程式設計提供了豐富的函數和 API 來實現各種 GPU 加速的操作。以下是一些常用的 CUDA 函數和 API，涵蓋了從內存管理到計算任務的各個方面。

#### 1. **內存管理函數**

- **`cudaMalloc`**
  - 用於在 GPU 上分配內存。
  ```cpp
  cudaError_t cudaMalloc(void** devPtr, size_t size);
  ```

- **`cudaFree`**
  - 用於釋放在 GPU 上分配的內存。
  ```cpp
  cudaError_t cudaFree(void* devPtr);
  ```

- **`cudaMemcpy`**
  - 用於在主機（CPU）與裝置（GPU）之間進行同步內存拷貝。
  ```cpp
  cudaError_t cudaMemcpy(void* dst, const void* src, size_t count, cudaMemcpyKind kind);
  ```

- **`cudaMemcpyAsync`**
  - 用於在主機與裝置之間進行異步內存拷貝。
  ```cpp
  cudaError_t cudaMemcpyAsync(void* dst, const void* src, size_t count, cudaMemcpyKind kind, cudaStream_t stream);
  ```

- **`cudaHostAlloc`**
  - 用於分配主機內存，這部分內存可以被用來進行異步拷貝。
  ```cpp
  cudaError_t cudaHostAlloc(void** pHost, size_t size, unsigned int flags);
  ```

#### 2. **錯誤處理函數**

- **`cudaGetErrorString`**
  - 返回最近的 CUDA 錯誤消息。
  ```cpp
  const char* cudaGetErrorString(cudaError_t error);
  ```

- **`cudaGetLastError`**
  - 返回最後一次 CUDA 錯誤。
  ```cpp
  cudaError_t cudaGetLastError();
  ```

#### 3. **核函數（Kernel）執行控制**

- **`cudaLaunchKernel`**
  - 用於啟動指定的 CUDA 核心函數。
  ```cpp
  cudaError_t cudaLaunchKernel(const void* func, dim3 gridDim, dim3 blockDim, void** args, size_t sharedMem, cudaStream_t stream);
  ```

- **`cudaDeviceSynchronize`**
  - 同步主機與設備，等待所有 GPU 計算完成。
  ```cpp
  cudaError_t cudaDeviceSynchronize();
  ```

#### 4. **流與事件管理**

- **`cudaStreamCreate`**
  - 創建一個新的 CUDA 流。
  ```cpp
  cudaError_t cudaStreamCreate(cudaStream_t* stream);
  ```

- **`cudaStreamDestroy`**
  - 銷毀指定的 CUDA 流。
  ```cpp
  cudaError_t cudaStreamDestroy(cudaStream_t stream);
  ```

- **`cudaEventCreate`**
  - 創建一個新的 CUDA 事件。
  ```cpp
  cudaError_t cudaEventCreate(cudaEvent_t* event);
  ```

- **`cudaEventRecord`**
  - 記錄一個 CUDA 事件。
  ```cpp
  cudaError_t cudaEventRecord(cudaEvent_t event, cudaStream_t stream);
  ```

- **`cudaEventSynchronize`**
  - 等待指定的 CUDA 事件發生。
  ```cpp
  cudaError_t cudaEventSynchronize(cudaEvent_t event);
  ```

#### 5. **設備管理函數**

- **`cudaGetDevice`**
  - 返回當前使用的 CUDA 設備 ID。
  ```cpp
  cudaError_t cudaGetDevice(int* device);
  ```

- **`cudaSetDevice`**
  - 設定當前使用的 CUDA 設備。
  ```cpp
  cudaError_t cudaSetDevice(int device);
  ```

- **`cudaGetDeviceProperties`**
  - 獲取指定設備的屬性（如顯示記憶體大小、核心數量等）。
  ```cpp
  cudaError_t cudaGetDeviceProperties(cudaDeviceProp* prop, int device);
  ```

#### 6. **數學與運算庫**

- **`cuBLAS`（BLAS 服務）**
  - CUDA 基本線性代數子程序庫，提供矩陣運算的加速。
  - 例如：`cublasSgemm` 用於矩陣乘法。

- **`cuFFT`（快速傅里葉變換）**
  - 用於執行傅里葉變換運算的 CUDA 庫。
  - 例如：`cufftExecC2C` 用於執行 2D 複數到複數的傅里葉變換。

- **`cuSolver`（線性代數解算器）**
  - 用於求解線性系統和奇異值分解（SVD）的 CUDA 函數。
  - 例如：`cusolverDnSgesv` 用於解線性方程組。

#### 7. **原子操作**

- **`atomicAdd`**
  - 對一個變數執行原子加法操作。
  ```cpp
  __device__ int atomicAdd(int* address, int val);
  ```

- **`atomicExch`**
  - 執行原子交換操作。
  ```cpp
  __device__ int atomicExch(int* address, int val);
  ```

- **`atomicMax`**
  - 對一個變數執行原子最大值更新。
  ```cpp
  __device__ int atomicMax(int* address, int val);
  ```

#### 8. **計算與性能優化**

- **`cudaDeviceGetAttribute`**
  - 獲取 CUDA 設備的屬性，像是記憶體大小、運算能力等。
  ```cpp
  cudaError_t cudaDeviceGetAttribute(int* value, cudaDeviceAttr attr, int device);
  ```

- **`cudaFuncSetCacheConfig`**
  - 設置 CUDA 核心函數的快取配置。
  ```cpp
  cudaError_t cudaFuncSetCacheConfig(cudaFunction_t func, cudaFuncCache cacheConfig);
  ```

#### 9. **錯誤處理**

- **`cudaError_t`**
  - CUDA 錯誤類型，用來表示函數執行過程中發生的錯誤。通過該返回值，開發者可以獲得錯誤信息並進行錯誤處理。
  ```cpp
  typedef enum cudaError
  {
      cudaSuccess = 0,
      cudaErrorInvalidValue = 1,
      cudaErrorMemoryAllocation = 2,
      ...
  } cudaError_t;
  ```

### 結論

以上列舉的是一些常見的 CUDA 函數和 API，涵蓋了從內存管理、錯誤處理、核函數執行到性能優化等多個方面。使用這些 API 時，開發者可以靈活運用 CUDA 設備的計算與內存資源來實現高效的 GPU 加速計算。在進行 CUDA 程式設計時，熟悉這些函數將有助於提高開發效率並優化性能。