#include <cuda.h>
#include "nvcodec/NvDecoder/NvDecoder.h"
#include <iostream>
#include <fstream>
#include <vector>

class VideoDecoder {
private:
    CUcontext cuContext = nullptr;
    NvDecoder* decoder = nullptr;
    std::ifstream inputFile;
    std::vector<uint8_t> fileData;
    int width, height;
    int frameCount = 0;

public:
    VideoDecoder(const char* filename) {
        // 初始化 CUDA
        CHECK_CUDA(cuInit(0));
        
        // 創建 CUDA context
        CUdevice cuDevice = 0;
        CHECK_CUDA(cuDeviceGet(&cuDevice, 0));
        CHECK_CUDA(cuCtxCreate(&cuContext, 0, cuDevice));

        // 打開輸入檔案
        inputFile.open(filename, std::ios::in | std::ios::binary);
        if (!inputFile.is_open()) {
            throw std::runtime_error("無法開啟輸入檔案");
        }

        // 讀取檔案內容
        inputFile.seekg(0, std::ios::end);
        size_t fileSize = inputFile.tellg();
        inputFile.seekg(0, std::ios::beg);
        fileData.resize(fileSize);
        inputFile.read(reinterpret_cast<char*>(fileData.data()), fileSize);

        // 創建解碼器
        decoder = new NvDecoder(cuContext, false, cudaVideoCodec_H264);
    }

    ~VideoDecoder() {
        if (decoder) {
            delete decoder;
        }
        if (cuContext) {
            cuCtxDestroy(cuContext);
        }
        if (inputFile.is_open()) {
            inputFile.close();
        }
    }

    void decode() {
        uint8_t* pVideo = nullptr;
        int nVideoBytes = 0;
        int nFrameReturned = 0;
        uint8_t** ppFrame;

        // 解碼整個檔案
        decoder->Decode(fileData.data(), fileData.size(), &ppFrame, &nFrameReturned);

        // 獲取幀的資訊
        width = decoder->GetWidth();
        height = decoder->GetHeight();
        frameCount += nFrameReturned;

        std::cout << "解碼完成：\n";
        std::cout << "影片寬度: " << width << "\n";
        std::cout << "影片高度: " << height << "\n";
        std::cout << "總幀數: " << frameCount << "\n";
    }

    void saveFrame(int frameIndex, const char* outputFilename) {
        if (frameIndex >= frameCount) {
            throw std::runtime_error("幀索引超出範圍");
        }

        // 獲取指定幀
        uint8_t** ppFrame = decoder->GetFrame(frameIndex);
        int nPitch = decoder->GetDeviceFramePitch();

        // 分配主機記憶體
        std::vector<uint8_t> frameData(height * width * 3 / 2);  // NV12 格式

        // 從設備記憶體複製到主機記憶體
        CUDA_MEMCPY2D m = { 0 };
        m.srcMemoryType = CU_MEMORYTYPE_DEVICE;
        m.srcDevice = (CUdeviceptr)ppFrame[0];
        m.srcPitch = nPitch;
        m.dstMemoryType = CU_MEMORYTYPE_HOST;
        m.dstHost = frameData.data();
        m.dstPitch = width;
        m.WidthInBytes = width;
        m.Height = height * 3 / 2;  // 包含 Y 和 UV 平面
        CHECK_CUDA(cuMemcpy2D(&m));

        // 保存為檔案
        std::ofstream outFile(outputFilename, std::ios::binary);
        outFile.write(reinterpret_cast<char*>(frameData.data()), frameData.size());
        outFile.close();
    }

    // 獲取影片資訊
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    int getFrameCount() const { return frameCount; }
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "用法: " << argv[0] << " <輸入視頻檔案>\n";
        return 1;
    }

    try {
        // 創建解碼器
        VideoDecoder decoder(argv[1]);

        // 執行解碼
        decoder.decode();

        // 保存第一幀作為範例
        decoder.saveFrame(0, "frame0.raw");

        std::cout << "解碼成功，第一幀已保存為 frame0.raw\n";
    }
    catch (const std::exception& e) {
        std::cerr << "錯誤: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

// 編譯命令：
// nvcc -o video_decoder video_decoder.cpp -I<NVIDIA Video Codec SDK path> -L<NVIDIA Video Codec SDK path>/Lib/linux/stubs/x86_64 -lnvcuvid -lcuda