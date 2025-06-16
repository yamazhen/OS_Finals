import os
import random
import time
from collections import defaultdict

import matplotlib.pyplot as plt

from tlb import TLB


class Simulator:
    def __init__(self):
        self.page_size = 4096
        self.tlb_size = 4
    
    def clear_screen(self):
        os.system('clear')
    
    def virtual_to_physical(self, virtual_address, page_table, tlb):
        page_number = virtual_address // self.page_size
        offset = virtual_address % self.page_size
        
        frame_number = tlb.lookup(page_number)
        tlb_miss = frame_number is None
        
        if frame_number is None:
            if page_number in page_table:
                frame_number = page_table[page_number]
                tlb.update(page_number, frame_number)
            else:
                return None, None, True
        
        physical_address = frame_number * self.page_size + offset
        return physical_address, frame_number, tlb_miss
    
    def generate_virtual_addresses(self, reference_string):
        addresses = []
        for page in reference_string:
            offset = random.randint(0, self.page_size - 1)
            virtual_addr = page * self.page_size + offset
            addresses.append(virtual_addr)
        return addresses
    
    def visual_demonstration(self, reference_string, frame_size, algorithm_name):
        print(f"\n{'='*80}")
        print(f"VISUAL DEMONSTRATION: {algorithm_name.upper()} ALGORITHM WITH TLB")
        print(f"{'='*80}")
        print(f"Reference String: {reference_string}")
        print(f"Frame Size: {frame_size}")
        print(f"TLB Size: {self.tlb_size}")
        print(f"Page Size: {self.page_size} bytes")
        print(f"{'='*80}")
        
        virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        if algorithm_name.lower() == 'fifo':
            faults, steps = self.fifo_algorithm(reference_string, frame_size, virtual_addresses)
        elif algorithm_name.lower() == 'lru':
            faults, steps = self.lru_algorithm(reference_string, frame_size, virtual_addresses)
        elif algorithm_name.lower() == 'optimal':
            faults, steps = self.optimal_algorithm(reference_string, frame_size, virtual_addresses)
        elif algorithm_name.lower() == 'clock':
            faults, steps = self.clock_algorithm(reference_string, frame_size, virtual_addresses)
        else:
            faults, steps = self.custom_algorithm(reference_string, frame_size, virtual_addresses)
        
        print(f"\nStep-by-step execution:")
        print(f"{'Step':<4} {'Page':<4} {'Virtual':<10} {'Physical':<10} {'Memory Frames':<20} {'Status':<12} {'TLB'}")
        print("-" * 85)
        
        for i, step in enumerate(steps):
            frame_visual = "["
            for j in range(frame_size):
                if j < len(step['frames']):
                    frame_visual += f" {step['frames'][j]} "
                else:
                    frame_visual += " - "
                if j < frame_size - 1:
                    frame_visual += "|"
            frame_visual += "]"
            
            status = "PAGE FAULT" if step['fault'] else "PAGE HIT"
            tlb_status = "TLB MISS" if step['tlb_miss'] else "TLB HIT"
            
            virtual_addr = f"0x{step['virtual_addr']:08X}" if step['virtual_addr'] else "N/A"
            physical_addr = f"0x{step['physical_addr']:08X}" if step['physical_addr'] else "N/A"
            
            print(f"{i+1:<4} {step['page']:<4} {virtual_addr:<10} {physical_addr:<10} {frame_visual:<20} {status:<12} {tlb_status}")
            
            time.sleep(0.5)
        
        tlb = steps[-1]['tlb'] if steps else None
        if tlb:
            print(f"\nTLB STATISTICS:")
            print(f"TLB Hits: {tlb.hits}")
            print(f"TLB Misses: {tlb.misses}")
            print(f"TLB Hit Ratio: {tlb.get_hit_ratio():.1f}%")
        
        print(f"\nSUMMARY:")
        print(f"Total Page Faults: {faults}")
        print(f"Total Page Hits: {len(steps) - faults}")
        print(f"Page Hit Ratio: {(len(steps) - faults)/len(steps)*100:.1f}%")
    
    def animated_demonstration(self, reference_string, frame_size):
        self.clear_screen()
        print(f"\n{'='*100}")
        print("ANIMATED COMPARISON: ALL ALGORITHMS WITH TLB")
        print(f"{'='*100}")
        print(f"Reference String: {reference_string}")
        print(f"Frame Size: {frame_size}")
        print(f"TLB Size: {self.tlb_size}")
        print(f"{'='*100}")
        
        results = self.simulate_all(reference_string, frame_size)
        
        print(f"\n{'Step':<4} {'Page':<4} {'FIFO':<18} {'LRU':<18} {'Optimal':<18} {'Custom':<18} {'Clock':<18}")
        print("-" * 100)  
        
        max_steps = len(reference_string)
        
        for i in range(max_steps):
            page = reference_string[i]
            
            representations = {}
            for alg_name, data in results.items():
                step = data['steps'][i]
                frame_visual = "["
                for j in range(frame_size):
                    if j < len(step['frames']):
                        frame_visual += f"{step['frames'][j]}"
                    else:
                        frame_visual += "-"
                    if j < frame_size - 1:
                        frame_visual += "|"
                frame_visual += "]"
                
                if step['fault']:
                    frame_visual += "*F"
                else:
                    frame_visual += " H"
                
                if step['tlb_miss']:
                    frame_visual += "T"
                else:
                    frame_visual += " "
                    
                representations[alg_name] = frame_visual
            
            print(f"{i+1:<4} {page:<4} {representations['FIFO']:<18} {representations['LRU']:<18} {representations['Optimal']:<18} {representations['Custom']:<18} {representations['Clock']:<18}")
            time.sleep(0.8)
        
        print(f"\nLegend: *F = Page Fault, H = Page Hit, T = TLB Miss, - = Empty Slot")
        print(f"\nFINAL RESULTS:")
        for alg_name, data in results.items():
            tlb_ratio = data['tlb'].get_hit_ratio() if data['tlb'] else 0
            print(f"{alg_name}: {data['faults']} page faults, TLB hit ratio: {tlb_ratio:.1f}%")
        
        return results
    
    def fifo_algorithm(self, reference_string, frame_size, virtual_addresses=None):
        if virtual_addresses is None:
            virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        frames = []
        page_table = {}
        tlb = TLB(self.tlb_size)
        page_faults = 0
        steps = []
        
        for i, page in enumerate(reference_string):
            virtual_addr = virtual_addresses[i]
            
            if page in page_table:
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': False,
                    'tlb_miss': tlb_miss,
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
            else:
                page_faults += 1
                
                if len(frames) < frame_size:
                    
                    frames.append(page)
                    frame_number = len(frames) - 1
                    page_table[page] = frame_number
                else:
                    
                    old_page = frames.pop(0)
                    frames.append(page)
                    
                    
                    old_frame = page_table[old_page]
                    del page_table[old_page]
                    tlb.invalidate(old_page)
                    page_table[page] = old_frame
                
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': True,
                    'tlb_miss': True,  
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
        
        return page_faults, steps
    
    def lru_algorithm(self, reference_string, frame_size, virtual_addresses=None):
        if virtual_addresses is None:
            virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        frames = []
        page_table = {}
        tlb = TLB(self.tlb_size)
        page_faults = 0
        steps = []
        
        for i, page in enumerate(reference_string):
            virtual_addr = virtual_addresses[i]
            
            if page in page_table:
                
                frames.remove(page)
                frames.append(page)
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': False,
                    'tlb_miss': tlb_miss,
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
            else:
                
                page_faults += 1
                
                if len(frames) < frame_size:
                    
                    frames.append(page)
                    frame_number = len(frames) - 1
                    page_table[page] = frame_number
                else:
                    
                    lru_page = frames.pop(0)
                    frames.append(page)
                    
                    
                    old_frame = page_table[lru_page]
                    del page_table[lru_page]
                    tlb.invalidate(lru_page)
                    page_table[page] = old_frame
                
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': True,
                    'tlb_miss': True,  
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
        
        return page_faults, steps
    
    def optimal_algorithm(self, reference_string, frame_size, virtual_addresses=None):
        if virtual_addresses is None:
            virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        frames = []
        page_table = {}
        tlb = TLB(self.tlb_size)
        page_faults = 0
        steps = []
        
        for i, page in enumerate(reference_string):
            virtual_addr = virtual_addresses[i]
            
            if page in page_table:
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': False,
                    'tlb_miss': tlb_miss,
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
            else:
                
                page_faults += 1
                
                if len(frames) < frame_size:
                    
                    frames.append(page)
                    frame_number = len(frames) - 1
                    page_table[page] = frame_number
                else:
                    
                    farthest = -1
                    page_to_remove = frames[0]
                    
                    for frame_page in frames:
                        try:
                            next_use = reference_string[i+1:].index(frame_page)
                        except ValueError:
                            next_use = float('inf')
                        
                        if next_use > farthest:
                            farthest = next_use
                            page_to_remove = frame_page
                    
                    
                    frame_index = frames.index(page_to_remove)
                    frames[frame_index] = page
                    
                    
                    old_frame = page_table[page_to_remove]
                    del page_table[page_to_remove]
                    tlb.invalidate(page_to_remove)
                    page_table[page] = old_frame
                
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': True,
                    'tlb_miss': True,  
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
        
        return page_faults, steps
    
    def custom_algorithm(self, reference_string, frame_size, virtual_addresses=None):
        if virtual_addresses is None:
            virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        frames = []
        page_table = {}
        tlb = TLB(self.tlb_size)
        page_faults = 0
        steps = []
        frequency = defaultdict(int)
        access_time = {}
        
        for i, page in enumerate(reference_string):
            virtual_addr = virtual_addresses[i]
            frequency[page] += 1
            
            if page in page_table:
                
                access_time[page] = i
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': False,
                    'tlb_miss': tlb_miss,
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
            else:
                
                page_faults += 1
                access_time[page] = i
                
                if len(frames) < frame_size:
                    
                    frames.append(page)
                    frame_number = len(frames) - 1
                    page_table[page] = frame_number
                else:
                    
                    highest_score = -1
                    page_to_remove = frames[0]
                    
                    for frame_page in frames:
                        last_access = access_time.get(frame_page, 0)
                        freq = frequency[frame_page]
                        age = i - last_access
                        score = age / freq if freq > 0 else float('inf')
                        
                        if score > highest_score:
                            highest_score = score
                            page_to_remove = frame_page
                    
                    
                    frame_index = frames.index(page_to_remove)
                    frames[frame_index] = page
                    
                    
                    old_frame = page_table[page_to_remove]
                    del page_table[page_to_remove]
                    tlb.invalidate(page_to_remove)
                    page_table[page] = old_frame
                
                
                physical_addr, frame_number, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page, 
                    'frames': frames.copy(), 
                    'fault': True,
                    'tlb_miss': True,  
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb
                })
    
        return page_faults, steps

    def clock_algorithm(self, reference_string, frame_size, virtual_addresses=None):
        if virtual_addresses is None:
            virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        frames = []  
        reference_bits = []  
        page_table = {}  
        tlb = TLB(self.tlb_size)
        page_faults = 0
        steps = []
        clock_hand = 0
        
        for i, page in enumerate(reference_string):
            virtual_addr = virtual_addresses[i]
            
            if page in page_table:
                frame_index = page_table[page]
                reference_bits[frame_index] = 1
                
                physical_addr, _, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': False,
                    'tlb_miss': tlb_miss,
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb,
                    'clock_hand': clock_hand,
                    'reference_bits': reference_bits.copy()
                })
            else:
                page_faults += 1
                
                if len(frames) < frame_size:
                    frames.append(page)
                    reference_bits.append(1)  
                    page_table[page] = len(frames) - 1
                else:
                    replaced = False
                    
                    while not replaced:
                        if reference_bits[clock_hand] == 0:
                            victim_page = frames[clock_hand]
                            
                            frames[clock_hand] = page
                            reference_bits[clock_hand] = 1  
                            
                            if victim_page in page_table:
                                del page_table[victim_page]
                            tlb.invalidate(victim_page)
                            page_table[page] = clock_hand
                            
                            clock_hand = (clock_hand + 1) % frame_size
                            replaced = True
                        else:
                            reference_bits[clock_hand] = 0
                            clock_hand = (clock_hand + 1) % frame_size
                
                physical_addr, _, tlb_miss = self.virtual_to_physical(virtual_addr, page_table, tlb)
                steps.append({
                    'page': page,
                    'frames': frames.copy(),
                    'fault': True,
                    'tlb_miss': True,
                    'virtual_addr': virtual_addr,
                    'physical_addr': physical_addr,
                    'tlb': tlb,
                    'clock_hand': clock_hand,
                    'reference_bits': reference_bits.copy()
                })
        
        return page_faults, steps
    
    def simulate_all(self, reference_string, frame_size):
        results = {}
        
        virtual_addresses = self.generate_virtual_addresses(reference_string)
        
        fifo_faults, fifo_steps = self.fifo_algorithm(reference_string, frame_size, virtual_addresses)
        results['FIFO'] = {'faults': fifo_faults, 'steps': fifo_steps, 'tlb': fifo_steps[-1]['tlb'] if fifo_steps else None}
        
        lru_faults, lru_steps = self.lru_algorithm(reference_string, frame_size, virtual_addresses)
        results['LRU'] = {'faults': lru_faults, 'steps': lru_steps, 'tlb': lru_steps[-1]['tlb'] if lru_steps else None}
        
        optimal_faults, optimal_steps = self.optimal_algorithm(reference_string, frame_size, virtual_addresses)
        results['Optimal'] = {'faults': optimal_faults, 'steps': optimal_steps, 'tlb': optimal_steps[-1]['tlb'] if optimal_steps else None}
        
        custom_faults, custom_steps = self.custom_algorithm(reference_string, frame_size, virtual_addresses)
        results['Custom'] = {'faults': custom_faults, 'steps': custom_steps, 'tlb': custom_steps[-1]['tlb'] if custom_steps else None}

        clock_faults, clock_steps = self.clock_algorithm(reference_string, frame_size, virtual_addresses)
        results['Clock'] = {'faults': clock_faults, 'steps': clock_steps, 'tlb': clock_steps[-1]['tlb'] if clock_steps else None}
        
        return results
    
    def print_results(self, results, reference_string):
        self.clear_screen()
        print("\n" + "="*80)
        print("PAGE REPLACEMENT SIMULATION RESULTS WITH ADDRESS TRANSLATION")
        print("="*80)
        print(f"Reference String: {reference_string}")
        print(f"TLB Size: {self.tlb_size}")
        print(f"Page Size: {self.page_size} bytes")
        print("="*80)
        
        for alg_name, data in results.items():
            print(f"\n{alg_name} Algorithm:")
            print("-" * 50)
            print("Step | Page | Virtual   | Physical  | Frames | P.Fault | TLB")
            print("-" * 50)
            
            for i, step in enumerate(data['steps']):
                fault_str = "YES" if step['fault'] else "NO"
                tlb_str = "MISS" if step['tlb_miss'] else "HIT"
                frames_str = str(step['frames']).replace('[', '').replace(']', '').replace(',', '')
                virtual_str = f"0x{step['virtual_addr']:08X}" if step['virtual_addr'] else "N/A"
                physical_str = f"0x{step['physical_addr']:08X}" if step['physical_addr'] else "N/A"
                
                print(f"{i+1:4} | {step['page']:4} | {virtual_str} | {physical_str} | {frames_str:10} | {fault_str:7} | {tlb_str}")
            
            tlb = data['tlb']
            if tlb:
                print(f"\nPage Faults: {data['faults']}")
                print(f"TLB Hits: {tlb.hits}")
                print(f"TLB Misses: {tlb.misses}")
                print(f"TLB Hit Ratio: {tlb.get_hit_ratio():.1f}%")
    
    def plot_comparison(self, results):
        algorithms = list(results.keys())
        page_faults = [results[alg]['faults'] for alg in algorithms]
        tlb_hit_ratios = [results[alg]['tlb'].get_hit_ratio() if results[alg]['tlb'] else 0 for alg in algorithms]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        
        ax1.bar(algorithms, page_faults, color=colors)
        ax1.set_title('Page Faults Comparison')
        ax1.set_ylabel('Number of Page Faults')
        
        ax2.bar(algorithms, tlb_hit_ratios, color=colors)
        ax2.set_title('TLB Hit Ratio Comparison')
        ax2.set_ylabel('TLB Hit Ratio (%)')
        ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        print("Graph displayed. Press Enter in terminal to close...")
        plt.show(block=False)

        input()
        plt.close(fig)
        plt.close('all')
        plt.clf()
        plt.cla()
