import pandas as pd
from random import randint
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create Disk Memory
    disk_memory = []
    for count in range(65535):
        disk_memory.append({"Process": 0, "Virtual Address": 0, "Reference Bit": 0, "Dirty Bit": 0,
                            "Memory": 0})
    # Create Main Memory
    main_memory = []
    for count in range(32):
        main_memory.append({"Process": 0, "Virtual Address": 0, "Reference Bit": 0, "Dirty Bit": 0,
                            "Memory": 0})

    # Create Addressing Variables
    virtual_page_number = 0
    offset = 0
    # Variable for working Page and Process
    executing = []
    # Reading Text File
    text_file = sys.argv[1]
    text_input = pd.read_csv(text_file, sep="\t", header=None)

    # Test Variable
    check = 0
    full = 0
    page_faults = 0
    disk_references = 0
    write = 0
    dirty_write = 0

    # Unpack All Processes
    for counter in range(len(text_input)):
        # Getting Process Command
        executing = text_input.iloc[counter]
        # Getting Process
        process = executing[0]
        # Getting Virtual Address
        virtual_address = bin(executing[1])
        virtual_address = virtual_address[2:]
        # Getting VPN from Process
        vpn = bin(executing[1])[:9]
        # Remove initial '0b'
        virtual_page_number = vpn[2:]
        # Getting Offset from Process
        offset = bin(executing[1])[9:]
        # Getting W/R Command
        command = executing[2]
        if command == "W":
            write += 1

        # Variable to check if process is complete
        done = 0
        # Variable to check if process is in Main Memory
        found = 0

        # Check if page is in main memory
        for main in main_memory:
            # Check if process is not complete
            if found == 0:
                # Check for Process and Virtual Page Number
                if main["Process"] == process and main["Virtual Address"] == int(virtual_address):
                    found = 1
                    check += 1

        # If page not in main memory (Page Fault)
        if found == 0:
            for main in main_memory:
                # Check for Empty space in Main Memory
                if main["Memory"] == 0 and done == 0:
                    main["Virtual Address"] = int(virtual_address)
                    main["Process"] = process
                    main["Memory"] = 512
                    if command == "W":
                        main["Dirty Bit"] = 1
                    check += 1
                    done = 1
                    full += 1
                    found = 1
                    disk_references += 1
                    page_faults += 1

        # RANDOM REPLACEMENT ALGORITHM
        # If Main Memory is full and Page Fault
        if full == 32 and found == 0:
            rand = randint(0, 31)
            victim_page = main_memory[rand]
            victim_page["Virtual Address"] = int(virtual_address)
            victim_page["Process"] = process
            victim_page["Memory"] = 512
            # Check if Dirty Bit on Victim Page
            if victim_page["Dirty Bit"] == 1:
                disk_references += 1
            # Check if New Process Writes
            if command == "W":
                victim_page["Dirty Bit"] = 1
                dirty_write += 1
            else:
                victim_page["Dirty Bit"] = 0
            main_memory[rand] = victim_page
            check += 1
            done = 1
            found = 1
            page_faults += 1
            disk_references += 1

    print("Page Faults: ", page_faults)
    print("Disk References: ", disk_references)
    print("Dirty Write: ", dirty_write)

    # print(executing)
    # print(bin(executing[1]))
    # print("Virtual Page Number: ", virtual_page_number)
    # print("Offset: ", offset)
