import pandas as pd
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Reading Text File
    text_file = sys.argv[1]
    text_input = pd.read_csv(text_file, sep=" ", header=None)
