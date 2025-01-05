// main.cpp
#include <optix.h>
#include <optix_stubs.h>
#include <cuda_runtime.h>
#include <vector>
#include <iostream>

// 光線生成程式
const char* const ptx_code = R"(
  #include <optix.h>
  
  extern "C" __global__ void __raygen__rg() {
    // 計算像素座標
    const uint3 idx = optixGetLaunchIndex();
    const uint3 dim = optixGetLaunchDimensions();
    const float2 pixel = make_float2(idx.x, idx.y) / make_float2(dim.x, dim.y);
    
    // 產生光線
    float3 origin = make_float3(0.0f, 0.0f, -1.0f);
    float3 direction = normalize(make_float3(pixel.x - 0.5f, pixel.y - 0.5f, 1.0f));
    
    // 追蹤光線
    optixTrace(
        optixGetTraversableHandle(),    // 場景
        origin,                         // 起點
        direction,                      // 方向
        0.0f,                          // tmin
        1e16f,                         // tmax
        0.0f,                          // 光線時間
        OptixVisibilityMask(1),        // 可見性遮罩
        OPTIX_RAY_FLAG_NONE,           // 光線旗標
        0,                             // SBT offset
        1,                             // SBT stride
        0,                             // missSBTIndex
        u0, u1, u2);                   // 傳遞給最近命中著色器的數據
  }

  extern "C" __global__ void __miss__ms() {
    // 未命中時設定背景顏色
    optixSetPayload_0(float_as_int(0.0f));
    optixSetPayload_1(float_as_int(0.0f));
    optixSetPayload_2(float_as_int(0.0f));
  }

  extern "C" __global__ void __closesthit__ch() {
    // 設定命中點的顏色
    const float3 hitPoint = optixGetWorldRayOrigin() + optixGetRayTmax() * optixGetWorldRayDirection();
    const float3 normal = normalize(hitPoint);
    
    // 簡單的漫反射著色
    const float3 lightDir = normalize(make_float3(1.0f, 1.0f, 1.0f));
    const float diff = max(dot(normal, lightDir), 0.0f);
    
    optixSetPayload_0(float_as_int(diff));
    optixSetPayload_1(float_as_int(diff));
    optixSetPayload_2(float_as_int(diff));
  }
)";

int main() {
    // 初始化 OptiX
    OPTIX_CHECK(optixInit());
    
    // 創建 CUDA context
    CUcontext cuCtx = nullptr;
    CUdevice cuDevice = 0;
    CUDA_CHECK(cuInit(0));
    CUDA_CHECK(cuDeviceGet(&cuDevice, 0));
    CUDA_CHECK(cuCtxCreate(&cuCtx, 0, cuDevice));
    
    // 創建 OptiX context
    OptixDeviceContext context = nullptr;
    OPTIX_CHECK(optixDeviceContextCreate(cuCtx, nullptr, &context));
    
    // 編譯 PTX 代碼
    OptixModule module = nullptr;
    OptixPipelineCompileOptions pipeline_compile_options = {};
    OptixModuleCompileOptions module_compile_options = {};
    
    OPTIX_CHECK(optixModuleCreateFromPTX(
        context,
        &module_compile_options,
        &pipeline_compile_options,
        ptx_code,
        strlen(ptx_code),
        nullptr,
        nullptr,
        &module));
    
    // 創建程式群組
    OptixProgramGroup raygen_prog_group = nullptr;
    OptixProgramGroup miss_prog_group = nullptr;
    OptixProgramGroup hitgroup_prog_group = nullptr;
    
    OptixProgramGroupOptions program_group_options = {};
    
    OptixProgramGroupDesc raygen_prog_group_desc = {};
    raygen_prog_group_desc.kind = OPTIX_PROGRAM_GROUP_KIND_RAYGEN;
    raygen_prog_group_desc.raygen.module = module;
    raygen_prog_group_desc.raygen.entryFunctionName = "__raygen__rg";
    
    OPTIX_CHECK(optixProgramGroupCreate(
        context,
        &raygen_prog_group_desc,
        1,
        &program_group_options,
        nullptr,
        nullptr,
        &raygen_prog_group));
    
    // 創建管線
    std::vector<OptixProgramGroup> program_groups;
    program_groups.push_back(raygen_prog_group);
    
    OptixPipelineLinkOptions pipeline_link_options = {};
    pipeline_link_options.maxTraceDepth = 1;
    
    OptixPipeline pipeline = nullptr;
    OPTIX_CHECK(optixPipelineCreate(
        context,
        &pipeline_compile_options,
        &pipeline_link_options,
        program_groups.data(),
        program_groups.size(),
        nullptr,
        nullptr,
        &pipeline));
    
    // 創建 Shader Binding Table (SBT)
    CUdeviceptr raygen_record;
    const size_t raygen_record_size = sizeof(RayGenSbtRecord);
    CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&raygen_record), raygen_record_size));
    
    RayGenSbtRecord rg_sbt;
    OPTIX_CHECK(optixSbtRecordPackHeader(raygen_prog_group, &rg_sbt));
    CUDA_CHECK(cudaMemcpy(
        reinterpret_cast<void*>(raygen_record),
        &rg_sbt,
        raygen_record_size,
        cudaMemcpyHostToDevice));
    
    OptixShaderBindingTable sbt = {};
    sbt.raygenRecord = raygen_record;
    
    // 執行光線追蹤
    OPTIX_CHECK(optixLaunch(
        pipeline,
        0,
        sbt,
        512,  // 寬度
        512,  // 高度
        1     // 深度
    ));
    
    // 清理資源
    CUDA_CHECK(cudaFree(reinterpret_cast<void*>(raygen_record)));
    OPTIX_CHECK(optixProgramGroupDestroy(raygen_prog_group));
    OPTIX_CHECK(optixModuleDestroy(module));
    OPTIX_CHECK(optixPipelineDestroy(pipeline));
    OPTIX_CHECK(optixDeviceContextDestroy(context));
    CUDA_CHECK(cuCtxDestroy(cuCtx));
    
    return 0;
}