// 範例 1: 向量加法
__global__ void vectorAdd(float* a, float* b, float* c, int n) {
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

// 範例 2: 矩陣乘法
__global__ void matrixMul(float* a, float* b, float* c, int width) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    float sum = 0.0f;
    if (row < width && col < width) {
        for (int i = 0; i < width; i++) {
            sum += a[row * width + i] * b[i * width + col];
        }
        c[row * width + col] = sum;
    }
}

// 主程式示範如何使用這些 kernel
int main() {
    // 設定數據大小
    int N = 1024;
    size_t size = N * sizeof(float);
    
    // 分配主機記憶體
    float *h_a, *h_b, *h_c;
    h_a = (float*)malloc(size);
    h_b = (float*)malloc(size);
    h_c = (float*)malloc(size);
    
    // 初始化數據
    for (int i = 0; i < N; i++) {
        h_a[i] = rand() / (float)RAND_MAX;
        h_b[i] = rand() / (float)RAND_MAX;
    }
    
    // 分配設備記憶體
    float *d_a, *d_b, *d_c;
    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_c, size);
    
    // 複製數據到設備
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);
    
    // 設定 kernel 配置
    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
    
    // 啟動 kernel
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, N);
    
    // 複製結果回主機
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);
    
    // 清理記憶體
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    free(h_a);
    free(h_b);
    free(h_c);
    
    return 0;
}

// 範例 3: 使用共享記憶體的矩陣乘法
#define TILE_WIDTH 16

__global__ void matrixMulShared(float* a, float* b, float* c, int width) {
    __shared__ float ds_A[TILE_WIDTH][TILE_WIDTH];
    __shared__ float ds_B[TILE_WIDTH][TILE_WIDTH];
    
    int bx = blockIdx.x;
    int by = blockIdx.y;
    int tx = threadIdx.x;
    int ty = threadIdx.y;
    
    int row = by * TILE_WIDTH + ty;
    int col = bx * TILE_WIDTH + tx;
    
    float sum = 0.0f;
    
    for (int m = 0; m < width/TILE_WIDTH; ++m) {
        // 載入數據到共享記憶體
        ds_A[ty][tx] = a[row * width + (m * TILE_WIDTH + tx)];
        ds_B[ty][tx] = b[(m * TILE_WIDTH + ty) * width + col];
        __syncthreads();
        
        // 計算部分乘積
        for (int k = 0; k < TILE_WIDTH; ++k) {
            sum += ds_A[ty][k] * ds_B[k][tx];
        }
        __syncthreads();
    }
    
    if (row < width && col < width) {
        c[row * width + col] = sum;
    }
}