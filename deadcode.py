#!/usr/bin/python

import os, re, subprocess, sys

#-------------------------------------------------------------------------------
# Disassemble
#-------------------------------------------------------------------------------

def Disassemble(elf_binary):
  filename = elf_binary + ".asm"
  os.system("objdump --disassemble " + elf_binary + " > " + filename)
  with open(filename, "r") as file:
    return file.readlines()

#-------------------------------------------------------------------------------
# GetCalledFunctions
#-------------------------------------------------------------------------------

def GetCalledFunctions(asm):
  fns = set()
  for line in asm:
    match = re.search('call.* <(.*)>$', line)
    if match:
      fn = RemovePltIfNeeded(match.group(1))
      fns.add(fn)

  return fns;

#-------------------------------------------------------------------------------
# GetFunctionNames
#-------------------------------------------------------------------------------

def GetFunctionNames(asm):
  fns = set()
  for line in asm:
    match = re.search('^\w+ <(.*)>:$', line)
    if match:
      fn = RemovePltIfNeeded(match.group(1))
      if not IsCompilerFunction(fn) and not IsRuntimeFunction(fn):
        fns.add(fn)

  return fns;

#-------------------------------------------------------------------------------
# GetReferencedFunctions
#-------------------------------------------------------------------------------

def GetReferencedFunctions(relocs):
  fns = set()
  for line in relocs:
    match = re.search('  (\w+)$', line)
    if match:
      fn = match.group(1)
      fns.add(fn)

  return fns;

#-------------------------------------------------------------------------------
# GetRelocations
#-------------------------------------------------------------------------------

def GetRelocations(elf_bin):
  filename = elf_bin + ".relocs"
  os.system("objdump --dynamic-reloc " + elf_bin + " > " + filename)
  with open(filename, "r") as file:
    return file.readlines()

#-------------------------------------------------------------------------------
# IsCompilerFunction
#-------------------------------------------------------------------------------

def IsCompilerFunction(fn):
  return re.search('^\_\_', fn)

#-------------------------------------------------------------------------------
# IsRuntimeFunction
#-------------------------------------------------------------------------------

def IsRuntimeFunction(fn):
  runtime_fns = set([
      '.plt', '_fini', '_init', '_start', 'deregister_tm_clones', 'frame_dummy',
      'main', 'register_tm_clones'])

  return (fn in runtime_fns)

#-------------------------------------------------------------------------------
# RemovePltIfNeeded
#-------------------------------------------------------------------------------

def RemovePltIfNeeded(symbol):
  match = re.search('^(\w+)@plt$', symbol)
  if match:
    symbol = match.group(1)

  return symbol;

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

elf_bin = sys.argv[1]
asm = Disassemble(elf_bin)
relocs = GetRelocations(elf_bin)

all_fns = GetFunctionNames(asm)
called_fns = GetCalledFunctions(asm)
refd_fns = GetReferencedFunctions(relocs)

used_fns = called_fns.union(refd_fns)
dead_fns = all_fns.difference(used_fns)

for fn in dead_fns:
  print(fn)
