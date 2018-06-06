# deadcode
Detect unused functions from an ELF binary.

### Usage

    objdump --disassemble <elf-binary> > dump
    objdump --reloc <elf-binary> > relo
    ./deadcode.py dump relo
    cat dead.txt
