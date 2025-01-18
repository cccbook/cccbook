#include <stdio.h>
#include <npp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>

// 錯誤檢查巨集
#define CHECK_NPP(call) \
do { \
    NppStatus status = call; \
    if (status != NPP_SUCCESS) { \
        printf("NPP Error at %s %d: %d\n", __FILE__, __LINE__, status); \
        exit(EXIT_FAILURE); \
    } \
} while(0)

int main() {
    // 設定影像參數
    const int width = 640;
    const int height = 480;
    const int channels = 3;  // RGB 影像
    const int step = width * channels;
    
    // 分配主機記憶體
    Npp8u* h_input = (Npp8u*)malloc(width * height * channels);
    Npp8u* h_output = (Npp8u*)malloc(width * height * channels);
    
    // 初始化輸入影像（這裡只是示範，實際應用中應該載入真實影像）
    for (int i = 0; i < width * height * channels; i++) {
        h_input[i] = (Npp8u)(i % 256);
    }
    
    // 分配設備記憶體
    Npp8u* d_input;
    Npp8u* d_output;
    Npp8u* d_temp;  // 用於中間處理結果
    
    cudaMalloc((void**)&d_input, width * height * channels);
    cudaMalloc((void**)&d_output, width * height * channels);
    cudaMalloc((void**)&d_temp, width * height * channels);
    
    // 複製輸入影像到設備
    cudaMemcpy(d_input, h_input, width * height * channels, cudaMemcpyHostToDevice);
    
    // 創建 ROI (Region of Interest)
    NppiSize roi = {width, height};
    
    // 1. 高斯模糊
    NppiMaskSize maskSize = NPP_MASK_SIZE_5_X_5;
    CHECK_NPP(nppiFilterGauss_8u_C3R(
        d_input,
        step,
        d_temp,
        step,
        roi,
        maskSize));
    
    // 2. 調整亮度和對比度
    const Npp32f brightness = 10.0f;
    const Npp32f contrast = 1.2f;
    CHECK_NPP(nppiColorTwist32f_8u_C3R(
        d_temp,
        step,
        d_output,
        step,
        roi,
        contrast, brightness, 1.0f, 0.0f));  // contrast, brightness, hue, saturation
    
    // 3. 執行中值濾波
    CHECK_NPP(nppiFilterMedian_8u_C3R(
        d_output,
        step,
        d_temp,
        step,
        roi,
        NPP_MASK_SIZE_3_X_3));
    
    // 4. 銳化處理
    Npp32f kernel[9] = {
        -1.0f, -1.0f, -1.0f,
        -1.0f,  9.0f, -1.0f,
        -1.0f, -1.0f, -1.0f
    };
    CHECK_NPP(nppiFilter32f_8u_C3R(
        d_temp,
        step,
        d_output,
        step,
        roi,
        kernel,
        {3, 3},     // 核大小
        {1, 1},     // 錨點
        NPP_BORDER_REPLICATE));
    
    // 5. 色彩空間轉換: RGB 轉 HSV
    Npp8u* d_hsv;
    cudaMalloc((void**)&d_hsv, width * height * channels);
    CHECK_NPP(nppiRGBToHSV_8u_C3R(
        d_output,
        step,
        d_hsv,
        step,
        roi));
    
    // 6. 直方圖均衡化（只處理 V 通道）
    Npp8u* d_v_channel;
    cudaMalloc((void**)&d_v_channel, width * height);
    
    // 分離 V 通道
    CHECK_NPP(nppiCopy_8u_C3C1R(
        d_hsv + 2,  // V 在第三個通道
        step,
        d_v_channel,
        width,
        roi));
    
    // 執行直方圖均衡化
    CHECK_NPP(nppiEqualizeHist_8u_C1R(
        d_v_channel,
        width,
        d_v_channel,
        width,
        roi));
    
    // 將處理後的 V 通道放回
    CHECK_NPP(nppiCopy_8u_C1C3R(
        d_v_channel,
        width,
        d_hsv + 2,
        step,
        roi));
    
    // 7. HSV 轉回 RGB
    CHECK_NPP(nppiHSVToRGB_8u_C3R(
        d_hsv,
        step,
        d_output,
        step,
        roi));
    
    // 複製結果回主機
    cudaMemcpy(h_output, d_output, width * height * channels, cudaMemcpyDeviceToHost);
    
    // 清理資源
    cudaFree(d_input);
    cudaFree(d_output);
    cudaFree(d_temp);
    cudaFree(d_hsv);
    cudaFree(d_v_channel);
    free(h_input);
    free(h_output);
    
    return 0;
}

// 編譯命令：
// nvcc -o npp_example npp_example.cu -lnppc -lnppi -lnppif -lnppig