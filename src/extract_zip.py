import os
import zipfile
import glob


def find_zip_file(directory="assets"):
    files = glob.glob(os.path.join(directory, "*.zip"))
    if not files:
        raise FileNotFoundError("No .zip file found in 'assets' folder. Please add your images zip file.")
    return files[0]


def extract_input_zip(zip_path, output_dir="assets/images"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Images extracted from {zip_path} to {output_dir}")
    return output_dir
