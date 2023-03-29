import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

################################################################################
# Problem 1
################################################################################

def deidentify(df):
    # models a faulty data release with just Name/SSN dropeed
    return df.drop(columns=['Name', 'SSN'])

def pii(df):
    # models what an attacker may have obtained
    return df[['Name','DOB','SSN','Zip']]

def link_attack(deidenfied_df, pii_df):
    # merge
    df1 = pd.merge(pii_df, deidenfied_df, how='inner', on=["DOB", "Zip"])
    
    # drop duplicates
    df1 = df1.drop_duplicates(subset=['DOB', 'Zip'], keep = False)
    
    return df1

################################################################################
# Problem 1.2
################################################################################

def is_k_anon(df, cols, k):
    """
    Inputs: dataframe df, a list of column names cols, 
    integer k assumed to be at least 1
    """
    
    val_count = df.value_counts(cols)
    print(val_count)
    return min(val_count) >= k

################################################################################
# Problem 1.3
################################################################################

def num_bachelors(df):
    return (df.Education == 'Bachelors').sum()

def laplace_mech(query, sensitivity, epsilon):
    return query + np.random.laplace(0.0, scale = sensitivity/epsilon)

def make_plot_3():
    query = 200.0
    sensitivity = 1
    runs = 10000
    
    plot_data = []
    
    for epsilon in [.5, 1, 10]:
        res = []
        for i in range(runs):
            output = laplace_mech(query, sensitivity, epsilon)
            res.append(output)
            
        plt.hist(res, bins = 50, label = f"Epsilon Value: {epsilon}")
    
    plt.legend(loc = 'upper right')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()    

################################################################################
# Problem 1.4
################################################################################

def make_plot_4():
    sensitivity = 1
    epsilon = .05
    runs = 10000

    for query in [200.0, 201.0]:
        res = []
        for i in range(runs):
            output = laplace_mech(query, sensitivity, epsilon)
            res.append(output)

        plt.hist(res, bins = 50, label = f"Query: {query}", alpha = 0.75)
        
    plt.legend(loc = 'upper right')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.xlim(100, 300)
    plt.show()
    

################################################################################
# Problem 1.5
################################################################################

def make_plot_5():
    
    query = num_bachelors(pd.read_csv('./adult_with_pii.csv'))
    sensitivity = 1 ####### 

    runs = 10000

    for epsilon in [.5, 1, 10]:
        res = []
        for i in range(runs):
            output = abs(laplace_mech(query, sensitivity, epsilon)- query)
            res.append(output)

        plt.hist(res, bins = 20, \
                 label = f"Epsilon Value: {epsilon}")
    
    plt.legend(loc = 'upper right')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()
    
    
# driver/test code below here
if __name__ == "__main__":
    # tested them in notebook
    exit()
