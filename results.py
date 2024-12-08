

def main():
    # find the sample mean, sample dev, CI of time for a run across diff seeds
    # create average scatter plots for a run across diff seeds

    seeds = [10, 11, 12, 13, 14]
    probab = 0.3 #0.7 or 0.3
    g_type = 0.8 #low = 0.8, sun = 1, high = 1.04
    time_taken_for_critical_mass_across_seeds = []
    sum_sizes = 0
    average_object_size_across_seeds_li = []
    sample_var_across_runs_li = []

    max_num_entries = 0
    plots = []

    for seed in seeds:
        with open(f"output_for_{g_type},{probab},{seed}.txt") as file:
            lines = file.readlines()
            time_taken_for_critical_mass_across_seeds.append(lines[2])
            
            lines = lines[4:]
            num_entries = len(lines)
            max_num_entries = max(num_entries, max_num_entries)
            plots.append(lines)
            for line in lines:
                nums = line.split(" ")
                sum_sizes += int(nums[1]) #size

            average_object_size = sum_sizes/num_entries #for the run with a specfic seed
            variance_sum = 0
            for sample in lines:
                difference = int(sample[1]) - average_object_size
                variance_sum += difference**2

            sample_var = 1/(len(num_entries) - 1) * variance_sum #sample variance of object size per run
            sample_var_across_runs_li.append(sample_var)

            print(f"average object size for seed {seed} using p={probab} and gtype {g_type} = {average_object_size}, with sample variance {sample_var}")
            average_object_size_across_seeds_li.append(average_object_size)

            avg_time_taken_for_critical_mass_across_seeds = sum(time_taken_for_critical_mass_across_seeds)/5

    list_of_sizes = [0] * max_num_entries
    for plot in plots:
        for i in range(max_num_entries):
            if i < len(plot):
                list_of_sizes[i] += int(plot[i].split(" ")[1])
            else:
                list_of_sizes[i] += 1


    averaged_list_of_sizes = [round(x/5, 3) for x in list_of_sizes]
    average_object_size_across_seeds_value = sum(average_object_size_across_seeds_li)/5 #divide by 5 for 5 random seeds
    average_sample_var_across_runs_val = sum(sample_var_across_runs_li)/5



    #print results
    print(f"printing results for gtpye {g_type} and probab {probab}:")
    print("average object size across the 5 seeds is: ", average_object_size_across_seeds_value)
    print("average time taken to reach critical mass across the 5 seeds is: ", avg_time_taken_for_critical_mass_across_seeds)
    print(f"average sample variance across 5 runs is {average_sample_var_across_runs_val}")

    import matplotlib.pyplot as plt
    x = [i for i in range(len(list_of_sizes))]
    y = [i for i in list_of_sizes]
    plt.scatter(x, y)
    plt.xlabel("Object Number")
    plt.ylabel("Object Size")
            



if __name__ == "__main__":
    main()
