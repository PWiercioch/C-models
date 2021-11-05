def get_file(input):
    file = open(input)
    return file.readlines()

def get_heading(input):
    return input[0].split(',')

def get_values(input):
    return input[-1].split(',')

def main():
    file = get_file('C_Y_07_Baseline_DF.csv')
    headings = get_heading(file)

    return get_values(file)
