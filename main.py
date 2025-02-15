import argparse, os, shutil
import time
from datetime import datetime

# Parses command-line arguments
def parse_args():

    parser = argparse.ArgumentParser(description='Synchronize source and replica folders')

    parser.add_argument('source', help='Path to source folder')
    parser.add_argument('replica', help='Path to replica folder')
    parser.add_argument('sync_interval', type=int, help='Sync interval in seconds')
    parser.add_argument('log', help='Path to log file')

    return parser.parse_args()

# Lists all files in a folder
def list_files(folder):

    # Create unique set of filenames (avoid duplicates)
    unique_files = set()

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), folder)
            unique_files.add(rel_path)
    
    return unique_files

# Updates replica folder to maintain an exact copy of the source folder
def update_replica(source_folder, replica_folder):

    # Check for source folder
    if not os.path.exists(source_folder):
        raise Exception(f'The folder {source_folder} does not exist.') #raise eror if it does not exist
    elif not os.path.exists(replica_folder):
        os.mkdir(replica_folder)
        
    source_folder_files = list_files(source_folder)
    replica_folder_files = list_files(replica_folder)

    # Check if there are files in source folder that is not in the replica folder
    files_to_copy = source_folder_files - replica_folder_files
    # Check if there are files in replica folder that is not in the source folder
    files_to_delete = replica_folder_files - source_folder_files

    subfolder_added = []
    files_added = []
    files_removed = []
    files_updated = []
    subfolder_removed = []


    # Add folders and files from source folder that do not exist in replica folder
    for file_path in files_to_copy:
        src_path = os.path.join(source_folder, file_path)
        dest_path = os.path.join(replica_folder, file_path)
        dest_path_parent = os.path.dirname(dest_path)
        if not os.path.exists(dest_path_parent): # Check for subfolders
            os.makedirs(dest_path_parent) # Create them if they do not exist
            subfolder_added.append(dest_path_parent)
        shutil.copy2(src_path, dest_path) # Copy and preserve timestamps
        files_added.append(os.path.join(source_folder, file_path))
    
    # Deleting files from replica folder that do not exist in source folder
    for file_path in files_to_delete:
        files_removed.append(os.path.join(replica_folder, file_path))
        os.remove(os.path.join(replica_folder, file_path))
        

    # Check if there was any change in a file in source folder that already exists in replica folder using timestamps
    # If there was a change, update the file in replica folder
    for file_path in source_folder_files:
        src_path = os.path.join(source_folder, file_path)
        dest_path = os.path.join(replica_folder, file_path)
        if os.path.exists(src_path) and os.path.exists(dest_path):
            if os.path.getmtime(src_path) > os.path.getmtime(dest_path):
                shutil.copy2(src_path, dest_path)
                files_updated.append(file_path)

    for dirpath, dirnames, _ in os.walk(replica_folder, topdown=False): # Check subfolder before their parent
        for dirname in dirnames:
            if os.listdir(os.path.join(dirpath, dirname)) == []:
                subfolder_removed.append(os.path.join(dirpath, dirname))
                os.rmdir(os.path.join(dirpath, dirname))


    return subfolder_added, files_added, files_removed, files_updated, subfolder_removed

# Create logs in logs/sync.log of each file added or removed to replica folder
def log_changes(subfolder_added, files_added, files_removed, files_updated, subfolder_removed, log_file='logs/sync.log'):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] Changes:\n'

    if subfolder_added:
        log_entry += f'New folder(s) added: {", ".join(subfolder_added)}\n'
    if files_added:
        log_entry += f'File(s) added: {", ".join(files_added)}\n'
    if files_removed:
        log_entry += f'File(s) removed: {", ".join(files_removed)}\n'
    if files_updated:
        log_entry += f'File(s) updated: {", ".join(files_updated)}\n'
    if subfolder_removed:
        log_entry += f'Empty folder(s) removed: {", ".join(subfolder_removed)}\n'

    # Log the changes when they happen
    if files_added or files_removed or files_updated:
        with open(log_file, 'a') as f:
            f.write(log_entry)        
        print(log_entry)

# Sycronization initializer
def start_sync(source, replica, sync_interval):
    try:
        while True:
            subfolder_added, files_added, files_removed, files_updated, subfolder_removed = update_replica(source, replica)
            log_changes(subfolder_added, files_added, files_removed, files_updated, subfolder_removed)
            time.sleep(sync_interval)
    except KeyboardInterrupt:
        print('Sync terminated.')

if __name__ == '__main__':
    # Parse arguments to command line
    args = parse_args()

    # Start the synchronization
    start_sync(args.source, args.replica, args.sync_interval)