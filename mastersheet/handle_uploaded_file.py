def get_file(input):
    file = open(input)
    return file.readlines()

def get_heading(input):
    return input[0].split(',')

def get_values(input):
    return input[-1].split(',')

file = get_file('C_Y_07_Baseline_DF.csv')
headings = get_heading(file)
values = get_values(file)
