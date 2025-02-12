import argparse, os, shutil

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
    
    for file_path in files_to_delete:
        os.remove(file_path)
        files_removed.append(os.path.basename(file_path))

    return {
        'added_files': files_added,
        'removed_files': files_removed
    }