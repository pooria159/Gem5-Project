from MemObject import MemObject
from ShaderTLB import ShaderTLB
from m5.params import *

class ShaderLSQ(MemObject):
    type = 'ShaderLSQ'
    cxx_class = 'ShaderLSQ'
    cxx_header = "gpu/shader_lsq.hh"

    cache_port = MasterPort("The data cache port for this LSQ")

    lane_port = VectorSlavePort("the ports back to the shader core")

    data_tlb = Param.ShaderTLB(ShaderTLB(), "Data TLB")

    control_port = SlavePort("The control port for this LSQ")

    inject_width = Param.Int(1, "Max requests sent to L1 per cycle")
    eject_width = Param.Int(1, "Max cache lines to receive per cycle")

    warp_size = Param.Int(32, "Size of the warp")
    cache_line_size = Param.Int("Cache line size in bytes")
    subline_bytes = Param.Int(32, "Bytes per cache subline (e.g. Fermi = 32")
    warp_contexts = Param.Int(48, "Number of warps possible per GPU core")
    num_warp_inst_buffers = Param.Int(64, "Maximum number of in-flight warp instructions")
    atoms_per_subline = Param.Int(3, "Maximum atomic ops to send per cache subline in a single access (Fermi = 3)")

    # Notes: Fermi back-to-back dependent warp load L1 hits are 19 SM cycles
    # GPGPU-Sim models 5 cycles between LSQ completion and next issued load
    latency = Param.Cycles(14, "Cycles of latency for single uncontested L1 hit")
    l1_tag_cycles = Param.Cycles(4, "Cycles of latency L1 tag access")

    # currently only VI_hammer cache protocol supports flushing.
    # In VI_hammer only the L1 is flushed.
    forward_flush = Param.Bool("Issue a flush all to caches whenever the LSQ is flushed")
