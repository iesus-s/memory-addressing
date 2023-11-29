import pandas as pd
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Reading Text File
    text_file = sys.argv[1]
    text_input = pd.read_csv(text_file, sep="\t", header=None)

    # Unpack First Process
    executing = text_input.iloc[1]
    virtual_page_number = bin(executing[1])[:7]
    offset = bin(executing[1])[9:]
    print(executing)
    print(bin(executing[1]))
    print("Virtual Page Number: ", virtual_page_number)
    print("Offset: ", offset)
