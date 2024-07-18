import os
import re
import shutil
import requests

# Configuration
repo_url = "https://[INSERT_GITHUB_PERSONAL_ACCESS_TOKEN]@github.com/TimeWalkOrg/Manhattan.wiki.git"
local_dir = "Manhattan.wiki"
images_dir = os.path.join(local_dir, "images")
new_remote = "https://[INSERT_GITHUB_PERSONAL_ACCESS_TOKEN]@github.com/TimeWalkOrg/Manhattan_public.wiki.git"
personal_access_token = "[INSERT_GITHUB_PERSONAL_ACCESS_TOKEN]"

# Step 0: Remove the local directory if it already exists
if os.path.exists(local_dir):
    shutil.rmtree(local_dir)

# Step 1: Clone the wiki repository
os.system(f"git clone {repo_url} {local_dir}")

# Step 2: Create images directory
os.makedirs(images_dir, exist_ok=True)

# Step 3: Function to download an image with headers
def download_image(url, dest_folder):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': f'token {personal_access_token}'
    }
    print(f"Downloading image from {url}")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_name = os.path.join(dest_folder, os.path.basename(url))
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Saved image to {file_name}")
        return file_name
    else:
        print(f"Failed to download image from {url}, status code: {response.status_code}")
    return None

# Step 4: Function to update markdown files with downloaded images
def update_markdown_file(file_path, images_folder):
    print(f"Processing file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find all image URLs using regular expressions
    image_urls = re.findall(r'!\[.*?\]\((https?://.*?)\)', content)
    if image_urls:
        print(f"Found image URLs: {image_urls}")
    else:
        print("No image URLs found.")
    
    for img_url in image_urls:
        local_image_path = download_image(img_url, images_folder)
        if local_image_path:
            content = content.replace(img_url, local_image_path)
    
    with open(file_path, 'w') as file:
        file.write(content)

# Step 5: Process all markdown files in the wiki repository
for root, dirs, files in os.walk(local_dir):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            update_markdown_file(file_path, images_dir)

# Step 6: Remove existing remote if it exists and add the new remote
os.system(f"cd {local_dir} && git remote remove new-wiki || true")
os.system(f"cd {local_dir} && git remote add new-wiki {new_remote}")

# Step 7: Pull latest changes from the remote repository
os.system(f"cd {local_dir} && git pull new-wiki master --allow-unrelated-histories")

# Step 8: Commit and push changes to the new wiki repository
os.system(f"cd {local_dir} && git add .")
os.system(f"cd {local_dir} && git commit -m 'Add images and update paths'")
os.system(f"cd {local_dir} && git push new-wiki master")
