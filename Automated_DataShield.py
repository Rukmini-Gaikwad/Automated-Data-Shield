####################################################################
# Program Name : Automated Data Shield (File Duplication System)
# Description  : This application scans a specified directory to
#                identify duplicate files using MD5 checksum 
#                comparison. Redundant copies are removed while
#                preserving one original instance of each file.
# Input        : Directory path
# Output       : Displays detected duplicates and removes extra copies
# Author       : Rukmini Jayhind Gaikwad
# Date         : 18/02/2026
####################################################################

####################################################################
# import module
####################################################################
import sys
import os
import time
import schedule
import shutil
import hashlib
import zipfile

####################################################################
# Function Name : create_backup_archive
# Description   : Creates a compressed zip archive of the backup folder
#                 with timestamp to maintain backup history
# Input         : folder_name (string)
# Output        : Returns created zip file name
####################################################################

def make_zip(folder):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    
    zip_name = folder + "_" +timestamp + ".zip"

    # open the zip file
    zobj = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root,file)
            relative = os.path.relpath(full_path,folder)

            zobj.write(full_path,relative)

    zobj.close()

    return zip_name

####################################################################
# Function Name : calculate_file_hash
# Description   : Calculates MD5 hash value of a file to detect changes
#                 between source and backup files
# Input         : file_path (string)
# Output        : Returns hash value (string)
####################################################################


def calculate_hash(path):
    hobj = hashlib.md5()

    fobj = open(path,"rb")

    while True:
        data = fobj.read(1024)
        if not data:
            break
        else:
            hobj.update(data)

    fobj.close()

    return hobj.hexdigest()

####################################################################
# Function Name : backup_files
# Description   : Copies only new and modified files from source
#                 directory to backup directory using hash comparison
# Input         : source_dir (string), destination_dir (string)
# Output        : Returns list of copied files
####################################################################

def BackupFiles(Source, Destination):
    copied_files = []

    print("Createing the Bckup folder for backup process")

    os.makedirs(Destination, exist_ok= True)

    for root, dirs, files in os.walk(Source):
        for file in files:
            src_path = os.path.join(root,file)

            relative = os.path.relpath(src_path,Source)
            dest_path = os.path.join(Destination, relative)

            os.makedirs(os.path.dirname(dest_path),exist_ok= True)
    
            # Copy the files if its new
            if((not os.path.exists(dest_path)) or (calculate_hash(src_path) != calculate_hash(dest_path))):
                shutil.copy2(src_path, dest_path)
                copied_files.append(relative)

    return copied_files

####################################################################
# Function Name : start_backup_service
# Description   : Starts backup process, performs incremental backup
#                 and creates archive of backup folder
# Input         : source_dir (string, default = "Data")
# Output        : Displays backup status on console
####################################################################

def MarvellousDataShieldStart(Source = "Data"):
    Border = "-"*50
    
    BackupName = "MarvellousBackup"

    print(Border)
    print("Backup Process Started succesfully at : ",time.ctime())
    print(Border)

    files = BackupFiles(Source, BackupName)

    zip_file = make_zip(BackupName)

    print(Border)
    print("Backup completed succesfully")
    print("Files copied : ",len(files))
    print("Zip file gets creatd : ",zip_file)
    print(Border)

####################################################################
# Function Name : main
# Description   : Entry point of program, handles command line
#                 arguments and schedules automatic backup execution
# Input         : Command line arguments
# Output        : Starts scheduled backup service
####################################################################


def main():

    Border = "-"*50
    print(Border)
    print("--------- Marvellous Data Shield System ----------")
    print(Border)

    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This scipt is used to : ")
            print("1 : Takes auto backup at given time")
            print("2 : Backup only new and updated files")
            print("3 : Create an archive of the backup periodically")

        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Use the automation script as")
            print("ScriptName.py TimeInterval SourceDirectory")
            print("TimeInterval : The time in minutes for periodic scheduling")
            print("SourceDirectory : Name of directory to backed up")

        else:
            print("Unable to proceed as there is no such option")
            print("Please use --h or --u to get more details")
    
    # python Demo.py 5 Data
    elif(len(sys.argv) == 3):
        print("Inside projects logic")
        print("Time interval : ",sys.argv[1])
        print("Directory name : ",sys.argv[2])

        # Apply the schedular
        schedule.every(int(sys.argv[1])).minutes.do(MarvellousDataShieldStart, sys.argv[2])

        print(Border)
        print("Data Sheild System started succesfully")
        print("Time interval in minutes: ",sys.argv[1])
        print("Press Ctrl + C to stop the execution")
        print(Border)

        # Wait till abort
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        print("Invalid number of command line arguments")
        print("Unable to proceed as there is no such option")
        print("Please use --h or --u to get more details") 

    print(Border)
    print("--------- Thank you for using our script ---------")
    print(Border)
    
if __name__ == "__main__":
    main()

####################################################################
# Thank You For Using This Application 
####################################################################
