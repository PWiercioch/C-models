def get_file(input):
    file = input.read().decode('utf-8')
    return file.splitlines()

def get_heading(input):
    return input[0].split(',')

def get_values(input):
    return input[-1].split(',')

def main(filename):
    file = get_file(filename)
    headings = get_heading(file)

    return get_values(file)
