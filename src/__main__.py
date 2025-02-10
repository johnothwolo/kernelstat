#!/usr/bin/env python3

from macholib.MachO import MachO
from macholib import mach_o
import sys
import struct
import re
import os

xnu_version_pattern = re.compile(r'Darwin Kernel Version \d+\.\d+\.\d+.*?[A-Z]*_[A-Z0-9_]+')

class KernelMacho(MachO):

    def __init__(self, filename):

        # supports the ObjectGraph protocol
        self.graphident = filename
        self.filename = filename
        self.loader_path = os.path.dirname(filename)
        self.allow_unknown_load_commands = False

        # initialized by load
        self.fat = None
        self.headers = []
        self.file = open(filename, "rb")
        self.load(self.file)

    def uname(self):
        for header in self.headers:
            for (lc, segment, sections) in header.commands:
                if isinstance(segment, mach_o.segment_command_64) or isinstance(segment, mach_o.segment_command):
                    for section in sections:
                        sect_name = section.sectname.decode("utf-8").rstrip("\x00")
                        seg_name = section.segname.decode("utf-8").rstrip("\x00")
                        if seg_name == mach_o.SEG_TEXT and sect_name == "__const":
                            self.file.seek(section.offset)
                            section_data = self.file.read(section.size)
                            # Search for the kernel version using regex
                            match = xnu_version_pattern.search(section_data.decode("utf-8", errors="ignore"))
                            if match:
                                return match.group(0)
        raise Exception("Kernel version not found")


if __name__ == "__main__":
    # Default macOS kernel path
    # kernel_path = "/System/Library/Kernels/kernel"

    if len(sys.argv) > 1:
        kernel_path = sys.argv[1]
    else:
        raise BaseException("Usage kernel_stat kerne-file")
    try:
        print(KernelMacho(kernel_path).uname())
    except Exception as e:
        print("Error: {}".format(e))
