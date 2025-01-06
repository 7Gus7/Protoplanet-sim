import numpy as np
from scipy.stats import t

def calculate_confidence_interval(data, alpha=0.05):
    """Calculates the 95% confidence interval for the given data."""
    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # Sample standard deviation (ddof=1)
    t_critical = t.ppf(1 - alpha / 2, df=n - 1)  # t-value for 95% CI
    margin_of_error = t_critical * (std_dev / np.sqrt(n))
    return mean, (mean - margin_of_error, mean + margin_of_error)

def main():
    # find the sample mean, sample dev, CI of time for a run across diff seeds
    # create average scatter plots for a run across diff seeds

    seeds = [10, 11, 12, 13, 14]
    probab = 0.3 #0.7 or 0.3
    g_type = 1.04 #low = 0.8, sun = 1, high = 1.04
    time_taken_for_critical_mass_across_seeds = []
    sum_sizes = 0
    average_object_size_across_seeds_li = []
    sample_var_across_runs_li = []

    max_num_entries = 0
    plots = []
    
    print(f"printing stats for gtpye {g_type} and probab {probab}:")

    for seed in seeds:
        print("SEED IS ", seed)
        
        with open(f"output_for_{g_type},{probab},{seed}.txt") as file:
            lines = file.readlines()
            time_taken_for_critical_mass = float(lines[2].split(":")[1].strip())
            time_taken_for_critical_mass_across_seeds.append(time_taken_for_critical_mass)
            print("time taken for critical mass for seed ", seed, " is ", time_taken_for_critical_mass)
            
            lines = lines[4:]
            num_entries = len(lines)
            max_num_entries = max(num_entries, max_num_entries)
            plots.append(lines)
            
            # Calculate average object size for the run
            sum_sizes = 0
            object_sizes = []
            for line in lines:
                nums = line.split(" ")
                curr_size = int(nums[1])  # size
                object_sizes.append(curr_size)
                sum_sizes += curr_size
                
            average_object_size = sum_sizes / num_entries #avg object size for the current run 
            variance_sum = sum((size - average_object_size) ** 2 for size in object_sizes)
            sample_var = variance_sum / (num_entries - 1)  # Sample variance
            sample_var_across_runs_li.append(sample_var)
            average_object_size_across_seeds_li.append(average_object_size)  
            print(f"average object size for seed {seed} using p={probab} and gtype {g_type} = {average_object_size}, with sample variance {sample_var}")         
        
     
            
    # Calculate CI for time taken for critical mass
    time_mean, time_ci = calculate_confidence_interval(time_taken_for_critical_mass_across_seeds)
    print(f"\nTime taken for critical mass across seeds: Mean = {time_mean}, 95% CI = {time_ci}")

    # Calculate CI for average object size
    size_mean, size_ci = calculate_confidence_interval(average_object_size_across_seeds_li)
    print(f"Average object size across seeds: Mean = {size_mean}, 95% CI = {size_ci}")


    list_of_sizes = [0] * max_num_entries
    for plot in plots:
        for i in range(max_num_entries):
            if i < len(plot):
                list_of_sizes[i] += int(plot[i].split(" ")[1])
            else:
                list_of_sizes[i] += 1

    averaged_list_of_sizes = [round(x/5, 3) for x in list_of_sizes]

    average_sample_var_across_runs_val = sum(sample_var_across_runs_li)/5
    print(f"average sample variance across 5 runs is {average_sample_var_across_runs_val}")




    import matplotlib.pyplot as plt
    x = [i for i in range(len(list_of_sizes))]
    y = [i for i in averaged_list_of_sizes]
    plt.scatter(x, y)
    plt.xlabel("Object Number")
    plt.ylabel("Object Size")
    plt.show()
            


if __name__ == "__main__":
    main()
