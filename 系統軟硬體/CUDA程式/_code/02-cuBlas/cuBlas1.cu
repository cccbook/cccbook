#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>

// 用於錯誤檢查的輔助函數
#define CHECK_CUDA(call) \
do { \
    cudaError_t err = call; \
    if (err != cudaSuccess) { \
        printf("CUDA error at %s %d: %s\n", __FILE__, __LINE__, \
               cudaGetErrorString(err)); \
        exit(EXIT_FAILURE); \
    } \
} while (0)

#define CHECK_CUBLAS(call) \
do { \
    cublasStatus_t status = call; \
    if (status != CUBLAS_STATUS_SUCCESS) { \
        printf("cuBLAS error at %s %d\n", __FILE__, __LINE__); \
        exit(EXIT_FAILURE); \
    } \
} while (0)

int main() {
    // 初始化維度和常數
    const int m = 4;  // 矩陣行數
    const int n = 4;  // 矩陣列數
    const float alpha = 1.0f;
    const float beta = 0.0f;

    // 分配主機記憶體
    float *h_A = (float*)malloc(m * n * sizeof(float));
    float *h_B = (float*)malloc(m * n * sizeof(float));
    float *h_C = (float*)malloc(m * n * sizeof(float));

    // 初始化矩陣 A 和 B
    for (int i = 0; i < m * n; i++) {
        h_A[i] = 1.0f;  // A 矩陣填入 1.0
        h_B[i] = 2.0f;  // B 矩陣填入 2.0
    }

    // 分配設備記憶體
    float *d_A, *d_B, *d_C;
    CHECK_CUDA(cudaMalloc((void**)&d_A, m * n * sizeof(float)));
    CHECK_CUDA(cudaMalloc((void**)&d_B, m * n * sizeof(float)));
    CHECK_CUDA(cudaMalloc((void**)&d_C, m * n * sizeof(float)));

    // 將數據從主機複製到設備
    CHECK_CUDA(cudaMemcpy(d_A, h_A, m * n * sizeof(float), cudaMemcpyHostToDevice));
    CHECK_CUDA(cudaMemcpy(d_B, h_B, m * n * sizeof(float), cudaMemcpyHostToDevice));

    // 創建並初始化 CUBLAS 上下文
    cublasHandle_t handle;
    CHECK_CUBLAS(cublasCreate(&handle));

    // 執行矩陣乘法: C = α * A * B + β * C
    CHECK_CUBLAS(cublasSgemm(handle,
                            CUBLAS_OP_N,    // A 矩陣不轉置
                            CUBLAS_OP_N,    // B 矩陣不轉置
                            m,              // A 和 C 的行數
                            n,              // B 和 C 的列數
                            n,              // A 的列數和 B 的行數
                            &alpha,         // α 標量
                            d_A,            // A 矩陣
                            m,              // A 的主要維度
                            d_B,            // B 矩陣
                            n,              // B 的主要維度
                            &beta,          // β 標量
                            d_C,            // C 矩陣
                            m));            // C 的主要維度

    // 將結果從設備複製回主機
    CHECK_CUDA(cudaMemcpy(h_C, d_C, m * n * sizeof(float), cudaMemcpyDeviceToHost));

    // 輸出結果
    printf("結果矩陣：\n");
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            printf("%f ", h_C[i * n + j]);
        }
        printf("\n");
    }

    // 清理資源
    CHECK_CUBLAS(cublasDestroy(handle));
    CHECK_CUDA(cudaFree(d_A));
    CHECK_CUDA(cudaFree(d_B));
    CHECK_CUDA(cudaFree(d_C));
    free(h_A);
    free(h_B);
    free(h_C);

    return 0;
}

// 編譯命令：
// nvcc -o cublas_example cublas_example.cu -lcublas