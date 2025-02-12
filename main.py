import argparse, os, shutil
import time
from datetime import datetime

def parse_args():

    parser = argparse.ArgumentParser(description='Syncronize source and replica folders')

    parser.add_argument('source', help='Path to source folder')
    parser.add_argument('replica', help='Path to replica folder')
    parser.add_argument('sync_interval', type=int, help='Sync interval in seconds')
    parser.add_argument('log', help='Path to log file')

    return parser.parse_args()

def list_files(folder):

    # Create unique set of filenames
    unique_files = set()

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), folder)
            unique_files.add(rel_path)
    
    return unique_files


def update_replica(source_folder, replica_folder):

    # Check for source folder
    if not os.path.exists(source_folder):
        raise Exception(f'The folder {source_folder} does not exist.')
    elif not os.path.exists(replica_folder):
        os.mkdir(replica_folder)
        
    source_folder_files = list_files(source_folder)
    replica_folder_files = list_files(replica_folder)

    # Check if there are files in source folder that is not in the replica folder
    files_to_copy = source_folder_files - replica_folder_files
    files_to_delete = replica_folder_files - source_folder_files
    
    files_added = []
    files_removed = []

    for file_path in files_to_copy:
        src_path = os.path.join(source_folder, file_path)
        dest_path = os.path.join(replica_folder, file_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Ensure directories exist
        shutil.copy(src_path, dest_path)
        files_added.append(file_path)
    
    for file_path in files_to_delete:
        os.remove(os.path.join(replica_folder, file_path))
        files_removed.append(os.path.basename(file_path))

    return files_added, files_removed

def log_changes(files_added, files_removed, log_file='logs/sync.log'):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] Changes:\n'

    if files_added:
        log_entry += f'Files added: {", ".join(files_added)}\n'
    if files_removed:
        log_entry += f'Files removed: {", ".join(files_removed)}\n'

    # Log the changes when they happen
    if files_added or files_removed:
        with open(log_file, 'a') as f:
            f.write(log_entry)

        print(log_entry)

def start_sync(source, replica, sync_interval):
    try:
        while True:
            files_added, files_removed = update_replica(source, replica)
            log_changes(files_added, files_removed)
            time.sleep(sync_interval)
    except KeyboardInterrupt:
        print('Sync terminated.')

if __name__ == '__main__':
    # Parse arguments to command line
    args = parse_args()

    # Start the synchronization
    start_sync(args.source, args.replica, args.sync_interval)