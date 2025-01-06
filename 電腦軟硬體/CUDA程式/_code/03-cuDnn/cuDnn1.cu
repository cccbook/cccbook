#include <stdio.h>
#include <cudnn.h>
#include <cuda_runtime.h>
#include <stdlib.h>

// 錯誤檢查巨集
#define CHECK_CUDA(call) \
do { \
    cudaError_t status = call; \
    if (status != cudaSuccess) { \
        printf("CUDA Error at line %d: %s\n", __LINE__, cudaGetErrorString(status)); \
        exit(1); \
    } \
} while(0)

#define CHECK_CUDNN(call) \
do { \
    cudnnStatus_t status = call; \
    if (status != CUDNN_STATUS_SUCCESS) { \
        printf("CUDNN Error at line %d: %s\n", __LINE__, cudnnGetErrorString(status)); \
        exit(1); \
    } \
} while(0)

int main() {
    // 初始化 cuDNN
    cudnnHandle_t cudnn;
    CHECK_CUDNN(cudnnCreate(&cudnn));

    // 設定輸入參數
    const int batch_size = 1;
    const int in_channels = 3;  // RGB 輸入
    const int in_height = 32;
    const int in_width = 32;
    const int out_channels = 32;  // 輸出特徵圖數量
    const int kernel_size = 3;    // 3x3 卷積核
    const int pad = 1;           // 填充大小
    const int stride = 1;        // 步長
    
    // 計算輸出維度
    const int out_height = (in_height + 2 * pad - kernel_size) / stride + 1;
    const int out_width = (in_width + 2 * pad - kernel_size) / stride + 1;

    // 設定張量描述符
    cudnnTensorDescriptor_t input_descriptor;
    CHECK_CUDNN(cudnnCreateTensorDescriptor(&input_descriptor));
    CHECK_CUDNN(cudnnSetTensor4dDescriptor(input_descriptor,
                                         CUDNN_TENSOR_NCHW,
                                         CUDNN_DATA_FLOAT,
                                         batch_size, in_channels, in_height, in_width));

    cudnnTensorDescriptor_t output_descriptor;
    CHECK_CUDNN(cudnnCreateTensorDescriptor(&output_descriptor));
    CHECK_CUDNN(cudnnSetTensor4dDescriptor(output_descriptor,
                                         CUDNN_TENSOR_NCHW,
                                         CUDNN_DATA_FLOAT,
                                         batch_size, out_channels, out_height, out_width));

    // 設定卷積描述符
    cudnnFilterDescriptor_t kernel_descriptor;
    CHECK_CUDNN(cudnnCreateFilterDescriptor(&kernel_descriptor));
    CHECK_CUDNN(cudnnSetFilter4dDescriptor(kernel_descriptor,
                                         CUDNN_DATA_FLOAT,
                                         CUDNN_TENSOR_NCHW,
                                         out_channels, in_channels, kernel_size, kernel_size));

    cudnnConvolutionDescriptor_t convolution_descriptor;
    CHECK_CUDNN(cudnnCreateConvolutionDescriptor(&convolution_descriptor));
    CHECK_CUDNN(cudnnSetConvolution2dDescriptor(convolution_descriptor,
                                              pad, pad,           // 上下左右填充
                                              stride, stride,     // 垂直水平步長
                                              1, 1,              // dilation
                                              CUDNN_CROSS_CORRELATION,
                                              CUDNN_DATA_FLOAT));

    // 分配記憶體
    float *d_input, *d_output, *d_kernel;
    const int input_size = batch_size * in_channels * in_height * in_width;
    const int output_size = batch_size * out_channels * out_height * out_width;
    const int kernel_size_total = out_channels * in_channels * kernel_size * kernel_size;

    CHECK_CUDA(cudaMalloc(&d_input, input_size * sizeof(float)));
    CHECK_CUDA(cudaMalloc(&d_output, output_size * sizeof(float)));
    CHECK_CUDA(cudaMalloc(&d_kernel, kernel_size_total * sizeof(float)));

    // 選擇卷積演算法
    cudnnConvolutionFwdAlgoPerf_t conv_algo;
    int returnedAlgoCount;
    CHECK_CUDNN(cudnnGetConvolutionForwardAlgorithm_v7(
        cudnn,
        input_descriptor,
        kernel_descriptor,
        convolution_descriptor,
        output_descriptor,
        1,  // requested algo count
        &returnedAlgoCount,
        &conv_algo
    ));

    // 為工作空間分配記憶體
    size_t workspace_size;
    CHECK_CUDNN(cudnnGetConvolutionForwardWorkspaceSize(
        cudnn,
        input_descriptor,
        kernel_descriptor,
        convolution_descriptor,
        output_descriptor,
        conv_algo.algo,
        &workspace_size
    ));

    void* d_workspace;
    CHECK_CUDA(cudaMalloc(&d_workspace, workspace_size));

    // 執行卷積運算
    float alpha = 1.0f, beta = 0.0f;
    CHECK_CUDNN(cudnnConvolutionForward(
        cudnn,
        &alpha,
        input_descriptor, d_input,
        kernel_descriptor, d_kernel,
        convolution_descriptor,
        conv_algo.algo,
        d_workspace, workspace_size,
        &beta,
        output_descriptor, d_output
    ));

    // 清理資源
    CHECK_CUDA(cudaFree(d_workspace));
    CHECK_CUDA(cudaFree(d_input));
    CHECK_CUDA(cudaFree(d_output));
    CHECK_CUDA(cudaFree(d_kernel));
    
    CHECK_CUDNN(cudnnDestroyTensorDescriptor(input_descriptor));
    CHECK_CUDNN(cudnnDestroyTensorDescriptor(output_descriptor));
    CHECK_CUDNN(cudnnDestroyFilterDescriptor(kernel_descriptor));
    CHECK_CUDNN(cudnnDestroyConvolutionDescriptor(convolution_descriptor));
    CHECK_CUDNN(cudnnDestroy(cudnn));

    return 0;
}

// 編譯命令：
// nvcc -o cudnn_example cudnn_example.cu -lcudnn