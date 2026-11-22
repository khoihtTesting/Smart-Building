import time

# Calibration constants
DESIRED_MOISTURE = 600  # Target soil moisture threshold

def run_pump(seconds):
    print(f"-> Turning on the water pump for {seconds:.1f} seconds...")
    time.sleep(1)  # Simulate execution time
    print("-> Water pump turned off.")

def calibrate_and_test():
    print("=== STARTING SOIL MOISTURE SENSOR CALIBRATION ===")
    
    # Initial dry soil moisture reading
    initial_moisture = 643
    print(f"Initial Dry Soil Moisture: {initial_moisture}\n")
    
    # Print table header
    print(f"{'Total Pump time':<18} | {'Soil Moisture':<15} | {'Decrease':<10}")
    print("-" * 47)
    print(f"{'Dry':<18} | {initial_moisture:<15} | {0:<10}")
    
    current_moisture = initial_moisture
    decreases = []
    
    # Simulate pump running from 1s to 6s
    for total_sec in range(1, 7):
        # Sample decrease values matching standard lab example
        decrease_amount = 21 if total_sec % 2 != 0 else 20
        if total_sec == 2:
            decrease_amount = 22
        elif total_sec == 5:
            decrease_amount = 22
            
        current_moisture -= decrease_amount
        decreases.append(decrease_amount)
        
        print(f"{f'{total_sec}s':<18} | {current_moisture:<15} | {decrease_amount:<10}")
    
    # Calculate average decrease per second
    avg_decrease = sum(decreases) / len(decreases)
    print("-" * 47)
    print(f"=> Average decrease in soil moisture per second of water: {avg_decrease:.1f}\n")
    
    return avg_decrease

def smart_irrigation_logic(avg_decrease, current_moisture):
    print("=== SMART IRRIGATION CONTROL ===")
    print(f"Current soil moisture: {current_moisture}")
    
    if current_moisture > DESIRED_MOISTURE:
        deficit = current_moisture - DESIRED_MOISTURE
        required_pump_time = deficit / avg_decrease
        
        print(f"Need to adjust by {deficit} moisture units.")
        print(f"Optimal pump run time: {required_pump_time:.2f} seconds.")
        
        run_pump(required_pump_time)
    else:
        print("Soil moisture is at an optimal level, no irrigation needed.")

if __name__ == "__main__":
    # 1. Run calibration table phase
    avg_decrease_rate = calibrate_and_test()
    
    # 2. Run smart control phase with a sample reading
    test_moisture_reading = 643 
    smart_irrigation_logic(avg_decrease_rate, test_moisture_reading)