from pathlib import Path
cwd = Path(__file__).parent.parent.parent

import re
import requests
import tarfile
import random
random.seed(3)  # for reproducability
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_data(output_dir:Path):
    # names for files and folders
    tar_file = Path('2_LamaH-CE_daily.tar.gz')
    url = f"https://zenodo.org/record/5153305/files/{tar_file.name}?download=1"
    target_folder = "A_basins_total_upstrm/2_timeseries/daily/"

    # Download file
    logger.info("No files found in local directory: Downloading file...")
    print("Downloading file...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(tar_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        logger.info("File downloaded successfully!")
    else:
        logger.error(f"Failed to download file. Status code: {response.status_code}")

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)


    # Open the tar file
    logger.info("Opening tar file...")
    with tarfile.open(tar_file, "r:gz") as tar:
        # Filter for CSV files in the target directory
        files = [
            member for member in tar.getmembers()
            if member.name.startswith(target_folder) and member.name.endswith(".csv")
        ]

        # Randomly sample 100 files
        files_to_extract = random.sample(files, 100)
        logger.info(f"Extracting {len(files_to_extract)} CSV files...")
        for member in files_to_extract:
            member.name = Path(member.name).name
            tar.extract(member, path=output_dir)

    logger.info(f"Random CSV files extracted to '{output_dir}'")
    tar_file.unlink()


def create_df(data_dir:Path= cwd / 'data' ):
    if not data_dir.exists():
        get_data()
        logger.info('Data directory created and files downloaded.')

    data_files = []
    col_map = {'YYYY':'year', 'MM': 'month', 'DD': 'day'}
    levels = list(col_map.values())

    for path in data_dir.glob('*ID_*.csv'):
        file_number = int(re.findall(r'\d+', str(path.name))[0])
        data = pd.read_csv(path, sep=';')
        if len(data.index) < 1 or len(data.columns) < 3:
            logger.warning(f'Something went wrong with file: {path}')
            return None
        else:
            data['region'] = file_number
            data.rename(columns=col_map, inplace=True)
            data['date'] = pd.to_datetime(data.loc[:, levels])
            data_files.append(data)

    levels.append('region')

    if not data_files:
        logger.error("No valid data files were found or processed.")
        raise ValueError("No valid data files were found or processed.")

    data_files = [df for df in data_files if df is not None]
    data = pd.concat(data_files).set_index(levels).sort_index()
    logger.info("Dataframe created successfully.")
    return data


if __name__ == '__main__':
    create_df()
