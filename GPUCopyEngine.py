from MemObject import MemObject
from ShaderTLB import ShaderTLB
from m5.defines import buildEnv
from m5.params import *
from m5.proxy import *

class GPUCopyEngine(MemObject):
    type = 'GPUCopyEngine'
    cxx_class = 'GPUCopyEngine'
    cxx_header = "gpu/copy_engine.hh"

    host_port = MasterPort("The copy engine port to host coherence domain")
    device_port = MasterPort("The copy engine port to device coherence domain")
    driver_delay = Param.Int(0, "memcpy launch delay in ticks");
    sys = Param.System(Parent.any, "system sc will run on")
    # @TODO: This will need to be removed when CUDA syscalls manage copies
    
    gpu = Param.CudaGPU(Parent.any, "The GPU")

    cache_line_size = Param.Unsigned(Parent.cache_line_size, "Cache line size in bytes")
    buffering = Param.Unsigned(0, "The maximum cache lines that the copy engine"
                                "can buffer (0 implies effectively infinite)")

    host_dtb = Param.ShaderTLB(ShaderTLB(access_host_pagetable = True), "TLB for the host memory space")
    device_dtb = Param.ShaderTLB(ShaderTLB(), "TLB for the device memory space")

    id = Param.Int(-1, "ID of the CE")
    stats_filename = Param.String("ce_stats.txt",
        "file to which copy engine dumps its stats")
