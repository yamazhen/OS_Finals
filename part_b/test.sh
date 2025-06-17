#!/bin/bash
echo "Part B Demonstration"
echo "===================="

make all

echo "1. Page Faults:"
/usr/bin/time -v ./page_faults

echo -e "\n2. TLB Effects:"
./tlb_effects

echo -e "\n3. Copy-on-Write:"
./cow

echo -e "\n4. Thrashing (Ctrl+C to stop):"
./thrashing
