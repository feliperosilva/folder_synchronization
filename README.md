# Folder Synchronization Script

This script synchronizes a **source folder** with a **replica folder**.`  `
The goal is to maintain an exact copy of **source folder** inside the **replica folder**.`  `
It is designed to run periodically at a time interval defined by the user.

## Features

* Syncs files from source folder to replica folder.
* Creates a replica folder if it does not exist.
* Adds files that are in the source folder to the replica folder.
* Removes files from the replica folder that do not exist in the source folder.
* Logs all changes to a log file.

## Requirements

* Python 3.x
* Modules:
    * `argparse`
    * `os`
    * `shutil`
    * `time`
    * `datetime`

## Command-line arguments:
* `source`: Path to source folder
* `replica`: Path to replica folder
* `sync_interval`: Sync interval in seconds
* `log`: Path to log file

### Example
```bash
python main.py /path/to/source /path/to/replica 60 /path/to/log/sync.log
```

This command will:
* Sync files from source to replica.
* Run synchronization every 60 seconds.
* Save existing logs to `/sync.log`.

This script will stop through Keyboard Interruption (`Ctrl+C`)
