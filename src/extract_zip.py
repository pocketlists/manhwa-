import os, zipfile

def extract_input_zip(zip_path, output_dir="assets/images"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Zip file not found: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"✅ Images extracted to {output_dir}")
    return output_dir
