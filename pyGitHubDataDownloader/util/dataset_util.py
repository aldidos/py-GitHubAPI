
def split_dataset(dataset : list, order, n_sub) : 
    n_dataset = len(dataset)
    split_size = int( n_dataset / n_sub ) 
    start_idx = split_size * order
    end_idx = start_idx + split_size

    if end_idx >= n_dataset : 
        end_idx = n_dataset
    
    return dataset[start_idx : end_idx]