from m5.params import *
from m5.proxy import *
from BaseTLB import BaseTLB

class ShaderTLB(BaseTLB):
    type = 'ShaderTLB'
    cxx_class = 'ShaderTLB'
    cxx_header = "gpu/shader_tlb.hh"

    access_host_pagetable = Param.Bool(False, \
                "Whether to allow accesses to host page table")
    gpu = Param.CudaGPU(Parent.any, "The GPU")

    entries = Param.Int(0, "number entries in TLB (0 implies infinite)")

    associativity = Param.Int(4, "Number of sets in the TLB")

    hit_latency = Param.Cycles(1, "number of cycles for a hit")

