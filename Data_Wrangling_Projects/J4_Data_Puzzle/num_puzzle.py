import itertools
values = [1.67, 1.64, 1.37, 1.43, 1.41, 0.96, 1.05, 1.53, 1.59, 1.85, 1.85, 1.89, 1.49, 1.56, 1.72, 1.51, 1.48, 1.45, 1.51, 1.72, 1.69, 1.54, 1.51, 1.53, 1.66, 1.51, 1.53, 1.16]
keys = ['1360-2', '1360-3', '1364-1', '1364-2', '1364-3', '1370-GE', '1370-GW', '4603-1', '4603-2', '4605-1', '4607-1', '4607-3', '4609-1E', '4609-2E', '4611-2N', '4611-2W', '4611-3W', '4613-1E', '4613-2E', '4613-2S', '4613-3S', '4615-1E', '4615-2W', '4615-3E', '4617-1W', '4617-2E', '4617-3E', '4617-GW']
mapping = dict()
for i in range(len(keys)):
    mapping[keys[i]] = values[i]
print("Initial Mapping:")
print("Length:")
print(len(mapping))
print(mapping)
output_1 = list()
for L in range(6, 12):
    for subset in itertools.combinations(values, L):
        if sum(subset) == 10.43:
            output_1.append(subset)
print("Considering all 28 identifiers and weights:")
print("Number of combinations whose sum = 10.43:")
print(len(output_1))
mapping_2 = mapping.copy()
mapping_2.pop('4617-GW', None)
mapping_2.pop('4615-2W', None)
print("Mapping without 4617-GW and 4615-2W:")
print("Length:")
print(len(mapping_2))
print(mapping_2)
keys = mapping_2.keys()
values = list(mapping_2[key] for key in keys)
output_2 = list()
for L in range(6, 12):
    for subset in itertools.combinations(values, L):
        if sum(subset) == 10.43:
            output_2.append(subset)
print("Considering all identifiers and weights excluding ( 4617-GW and 4615-2W ):")
print("Number of combinations whose sum = 10.43:")
print(len(output_2))
sum_must_haves = 0
mapping_3 = mapping_2.copy()
sum_must_haves += mapping_3.pop('4611-3W', None)
sum_must_haves += mapping_3.pop('4613-2S', None)
print("Sum of the weights of 4611-3W and 4613-2S:")
print(sum_must_haves)
print("Mapping without 4617-GW, 4615-2W, 4611-3W and 4613-2S:")
print("Length:")
print(len(mapping_3))
print(mapping_3)
keys = mapping_3.keys()
values = list(mapping_3[key] for key in keys)
output_3 = list()
for L in range(4, 10):
    for subset in itertools.combinations(values, L):
        if (sum(subset) + sum_must_haves) == 10.43:
            output_3.append(subset)
print("Considering all identifiers and weights including ( 4611-3W and 4613-2S ) and excluding ( 4617-GW and 4615-2W ):")
print("Number of combinations whose sum = 10.43:")
print(len(output_3))
