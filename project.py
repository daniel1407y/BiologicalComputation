def fully_activated_deactivated():
    return function[2] and not function[6]

def monotonic_repressors_check(index0, index1, index2):
    none_enough = not function[index0] and not function[index1] and not function[index2]
    some_enough = function[index0] and ((not function[index1] and not function[index2]) or function[index1])
    return none_enough or some_enough

def monotonic_activators_check(index0, index1, index2):
    none_enough = function[index0] and function[index1] and function[index2]
    some_enough = not function[index0] and ((function[index1] and function[index2]) or not function[index1])
    return none_enough or some_enough


vars_activators = ['NoneActivators', 'SomeActivators','AllActivators']
vars_repressors = ['NoneRepressors', 'SomeRepressors','AllRepressors']

# Generate all input pairs
inputs = [(x, y) for y in vars_repressors for x in vars_activators]
print(inputs)
num_functions = 2 ** len(inputs) # 2^(3*3)

filtered_functions = []
for i in range(num_functions):
    # convert the index to binary to create the output function
    function = [(i >> j) & 1 for j in range(len(inputs))]
    print(function)
    if not fully_activated_deactivated():
        continue
    if not monotonic_activators_check(0,1,2) or not monotonic_activators_check(3, 4, 5) or not monotonic_activators_check(6, 7, 8):
        continue
    if not monotonic_repressors_check(0,3,6) or not monotonic_repressors_check(1, 4, 7) or not monotonic_repressors_check(2, 5, 8):
        continue
            
    # Append the valid output function to the filtered list
    filtered_functions.append(function)


# Display the filtered results and write into a output.txt file
with open("output.txt", "w") as file:
    for idx, function in enumerate(filtered_functions):
        active_pairs = [(inputs[j][0], inputs[j][1]) for j in range(len(function)) if function[j] == 1]
        
        formatted_output = ' OR '.join([f"({pair[0]} AND {pair[1]})" for pair in active_pairs])
        print(f"Monotonic regulation condition of the reasoning engine number {idx}: {formatted_output}")
        print()
        
        file.write(f"Monotonic regulation condition of the reasoning engine number {idx}: {formatted_output}\n\n")
        
