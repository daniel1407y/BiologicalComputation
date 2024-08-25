import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np

EXPECTED_REGULATION_CONDITIONS = [
    (0, 0, 1, 0, 0, 0, 0, 0, 0),
    (0, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 1, 0, 0, 0),
    (0, 1, 1, 0, 0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 1, 1, 0, 0, 0),
    (0, 1, 1, 0, 1, 1, 0, 0, 1),
    (0, 1, 1, 0, 1, 1, 0, 1, 1),
    (1, 1, 1, 0, 0, 0, 0, 0, 0),
    (1, 1, 1, 0, 0, 1, 0, 0, 0),
    (1, 1, 1, 0, 1, 1, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 0, 0, 0),
    (1, 1, 1, 0, 0, 1, 0, 0, 1),
    (1, 1, 1, 0, 1, 1, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 0, 0, 1),
    (1, 1, 1, 0, 1, 1, 0, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1),
]
EXPECTED_NUM_REGULATION_CONDITIONS = len(EXPECTED_REGULATION_CONDITIONS)

def fully_activated_deactivated(function):
    return function[2] and not function[6]

def monotonic_activators(function, index0, index1, index2):
    none_enough = function[index0] and function[index1] and function[index2]
    some_enough = not function[index0] and ((function[index1] and function[index2]) or not function[index1])
    return none_enough or some_enough

def monotonic_repressors(function, index0, index1, index2):
    none_enough = not function[index0] and not function[index1] and not function[index2]
    some_enough = function[index0] and ((not function[index1] and not function[index2]) or function[index1])
    return none_enough or some_enough

def plot_functions(df: pd.DataFrame):
    plt.figure(figsize=(12, 8))
    
    cmap = mcolors.ListedColormap(["white", "darkred"])
    plt.imshow(df, cmap=cmap, aspect="auto")
    
    plt.ylabel("Regulation Condition")
    plt.title("Monotonic Regulation Conditions")

    plt.xticks(ticks=range(len(df.columns)), labels=df.columns, fontsize=10, rotation=45, ha="right")
    plt.yticks(ticks=range(len(df.index)), labels=range(1, len(df.index) + 1))

    for y in range(df.shape[0] + 1):
        plt.axhline(y - 0.5, color="black", linewidth=2)
    for x in range(df.shape[1] + 1):
        plt.axvline(x - 0.5, color="black", linewidth=2)
        
    plt.tight_layout()
    plt.show() 
 
 
def initialize_network():
    vars_activators = ['NoneActivators', 'SomeActivators','AllActivators']
    vars_repressors = ['NoneRepressors', 'SomeRepressors','AllRepressors']

    # Generate all input pairs
    inputs = [(x, y) for y in vars_repressors for x in vars_activators]
    num_functions = 2 ** len(inputs) # 2^(3*3)
    return inputs, num_functions

def filter(inputs, num_functions):
    filtered_functions = []
    for i in range(num_functions):
        # convert the index to binary to create the output function
        function = [(i >> j) & 1 for j in range(len(inputs))]
        if not fully_activated_deactivated(function):
            continue
        if not monotonic_activators(function, 0,1,2) or not monotonic_activators(function, 3, 4, 5) or not monotonic_activators(function, 6, 7, 8):
            continue
        if not monotonic_repressors(function, 0,3,6) or not monotonic_repressors(function, 1, 4, 7) or not monotonic_repressors(function, 2, 5, 8):
            continue
                
        # Append the valid output function to the filtered list
        filtered_functions.append(function)
    return filtered_functions


def main():
    inputs, num_functions = initialize_network()
    filtered_functions = filter(inputs, num_functions)


    data = np.array(filtered_functions)
    df = pd.DataFrame(data, columns=inputs)
    plot_functions(df)

if __name__ == "__main__":
    main()