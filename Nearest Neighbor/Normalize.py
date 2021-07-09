def normalize(X):
    min_value = min(X)
    range = max(X) - min_value
    new_list = [(x-min_value)/range for x in X]
    return new_list

print(normalize((0.0, 5.0, 1.0, 500.0)))
