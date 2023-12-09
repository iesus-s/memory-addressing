import pandas as pd
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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

    num_page_tables = max(text_input[0])   # total amount of page tables to make and amount of total processes

    # print(num_page_tables)                  # test

    num_entries = 128

    # Create the page tables
    # Number of page tables with 128 entries each
    VPT_big = []    # 2D list of "x" page tables(rows) 128 columns deep
    for count1 in range(num_page_tables):
        VPT = []
        for count2 in range(num_entries):
            VPT.append({"Process": count1+1, "Virtual Address": 0, "Reference Bit": -1, "Dirty Bit": 0, "Memory": 0})
        VPT_big.append(VPT)

    # Test Variable
    check = 0
    full = 0
    page_faults = 0
    disk_references = 0
    write = 0
    dirty_write = 0
    process_num = 0     # process/task of the given address

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
        # convert to decimal
        int_vpn = int(virtual_page_number, 2)

        # Getting Offset from Process
        offset = bin(executing[1])[9:]
        # Getting W/R Command
        command = executing[2]
        if command == "W":
            write += 1

        # fill in the VPT given the process number and int_vpn
        VPT_big[process-1][int_vpn-1]["Process"] = process
        VPT_big[process-1][int_vpn-1]["Virtual Address"] = int_vpn
        VPT_big[process-1][int_vpn-1]["Reference Bit"] = -1
        VPT_big[process-1][int_vpn-1]["Dirty Bit"] = 0
        VPT_big[process-1][int_vpn-1]["Memory"] = 512   # not sure what's supposed to be here

        # FIFO and LRU algos will append/require more data inserted

        # Variable to check if process is complete
        done = 0
        # Variable to check if process is in Main Memory
        found = 0

        # Check if page is in main memory
        for main in main_memory:
            # Check if process is not complete
            if found == 0:
                # Check for Process and Virtual Page Number
                if main["Process"] == process and main["Virtual Address"] == int_vpn:
                    found = 1
                    check += 1

        # If page not in main memory (Page Fault)
        if found == 0:
            for main in main_memory:
                main["Reference Bit"] += 1
                # Check for Empty space in Main Memory
                if main["Memory"] == 0 and done == 0:
                    main["Virtual Address"] = int_vpn
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
            # FINDS OUR FIFO
            lifo = 0
            fifo = 0
            for loop in range(32):
                if lifo < main_memory[loop]["Reference Bit"]:
                    fifo = loop
                    lifo = main_memory[loop]["Reference Bit"]
            # print(main_memory[fifo]["Reference Bit"])
            # print(main_memory[fifo])
            # print(fifo)
            # exit()
            victim_page = main_memory[fifo]
            victim_page["Virtual Address"] = int_vpn
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
            main_memory[fifo] = victim_page
            check += 1
            done = 1
            found = 1
            page_faults += 1
            disk_references += 1
    print("---FIFO---")
    print("Page Faults: ", page_faults)
    print("Disk References: ", disk_references)
    print("Dirty Write: ", dirty_write)
