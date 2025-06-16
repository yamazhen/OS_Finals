from simulator import Simulator


def main():
    simulator = Simulator()
    simulator.clear_screen()
    
    print("PAGE FAULT SIMULATION SYSTEM")
    print("Operating Systems Assignment")
    print("="*40)
    
    try:
        while True:
            print("\nOptions:")
            print("1. Custom input")
            print("2. Test cases")
            print("3. Visual demonstration (single algorithm)")
            print("4. Animated comparison (all algorithms)")
            print("5. Exit")
            
            choice = input("Choose option (1-5): ")
            
            if choice == '1':
                try:
                    simulator.clear_screen()
                    ref_input = input("Enter reference string (space-separated): ")
                    reference_string = list(map(int, ref_input.split()))
                    frame_size = int(input("Enter frame size: "))
                    
                    results = simulator.simulate_all(reference_string, frame_size)
                    simulator.print_results(results, reference_string)
                    
                    show_graph = input("\nShow graphs? (y/n): ")
                    if show_graph.lower() == 'y':
                        simulator.plot_comparison(results)
                    
                    input("\nPress Enter to continue...")
                    simulator.clear_screen()
                    
                except ValueError:
                    print("Invalid input! Please enter numbers only.")
                    input("Press Enter to continue...")
                    simulator.clear_screen()
            
            elif choice == '2':
                simulator.clear_screen()
                test_cases = [
                    {
                        "name": "Frequency Accumulation (Custom Algorithm Advantage)",
                        "description": "One very frequent page vs multiple recent pages - Custom retains frequent page",
                        "reference_string": [1, 1, 1, 1, 2, 3, 1],
                        "frame_size": 2
                    },
                    {
                        "name": "Sequential Access Pattern (FIFO Friendly)",
                        "description": "Linear page access - FIFO performs well here",
                        "reference_string": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "frame_size": 4
                    },
                    {
                        "name": "Temporal Locality Pattern (LRU Advantage)", 
                        "description": "Recent pages accessed again - LRU should dominate",
                        "reference_string": [1, 2, 3, 2, 1, 4, 5, 4, 1, 2, 3, 4, 5],
                        "frame_size": 3
                    },
                    {
                        "name": "Clock Algorithm Demonstration",
                        "description": "Classic textbook example showing Clock outperforming FIFO",
                        "reference_string": [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2],
                        "frame_size": 3
                    }
                ]
                
                print("Available Test Cases:")
                print("="*60)
                for i, test_case in enumerate(test_cases, 1):
                    print(f"{i}. {test_case['name']}")
                    print(f"   Description: {test_case['description']}")
                    print(f"   Reference String: {test_case['reference_string']}")
                    print(f"   Frame Size: {test_case['frame_size']}")
                    print()
                
                try:
                    test_num = int(input("Select test case (1-4): ")) - 1
                    if 0 <= test_num < len(test_cases):
                        selected_test = test_cases[test_num]
                        reference_string = selected_test['reference_string']
                        frame_size = selected_test['frame_size']
                        
                        print(f"\nRunning: {selected_test['name']}")
                        print(f"Expected: {selected_test['description']}")
                        print("="*60)
                        
                        results = simulator.animated_demonstration(reference_string, frame_size)
                        
                        input("\nPress Enter to show graphs...")
                        simulator.clear_screen()
                        
                        simulator.plot_comparison(results)
                    else:
                        print("Invalid test case!")
                    
                    input("\nPress Enter to continue...")
                    simulator.clear_screen()
                    
                except ValueError:
                    print("Invalid input!")
                    input("Press Enter to continue...")
                    simulator.clear_screen()
            
            elif choice == '3':
                try:
                    simulator.clear_screen()
                    ref_input = input("Enter reference string (space-separated): ")
                    reference_string = list(map(int, ref_input.split()))
                    frame_size = int(input("Enter frame size: "))
                    
                    print("\nSelect algorithm:")
                    print("1. FIFO")
                    print("2. LRU") 
                    print("3. Optimal")
                    print("4. Custom")
                    print("5. Clock")
                    
                    alg_choice = input("Choose algorithm (1-5): ")
                    algorithms = {'1': 'fifo', '2': 'lru', '3': 'optimal', '4': 'custom', '5': 'clock'}
                    
                    if alg_choice in algorithms:
                        simulator.clear_screen()
                        simulator.visual_demonstration(reference_string, frame_size, algorithms[alg_choice])
                    else:
                        print("Invalid choice!")
                    
                    input("\nPress Enter to continue...")
                    simulator.clear_screen()
                    
                except ValueError:
                    print("Invalid input!")
                    input("Press Enter to continue...")
                    simulator.clear_screen()
            
            elif choice == '4':
                try:
                    simulator.clear_screen()
                    ref_input = input("Enter reference string (space-separated): ")
                    reference_string = list(map(int, ref_input.split()))
                    frame_size = int(input("Enter frame size: "))
                    
                    simulator.animated_demonstration(reference_string, frame_size)
                    
                    input("\nPress Enter to continue...")
                    simulator.clear_screen()
                    
                except ValueError:
                    print("Invalid input!")
                    input("Press Enter to continue...")
                    simulator.clear_screen()
            
            elif choice == '5':
                simulator.clear_screen()
                print("Thank you!")
                break
            
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
                simulator.clear_screen()
    except KeyboardInterrupt:
        simulator.clear_screen()
        print("\nExiting simulation system. Goodbye!")
        return

if __name__ == "__main__":
    main()
