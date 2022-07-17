
"""
Align sequence reads
"""


import subprocess
from pathlib import Path
import os

from latch import small_task, medium_task, large_task, large_gpu_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional


@large_gpu_task
def align_task(ref: LatchFile, read1:LatchFile, read2: LatchFile, output_dir: LatchDir) -> LatchFile:

    out_basename = str(output_dir.remote_path)
    outname = Path(str(os.path.basename(read1.local_path))).stem

    _index_cmd = [
      "bwa-mem2",
       "index",
       ref.local_path
    ]
    
    _align_cmd = [
        "bwa-mem2",
         "mem",
         "-o",
          "out.sam",
          ref.local_path,
          read1.local_path, 
          read2.local_path
    ]
    
    
    subprocess.run(_index_cmd)
    subprocess.run(_align_cmd)
    
    return LatchFile(f"out.sam",f"{out_basename}/{outname}.sam" )


@workflow
def bwamem2(ref: LatchFile, read1:LatchFile, read2: LatchFile, output_dir: LatchDir) -> LatchFile:
    """Align reads to a genome

#BWA-MEM2

BWA-MEM2 is a software package for mapping DNA sequences against a 
large reference genome. Bwa-mem2 is the next version of the bwa-mem 
algorithm in bwa. It produces alignment identical to bwa and 
is ~1.3-3.1x faster depending on the use-case, dataset and the running machine.

For more information visit the BWA-MEM2 [Github](https://github.com/bwa-mem2/bwa-mem2). 


__metadata__:
        display_name: bwa-mem2
        author:
            name: Corey Howe
            email: coreyhowe99 at gmail dot com
            github: https://github.com/coreyhowe/latch_hicqc
        repository: https://github.com/phasegenomics/hic_qc
        license:
            id: 

Args:

        ref:
          Reference Genome Fasta Sequence 

          __metadata__:
            display_name: Reference Genome Fasta 
        
        read1:
          Sequence File - Read1

          __metadata__:
            display_name: Sequence file 1 
        
        read2:
          Sequence File - Read2

          __metadata__:
            display_name: Sequence file 2 
            
        output_dir:
          Output directory

          __metadata__:
            display_name: Output directory
    """
    return align_task(ref=ref,read1=read1,read2=read2,output_dir=output_dir)
