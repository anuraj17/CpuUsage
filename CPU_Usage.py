#Name - Aniruddha Rajguru,
#Institute - California State University, Sacramento
#Copyright, All rights reserved
#Version 0.9.1

from beautifultable import BeautifulTable
import sys, re, time, os, os.path, math, numbers

#Module for counting the number of CPU cores
cpu_Counter = 0
def cpu_Count():
    global cpu_Counter
    cpu_Counter = 0
    stat_List = open("/proc/stat", "r")
    regexp_Cpu = re.compile("cpu*.")
    new_Stat_List = filter(regexp_Cpu.match, stat_List)
    cpu_List = [line.split() for line in new_Stat_List]
    for word in cpu_List:
        cpu_Counter = cpu_Counter + 1
    print "You have a ",cpu_Counter-1," core CPU."
#End of cpu_Count()

#Module for print CPU Count
def cpu_Print():
    print "You have a",cpu_Counter-1," core CPU."
#End of CPU_Print

#Testing Module, not required in current version (0.9.1) of the program
count_diskNum = 0
disk_Name = []
def diskNum_Util():
    global  count_diskNum

    disk_Num_List = os.listdir("/sys/block/")   #The advantage of using sys is less overhead
    diskinfo_Num_List = [line.split() for line in disk_Num_List]

    regexp_diskNum = re.compile("sd.")
    new_diskNum_List = filter(regexp_diskNum.match, disk_Num_List)
    new_diskNum_List = [line.split() for line in new_diskNum_List]

    for word in new_diskNum_List:
        count_diskNum = count_diskNum + 1

    for word in new_diskNum_List:
        disk_Name.append(word)

    for word in disk_Name:
        value = str(word[0])
diskNum_Util()

#Testing Module, not required in current version (0.9.1) of the program
prev_disk_Read = []
prev_disk_Write = []
prev_block_Read = []
prev_block_Write = []

for i in range(0, count_diskNum):
    prev_disk_Read.insert(i, '0')
    prev_disk_Write.insert(i, '0')
    prev_block_Read.insert(i, '0')
    prev_block_Write.insert(i, '0')
net_BANDWIDTH = 1024
def disk_Util():
    global prev_block_Write, prev_block_Read, prev_disk_Write, prev_disk_Read
    disk_count = 0
    disk_Table = BeautifulTable()
    disk_Table.column_headers = ["Disk Name", "Disk Read", "Disk Write", "Block Read", "Block Write"]

    print "You have ",count_diskNum," Hard Drive(s) on your machine"

    for word in disk_Name:
        value = str(word[0])
        diskPath = ''.join(['/sys/block/',value,'/stat'])   #The advantage of using sys is less overhead
        diskinfo = open(diskPath, 'r')
        diskinfo_List = [line.split() for line in diskinfo]

        cur_disk_Read = int(diskinfo_List[0][0])
        cur_disk_Write = int(diskinfo_List[0][4])
        cur_block_Read = int(diskinfo_List[0][2])
        cur_block_Write = int(diskinfo_List[0][6])

        delta_disk_Read = float(cur_disk_Read + int(prev_disk_Read[disk_count]))/2
        delta_disk_Write = float(cur_disk_Write + int(prev_disk_Write[disk_count]))/2
        delta_block_Read = float(cur_block_Read + int(prev_block_Read[disk_count]) * 512)/2
        delta_block_Write = float(cur_block_Write + int(prev_block_Write[disk_count]) * 512)/2

        prev_disk_Read[disk_count] = cur_disk_Read
        prev_disk_Write[disk_count] = cur_disk_Write
        prev_block_Read[disk_count] = cur_block_Read
        prev_block_Write[disk_count] = cur_block_Write
        disk_count = disk_count + 1
        disk_Table.append_row([word, str(delta_disk_Read)+'bytes', str(delta_disk_Write)+'bytes', str(delta_block_Read)+'bytes', str(delta_block_Write)+'bytes'])
    print "Total Disk Utilization:"
    print disk_Table

#Module for ProcessName
process_Name = '1'
def processName():
    global process_Name
    processID_Total = 0
    temp_List = ['0','0','0', '0','0','0']
    column_Counter = 0      #Just to maintain the table column counter
    processIDs_Table = BeautifulTable()

    print "Following are the processes that are running on your machine"
    process_names_Total = os.listdir('/proc')   #This has other folders along with PID
    process_names_Total2 = [line.split() for line in process_names_Total]   #Split into a List

    for word in process_names_Total2:
        s = ''.join(x for x in word[0] if x.isdigit())  #Filter out the processes that don't have a PID
        if s:
            temp_List[column_Counter] = s
            column_Counter = column_Counter + 1
            if column_Counter == 6:
                processIDs_Table.append_row([temp_List[0], temp_List[1], temp_List[2], temp_List[3], temp_List[4], temp_List[5]])
                column_Counter = 0
                processID_Total = processID_Total + 1
            else:
                continue
    print processIDs_Table
    try:
        print "Enter the Process-ID:"
        process_Name = raw_input()
        for row in range(0, processID_Total):
            for column in range(0, 5):
                if (str(process_Name) == str(processIDs_Table[row][column])):
                    main()
                else:
                    continue
        print "You entered incorrect value, Please try again"
        process_Name = '1'
        processName()
    except KeyboardInterrupt:
        main_Menu()
#End of ProcessName()

#Module for CPU_Resource_Overall
prev_worktime_Overall = 0
prev_idletime_Overall = 0

prev_worktime_User = 0
prev_idletime_User = 0

prev_worktime_Kernel = 0
prev_idletime_Kernel = 0
cpu_Table = BeautifulTable()
#-----------------------------
prev_worktime_perProcess_Overall = 0
prev_worktime_perProcess_User = 0
prev_worktime_perProcess_Kernel = 0
#--------------------------------
prev_proc_PhysicalMem = 0
prev_proc_VirtualMem = 0
prev_worktime_User_Individual = []
prev_idletime_User_Individual = []

prev_worktime_Kernel_Individual = []
prev_idletime_Kernel_Individual = []

prev_worktime_Overall_Individual = []
prev_idletime_Overall_Individual = []

def set_variable():
    global cpu_Counter, prev_worktime_User_Individual, prev_idletime_User_Individual, prev_worktime_Kernel_Individual, prev_idletime_Kernel_Individual, prev_worktime_Overall_Individual, prev_idletime_Overall_Individual
    for j in range(0, cpu_Counter):
        prev_worktime_User_Individual.insert(j,'0')
        prev_idletime_User_Individual.insert(j,'0')

        prev_worktime_Kernel_Individual.insert(j,'0')
        prev_idletime_Kernel_Individual.insert(j,'0')

        prev_worktime_Overall_Individual.insert(j,'0')
        prev_idletime_Overall_Individual.insert(j,'0')
#End of set_variable

def cpu_Util():
    cpu_Table = BeautifulTable()
    cpu_perProcess_Table = BeautifulTable()
    cpu_Individual_Table = BeautifulTable()

    global prev_worktime_Overall, prev_idletime_Overall, prev_worktime_User, prev_idletime_User, prev_worktime_Kernel, prev_idletime_Kernel;

    stat_List = open("/proc/stat", "r")
    regexp_Cpu = re.compile("cpu*.")
    new_Stat_List = filter(regexp_Cpu.match, stat_List)
    cpu_List = [line.split() for line in new_Stat_List]
    cpu_Table.column_headers = ["Overall", "Kernel Mode", "User Mode"]

    #Overall
    cur_worktime_Overall = int(cpu_List[0][1]) + int(cpu_List[0][2]) + int(cpu_List[0][3])
    cur_idletime_Overall = int(cpu_List[0][4])

    delta_worktime_Overall = (cur_worktime_Overall - prev_worktime_Overall)
    delta_idletime_Overall = (cur_idletime_Overall - prev_idletime_Overall)

    cur_rate_Overall = float(delta_worktime_Overall)/(delta_worktime_Overall + delta_idletime_Overall)
    cur_rate_percentage_Overall = cur_rate_Overall * 100

    prev_worktime_Overall = cur_worktime_Overall
    prev_idletime_Overall = cur_idletime_Overall

    #User Mode
    cur_worktime_User = int(cpu_List[0][1])
    cur_idletime_User = int(cpu_List[0][4])

    delta_worktime_User = (cur_worktime_User - prev_worktime_User)
    delta_idletime_User = (cur_idletime_User - prev_idletime_User)

    cur_rate_User = float(delta_worktime_User)/(delta_worktime_User + delta_idletime_User)
    cur_rate_percentage_User = cur_rate_User * 100

    prev_worktime_User = cur_worktime_User
    prev_idletime_User = cur_idletime_User

    #Kernel Mode
    cur_worktime_Kernel= int(cpu_List[0][3])
    cur_idletime_Kernel = int(cpu_List[0][4])

    delta_worktime_Kernel = (cur_worktime_Kernel - prev_worktime_Kernel)
    delta_idletime_Kernel = (cur_idletime_Kernel - prev_idletime_Kernel)

    cur_rate_Kernel = float(delta_worktime_Kernel)/(delta_worktime_Kernel + delta_idletime_Kernel)
    cur_rate_percentage_Kernel = cur_rate_Kernel * 100

    prev_worktime_Kernel = cur_worktime_Kernel
    prev_idletime_Kernel = cur_idletime_Kernel

    cpu_Table.append_row([(str(cur_rate_percentage_Overall)[0:4])+'%', (str(cur_rate_percentage_Kernel)[0:4])+'%', (str(cur_rate_percentage_User)[0:4])+'%'])
    print "Total Utilization by the CPU:"
    print cpu_Table

    #PerProcess Utilization
    global prev_worktime_perProcess_User, prev_worktime_perProcess_Kernel, prev_worktime_perProcess_Overall

    per_processPath = ''.join(['/proc/',process_Name,'/stat'])
    per_process_List = open(per_processPath, 'r')
    per_processinfo_List = [line.split() for line in per_process_List]

    cpu_perProcess_Table.column_headers = ["Process-ID","Overall", "UserMode","KernelMode", "PhysicalMemory", "VirtualMemory"]

    try:
        cur_worktime_perProcess_User = int(per_processinfo_List[0][13] + per_processinfo_List[0][15]) #if you want the User child process jiffies as well, just add feild per_processinfo_List[0][15] as well
        delta_worktime_perProcess_User = float(cur_worktime_perProcess_User - prev_worktime_perProcess_User)
        worktime_perProcess_percentage_User = float(delta_worktime_perProcess_User/delta_worktime_User)

        cur_worktime_perProcess_Kernel = int(per_processinfo_List[0][14] + per_processinfo_List[0][15])  #if you want the Kernel child process jiffies as well, just add feild per_processinfo_List[0][15] as well
        delta_worktime_perProcess_Kernel = float(cur_worktime_perProcess_Kernel - prev_worktime_perProcess_Kernel)
        worktime_perProcess_percentage_Kernel = float(delta_worktime_perProcess_Kernel/delta_worktime_Kernel)

        cur_worktime_perProcess_Overall = int (cur_worktime_perProcess_User + cur_worktime_perProcess_Kernel)
        delta_worktime_perProcess_Overall = float(cur_worktime_perProcess_Overall - prev_worktime_perProcess_Overall)
        worktime_perProcess_percentage_Overall = float(delta_worktime_perProcess_Overall/delta_worktime_Overall)

        prev_worktime_perProcess_User = cur_worktime_perProcess_User
        prev_worktime_perProcess_Kernel = cur_worktime_perProcess_Kernel
        prev_worktime_perProcess_Overall = cur_worktime_perProcess_Overall

    except ZeroDivisionError as error:
        worktime_perProcess_percentage_Overall = 0.0
        worktime_perProcess_percentage_User = 0.0
        worktime_perProcess_percentage_Kernel = 0.0

    #Physical_Memory used by every process
    global prev_proc_PhysicalMem

    per_process_PhysicalMem_Path = ''.join(['/proc/',process_Name,'/statm'])
    per_process_PhysicalMem_List = open(per_process_PhysicalMem_Path, 'r')
    per_processinfo_PhysicalMem_List = [line.split() for line in per_process_PhysicalMem_List]

    Mem_List = open('/proc/meminfo', 'r')
    new_Mem_List = [line.split() for line in Mem_List]
    cur_mem_Total = int(new_Mem_List[0][1])
    proc_VirtualMem_Overall = int(new_Mem_List[31][1])

    cur_proc_PhysicalMem = int(per_processinfo_PhysicalMem_List[0][1])
    delta_proc_PhysicalMem = float(cur_proc_PhysicalMem + prev_proc_PhysicalMem)
    cur_percentage_PhysicalMem = float(delta_proc_PhysicalMem/cur_mem_Total)

    prev_proc_PhysicalMem = cur_proc_PhysicalMem

    #Virtual_Memory used by every process
    global prev_proc_VirtualMem

    per_process_VirtualMem_Path = ''.join(['/proc/',process_Name,'/status'])
    per_process_VirtualMem_List = open(per_process_VirtualMem_Path, 'r')
    per_processinfo_VirtualMem_List = [line.split() for line in per_process_VirtualMem_List]

    cur_proc_VirtualMem = int(per_processinfo_VirtualMem_List[21][1])

    bits_OS = open("/lib/systemd/systemd","r")  #You can also Use Cpu_Info for the same value
    regexp_BitsOS = re.compile("lib-x86-32*.")  #Check if the OS is 32-bits or 64-bits
    result_BitsOS = filter(regexp_BitsOS.match, bits_OS)
    if result_BitsOS:
        delta_proc_VirtualMem = float(cur_proc_VirtualMem + prev_proc_VirtualMem)/4294967296
    else:
        delta_proc_VirtualMem = float(cur_proc_VirtualMem + prev_proc_VirtualMem)/ (4294967296 * 2)
    cur_percentage_VirtualMem = float(delta_proc_VirtualMem/proc_VirtualMem_Overall) * 100

    prev_proc_VirtualMem = cur_proc_VirtualMem

    cpu_perProcess_Table.append_row([process_Name, (str(worktime_perProcess_percentage_Overall)[0:4])+'%', (str(worktime_perProcess_percentage_User)[0:4]+'%'), (str(worktime_perProcess_percentage_Kernel)[0:4])+'%', (str(cur_percentage_PhysicalMem)[0:4])+'%', (str(cur_percentage_VirtualMem)[0:4])+'%'])

    #PerCPU Utili
    global prev_worktime_Overall_Individual, prev_idletime_Overall_Individual
    cpu_Individual_Table.column_headers = ['CPU_Number','Overall','KernelMode','UserMode']

    for perCPU in range(1, cpu_Counter):
        #Overall
        cur_worktime_Overall_Individual = int(cpu_List[perCPU][1]) + int(cpu_List[perCPU][2]) + int(cpu_List[perCPU][3])
        cur_idletime_Overall_Individual = int(cpu_List[perCPU][4])

        delta_worktime_Overall_Individual = (int(cur_worktime_Overall_Individual) - int(prev_worktime_Overall_Individual[perCPU]))
        delta_idletime_Overall_Individual = (int(cur_idletime_Overall_Individual) - int(prev_idletime_Overall_Individual[perCPU]))

        cur_rate_Overall_Individual = float(delta_worktime_Overall_Individual)/(delta_worktime_Overall_Individual + delta_idletime_Overall_Individual)
        cur_rate_percentage_Overall_Individual = cur_rate_Overall_Individual * 100

        prev_worktime_Overall_Individual[perCPU] = cur_worktime_Overall_Individual
        prev_idletime_Overall_Individual[perCPU] = cur_idletime_Overall_Individual

        #KernelMode
        cur_worktime_Kernel_Individual = int(cpu_List[perCPU][3])
        cur_idletime_Kernel_Individual = int(cpu_List[perCPU][4])

        delta_worktime_Kernel_Individual = (int(cur_worktime_Kernel_Individual) - int(prev_worktime_Kernel_Individual[perCPU]))
        delta_idletime_Kernel_Individual = (int(cur_idletime_Kernel_Individual) - int(prev_idletime_Kernel_Individual[perCPU]))

        cur_rate_Kernel_Individual = float(delta_worktime_Kernel_Individual)/(delta_worktime_Kernel_Individual + delta_idletime_Kernel_Individual)
        cur_rate_percentage_Kernel_Individual = cur_rate_Kernel_Individual * 100

        prev_worktime_Kernel_Individual[perCPU] = cur_worktime_Kernel_Individual
        prev_idletime_Kernel_Individual[perCPU] = cur_idletime_Kernel_Individual

        #UserMode
        cur_worktime_User_Individual = int(cpu_List[perCPU][2])
        cur_idletime_User_Individual = int(cpu_List[perCPU][4])

        delta_worktime_User_Individual = (int(cur_worktime_Overall_Individual) - int(prev_worktime_Overall_Individual[perCPU]))
        delta_idletime_User_Individual = (int(cur_idletime_Overall_Individual) - int(prev_idletime_Overall_Individual[perCPU]))

        if (delta_worktime_User_Individual + delta_idletime_User_Individual == 0):
            cur_rate_User_Individual = 0
        else:
            cur_rate_User_Individual = float(delta_worktime_User_Individual)/(delta_worktime_User_Individual + delta_idletime_User_Individual)

        cur_rate_percentage_User_Individual = cur_rate_User_Individual * 100

        prev_worktime_User_Individual[perCPU] = cur_worktime_User_Individual
        prev_idletime_User_Individual[perCPU] = cur_idletime_User_Individual
        CPU_Number = ''.join(['CPU',str(perCPU - 1)])

        cpu_Individual_Table.append_row([CPU_Number,(str(cur_rate_percentage_Overall_Individual)[0:4])+"%", (str(cur_rate_percentage_Kernel_Individual)[0:4])+"%", (str(cur_rate_percentage_User_Individual)[0:4])+"%"])
    print "Individual CPU Utilization:"
    print cpu_Individual_Table
    print "Per-Process CPU Utilization"
    print cpu_perProcess_Table
#End for cpu_Util()

#Module for Interrupts
prev_intrr_Overall = 0
def intrr_Util():
    global prev_intrr_Overall;
    intrr_Table = BeautifulTable()
    intrr_Table.column_headers = ["Value", "Interrupts"]

    interr_List = open("/proc/stat","r")
    regexp_Interr = re.compile("intr*.")
    new_Interr_List = filter(regexp_Interr.match, interr_List)
    interr_List = [line.split() for line in new_Interr_List]
    cur_intrr_Overall = int(interr_List[0][1])

    delta_intrr_Overall = float(prev_intrr_Overall + cur_intrr_Overall)/2
    prev_intrr_Overall = cur_intrr_Overall

    intrr_Table.append_row(["Total Interrupts", cur_intrr_Overall])
    print "Total Interrupts handled"
    print intrr_Table

#End of intrr_Util

#Module for ContextSwitches
prev_ctxt_Overall = 0
def ctxt_Util():
    global prev_ctxt_Overall;
    ctxt_Table = BeautifulTable()
    ctxt_Table.column_headers = ["Value", "ContextSwitches"]

    ctxt_List = open("/proc/stat","r")
    regexp_ctxt = re.compile("ctxt*.")
    new_ctxt_List = filter(regexp_ctxt.match, ctxt_List)
    ctxt_List = [line.split() for line in new_ctxt_List]

    cur_ctxt_Overall = int(ctxt_List[0][1])

    delta_ctxt_Overall = float(prev_ctxt_Overall + cur_ctxt_Overall)/2
    prev_ctxt_Overall = cur_ctxt_Overall

    ctxt_Table.append_row(["Total Context Switches", cur_ctxt_Overall])
    print "Total ContextSwitches handled"
    print ctxt_Table
#End of ctxt_Util

#Module for Memory_Utilization
prev_mem_Used = 0

def mem_Util():
    global  prev_mem_Used;
    mem_Table = BeautifulTable()

    mem_Table.column_headers = ["Total Memory", "Free Memory", "Memory Utilization"]
    meminfo_List = open("/proc/meminfo", "r")
    mem_List = [line.split() for line in meminfo_List]
    cur_mem_Total = int(mem_List[0][1])
    cur_mem_Free = int(mem_List[1][1])

    cur_mem_Used = float(cur_mem_Total - cur_mem_Free)
    delta_mem_Used = float(cur_mem_Used + prev_mem_Used)/2

    Total_delta_Used = float(cur_mem_Used - prev_mem_Used)
    cur_mem_Percentage_Used = (delta_mem_Used/cur_mem_Total) * 100

    prev_mem_Used = cur_mem_Used

    mem_Table.append_row([str(cur_mem_Total)+' bytes', str(cur_mem_Free)+' bytes', (str(cur_mem_Percentage_Used)[0:4])+'%'])
    print "Total Memory Utilization:"
    print mem_Table
#End of mem_Util

#Module for Network Utilization
prev_netIO_Overall = 0
def netIO_Util():
    global prev_netIO_Overall, net_BANDWIDTH
    netIO_Table = BeautifulTable()
    netIO_Table.column_headers = ["Network Utilization", "Number of active TCP"]

    netIOTemp1_List = os.listdir("/sys/class/net")  #The same information can be used from /proc/tcp/dev
    regexp_netIO = re.compile("en.")
    netIOTemp2_List = filter(regexp_netIO.match, netIOTemp1_List)
    new_netIO_List = [line.split() for line in netIOTemp2_List]
    for word in new_netIO_List:
        etheret_port = str(word[0])

    netIO_transmitted = ''.join(['/sys/class/net/',etheret_port,'/statistics/tx_bytes'])
    netIOinfo_List = open(netIO_transmitted)

    netIO_List = [line.split() for line in netIOinfo_List]
    net_BANDW1DTH = netIO_List[0][0]

    netIO_List = ''.join(netIO_List[0])
    cur_netIO_Overall = int(netIO_List)
    delta_netIO_Overall = cur_netIO_Overall - prev_netIO_Overall
    netIO_KB_Overall = delta_netIO_Overall / (net_BANDWIDTH * sleep_Value)
    prev_netIO_Overall = cur_netIO_Overall

    #Active TCP Connections
    netTcp_Util = open("/proc/net/sockstat", 'r')   #The same value is present in /proc/tcp/dev
    netTcpinfo_List = [line.split() for line in netTcp_Util]
    netTcp_Active = netTcpinfo_List[1][2]

    netIO_Table.append_row([str(netIO_KB_Overall)+'/Second', netTcp_Active])
    print "Total Network Utilization:"
    print netIO_Table
#End of netIO_Util

#user_Input
sleep_Value = 1
def user_Input():
    global sleep_Value
    try:
        print "Options:"
        print "1:Every 1 Second"
        print "3:Every 3 Seconds"
        print "5:Every 5 Seconds"
        print "Enter option"
        sleep_Value = int(raw_input())
        main()
    except KeyboardInterrupt:
        main_Menu()

#Module for displaying the program Menu
def main_Menu():
    os.system("printf '\033c'")

    print "1:Change the refresh rate?"
    print "2:Enter the process ID for Utilization (Default is PID -> 1)"
    print "3:Return to program execution"
    print "4:EXIT the program"
    print "Enter your choice"

    try:
        switch = int(raw_input())
        if switch == 1:
            user_Input()
        elif switch == 2:
            processName()
        elif switch == 3:
            main()
        elif switch == 4:
            exit(0)
            print "You Entered a wrong choice"
        else:
            main_Menu()
    except ValueError:
        print "Please enter a valid choice:"
        main_Menu()
    except KeyboardInterrupt:
        main_Menu()
#End of main_Menu()

#Calling all the modules
def main():
    try:
        cpu_Count()
        set_variable()
        while True:
            print "To view main_Menu, enter ^C (Control-c)"
            cpu_Print()
            cpu_Util()
            intrr_Util()
            ctxt_Util()
            mem_Util()
            disk_Util()
            netIO_Util()
            time.sleep(sleep_Value)
            os.system("printf '\033c'")

    except KeyboardInterrupt:
        main_Menu()
main()
