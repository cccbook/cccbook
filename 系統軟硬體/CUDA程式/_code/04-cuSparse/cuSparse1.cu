#include <cuda_runtime.h>
#include <cusparse.h>
#include <stdio.h>

// 錯誤檢查巨集
#define CHECK_CUDA(call) \
do { \
    cudaError_t err = call; \
    if (err != cudaSuccess) { \
        printf("CUDA error at %s %d: %s\n", __FILE__, __LINE__, \
               cudaGetErrorString(err)); \
        exit(EXIT_FAILURE); \
    } \
} while(0)

#define CHECK_CUSPARSE(call) \
do { \
    cusparseStatus_t err = call; \
    if (err != CUSPARSE_STATUS_SUCCESS) { \
        printf("cuSPARSE error at %s %d: %s\n", __FILE__, __LINE__, \
               cusparseGetErrorString(err)); \
        exit(EXIT_FAILURE); \
    } \
} while(0)

int main() {
    // 初始化 cuSPARSE
    cusparseHandle_t handle;
    CHECK_CUSPARSE(cusparseCreate(&handle));

    // 定義矩陣參數
    const int num_rows = 4;
    const int num_cols = 4;
    const int nnz = 9;  // 非零元素數量

    // CSR 格式的稀疏矩陣數據
    // 示例矩陣:
    // 5 2 0 0
    // 0 3 7 0
    // 0 0 4 1
    // 1 0 0 6
    
    int h_csrRows[5] = {0, 2, 4, 6, 9};  // 行偏移
    int h_csrCols[9] = {0, 1,            // 列索引
                        1, 2,
                        2, 3,
                        0, 3};
    float h_csrVals[9] = {5, 2,          // 非零值
                          3, 7,
                          4, 1,
                          1, 6};
    
    // 密集向量 x = [1, 2, 3, 4]
    float h_x[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    float h_y[4] = {0.0f};  // 輸出向量

    // 分配設備記憶體
    int *d_csrRows, *d_csrCols;
    float *d_csrVals, *d_x, *d_y;

    CHECK_CUDA(cudaMalloc(&d_csrRows, (num_rows + 1) * sizeof(int)));
    CHECK_CUDA(cudaMalloc(&d_csrCols, nnz * sizeof(int)));
    CHECK_CUDA(cudaMalloc(&d_csrVals, nnz * sizeof(float)));
    CHECK_CUDA(cudaMalloc(&d_x, num_cols * sizeof(float)));
    CHECK_CUDA(cudaMalloc(&d_y, num_rows * sizeof(float)));

    // 複製數據到設備
    CHECK_CUDA(cudaMemcpy(d_csrRows, h_csrRows, (num_rows + 1) * sizeof(int),
                         cudaMemcpyHostToDevice));
    CHECK_CUDA(cudaMemcpy(d_csrCols, h_csrCols, nnz * sizeof(int),
                         cudaMemcpyHostToDevice));
    CHECK_CUDA(cudaMemcpy(d_csrVals, h_csrVals, nnz * sizeof(float),
                         cudaMemcpyHostToDevice));
    CHECK_CUDA(cudaMemcpy(d_x, h_x, num_cols * sizeof(float),
                         cudaMemcpyHostToDevice));

    // 創建矩陣描述符
    cusparseSpMatDescr_t matA;
    cusparseDnVecDescr_t vecX, vecY;
    
    CHECK_CUSPARSE(cusparseCreateCsr(&matA, num_rows, num_cols, nnz,
                                    d_csrRows, d_csrCols, d_csrVals,
                                    CUSPARSE_INDEX_32I, CUSPARSE_INDEX_32I,
                                    CUSPARSE_INDEX_BASE_ZERO, CUDA_R_32F));
    
    CHECK_CUSPARSE(cusparseCreateDnVec(&vecX, num_cols, d_x, CUDA_R_32F));
    CHECK_CUSPARSE(cusparseCreateDnVec(&vecY, num_rows, d_y, CUDA_R_32F));

    // 分配緩衝區
    size_t bufferSize = 0;
    CHECK_CUSPARSE(cusparseSpMV_bufferSize(
        handle, CUSPARSE_OPERATION_NON_TRANSPOSE,
        &(float){1.0f}, matA, vecX, &(float){0.0f}, vecY,
        CUDA_R_32F, CUSPARSE_SPMV_ALG_DEFAULT, &bufferSize));

    void* buffer = nullptr;
    CHECK_CUDA(cudaMalloc(&buffer, bufferSize));

    // 執行 SpMV: y = alpha * A * x + beta * y
    CHECK_CUSPARSE(cusparseSpMV(
        handle, CUSPARSE_OPERATION_NON_TRANSPOSE,
        &(float){1.0f}, matA, vecX, &(float){0.0f}, vecY,
        CUDA_R_32F, CUSPARSE_SPMV_ALG_DEFAULT, buffer));

    // 將結果複製回主機
    CHECK_CUDA(cudaMemcpy(h_y, d_y, num_rows * sizeof(float),
                         cudaMemcpyDeviceToHost));

    // 輸出結果
    printf("Result vector y:\n");
    for (int i = 0; i < num_rows; i++) {
        printf("%f\n", h_y[i]);
    }

    // 清理資源
    CHECK_CUSPARSE(cusparseDestroySpMat(matA));
    CHECK_CUSPARSE(cusparseDestroyDnVec(vecX));
    CHECK_CUSPARSE(cusparseDestroyDnVec(vecY));
    CHECK_CUSPARSE(cusparseDestroy(handle));
    
    CHECK_CUDA(cudaFree(buffer));
    CHECK_CUDA(cudaFree(d_csrRows));
    CHECK_CUDA(cudaFree(d_csrCols));
    CHECK_CUDA(cudaFree(d_csrVals));
    CHECK_CUDA(cudaFree(d_x));
    CHECK_CUDA(cudaFree(d_y));

    return 0;
}

// 編譯命令：
// nvcc -o cusparse_example cusparse_example.cu -lcusparse