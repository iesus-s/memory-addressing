import pandas as pd
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create Disk Memory

    # Create Main Memory
    main_memory = []
    # Create Addressing Variables
    virtual_page_number = 0
    offset = 0
    # Reading Text File
    text_file = sys.argv[1]
    text_input = pd.read_csv(text_file, sep="\t", header=None)

    # Unpack All Processes
    for counter in range(len(text_input)):
        # Getting Process
        executing = text_input.iloc[counter]
        # Getting VPN from Process
        vpn = bin(executing[1])[:9]
        # Remove initial '0b'
        virtual_page_number = vpn[2:]
        # Getting Offset from Process
        offset = bin(executing[1])[9:]

        for main in main_memory:
            if main == virtual_page_number:
                print("1")
                exit()

    print("Binary Value: ", bin(executing[1]))
    print("Virtual Page Number: ", virtual_page_number)
    print("Offset: ", offset)
    print("Int VPN: ", int(virtual_page_number, 2))
    print("Int Offset: ", int(offset, 2))
    exit()

    # print(executing)
    # print(bin(executing[1]))
    # print("Virtual Page Number: ", virtual_page_number)
    # print("Offset: ", offset)
