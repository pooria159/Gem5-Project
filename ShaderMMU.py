from m5.defines import buildEnv
from m5.params import *
from m5.proxy import *
from m5.util import fatal
from ClockedObject import ClockedObject

class ShaderMMU(ClockedObject):
    type = 'ShaderMMU'
    cxx_class = 'ShaderMMU'
    cxx_header = "gpu/shader_mmu.hh"

    if buildEnv['TARGET_ISA'] == 'x86':
        from X86TLB import X86TLB
        pagewalkers = VectorParam.X86TLB("wrapped TLB")
    elif buildEnv['TARGET_ISA'] == 'arm':
        from ArmTLB import ArmTLB
        pagewalkers = VectorParam.ArmTLB("wrapped TLB")
        stage2_mmu = Param.ArmStage2MMU("Stage 2 MMU for port")
    else:
        fatal('ShaderMMU only supports x86 and ARM architectures currently')

    latency = Param.Int(20, "Round trip latency for requests from L1 TLBs")

    l2_tlb_entries = Param.Int(0, "Number of entries in the L2 TLB (0=>no L2)")
    l2_tlb_assoc = Param.Int(4, "Associativity of the L2 TLB (0 => full)")

    prefetch_buffer_size = Param.Int(0, "Size of the prefetch buffer")

    def setUpPagewalkers(self, num, port, bypass_l1):
        if buildEnv['TARGET_ISA'] == 'arm':
            from ArmTLB import ArmTLB, ArmStage2DMMU
            self.stage2_mmu = ArmStage2DMMU(tlb = ArmTLB())
        tlbs = []
        for i in range(num):
            # set to only a single entry here so that all requests are misses
            if buildEnv['TARGET_ISA'] == 'x86':
                from X86TLB import X86TLB
                t = X86TLB(size=1)
                t.walker.bypass_l1 = bypass_l1
            elif buildEnv['TARGET_ISA'] == 'arm':
                t = ArmTLB(size=1)
                # ArmTLB does not yet include bypass_l1 option
            else:
                fatal('ShaderMMU only supports x86 and ARM architectures ' \
                      'currently')
            t.walker.port = port
            tlbs.append(t)
        self.pagewalkers = tlbs
