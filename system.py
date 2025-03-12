from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
from m5.objects import *

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.resources.resource import BinaryResource

requires(ISA.X86)

spectre_workload = BinaryResource(
    local_path="spectre",
    id="x86-spectre-static"
)

class X86TAGE(BaseCPUProcessor):
    class X86Core(BaseCPUCore):
        def __init__(self, core_id: int, branchPred):
            cpu = X86O3CPU(branchPred=branchPred)
            super().__init__(core=cpu, isa=ISA.X86)

    def __init__(self, num_cores):
        super().__init__(cores=[X86TAGE.X86Core(i, branchPred=LTAGE()) for i in range(num_cores)])

# Simple processor
processor = X86TAGE(num_cores=1)
# Simple cache hierarchy
cache = PrivateL1CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB")
# Simple memory module
memory = SingleChannelDDR3_1600(size="8GiB")

# Link everything together in your board
board = SimpleBoard(
    clk_freq="3GHz",
    cache_hierarchy=cache,
    processor=processor,
    memory=memory,
)

# Check out https://resources.gem5.org for more things to run
# NOTE run this to check everything
# board.set_se_binary_workload(obtain_resource("x86-hello64-static"))
# NOTE run this for your experiments
board.set_se_binary_workload(spectre_workload)

# Set up the simulation (This is where you would set up the checkpoints)
simulator = Simulator(
    board=board,
)

# Run it all
simulator.run()
