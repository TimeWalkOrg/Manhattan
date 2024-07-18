import os
import re

# Configuration
local_dir = "Manhattan.wiki"
images_prefix_to_remove = "Manhattan.wiki/"
new_remote = "https://[INSERT_GITHUB_PERSONAL_ACCESS_TOKEN]@github.com/TimeWalkOrg/Manhattan_public.wiki.git"

# Step 1: Function to update markdown files
def update_markdown_file(file_path, prefix_to_remove):
    print(f"Processing file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find all image URLs in Markdown and HTML img tags
    image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)
    img_tag_urls = re.findall(r'<img.*?src="(.*?)".*?>', content)
    image_urls.extend(img_tag_urls)

    if image_urls:
        print(f"Found image URLs: {image_urls}")
    else:
        print("No image URLs found.")
    
    for img_url in image_urls:
        if img_url.startswith(prefix_to_remove):
            new_path = img_url.replace(prefix_to_remove, '', 1)
            content = content.replace(img_url, new_path)
    
    with open(file_path, 'w') as file:
        file.write(content)

# Step 2: Process all markdown files in the specified directory
for root, dirs, files in os.walk(local_dir):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            update_markdown_file(file_path, images_prefix_to_remove)

print("Image paths updated successfully.")

# Step 3: Commit and push changes to the new wiki repository
os.system(f"cd {local_dir} && git add .")
os.system(f"cd {local_dir} && git commit -m 'Fix image paths'")
os.system(f"cd {local_dir} && git remote remove new-wiki || true")
os.system(f"cd {local_dir} && git remote add new-wiki {new_remote}")
os.system(f"cd {local_dir} && git pull new-wiki master --allow-unrelated-histories")

pull_result = os.system(f"cd {local_dir} && git pull new-wiki master --allow-unrelated-histories")
if pull_result != 0:
    print("Merge conflicts detected. Please resolve them manually and then run the script again.")
else:
    os.system(f"cd {local_dir} && git push new-wiki master")
