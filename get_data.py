import requests
import tarfile
import os
import random
random.seed(3)  # for reproducability


def get_data():
    # names for files and folders
    tar_file = "2_LamaH-CE_daily.tar.gz"
    url = f"https://zenodo.org/record/5153305/files/{tar_file}?download=1"
    output_dir = "data"
    target_folder = "A_basins_total_upstrm/2_timeseries/daily/"

    # Download file
    print("Downloading file...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(tar_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("File downloaded successfully!")
    else:
        print("Failed to download file. Status code: ", response.status_code)

    # Create the output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the tar file
    print("Opening tar file...")
    with tarfile.open(tar_file, "r:gz") as tar:
        # Filter for CSV files in the target directory
        files = [
            member for member in tar.getmembers()
            if member.name.startswith(target_folder) and member.name.endswith(".csv")
        ]

        # Randomly sample 100 files
        files_to_extract = random.sample(files, 100)
        print(f"Extracting {len(files_to_extract)} CSV files...")
        for member in files_to_extract:
            member.name = os.path.basename(member.name)  # Strip directory structure
            tar.extract(member, path=output_dir)

    print(f"Random CSV files extracted to '{output_dir}'")
    print('Removing Tar file...')
    os.remove(tar_file)


if __name__ == '__main__':
    get_data()
