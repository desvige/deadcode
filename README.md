# deadcode
Detect unused functions from an ELF binary.

### Usage

    objdump --disassembly <elf-binary> > dump
    objdump --reloc <elf-binary> > relo
    ./deadcode.py dump relo
    cat dead.txt
