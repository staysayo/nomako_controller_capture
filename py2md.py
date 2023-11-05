import re
import argparse

# Define a function to extract comments and tags from a Python script
def extract_comments_and_tags(script_content):
    comments_and_tags = []
    comment_pattern = r'@([a-zA-Z_0-9]+)\s+(.*?)\n'
    matches = re.findall(comment_pattern, script_content)
    for match in matches:
        comments_and_tags.append(match)
    return comments_and_tags

# Create a command-line argument parser
parser = argparse.ArgumentParser(description='Generate a Markdown README.md file from a Python script.')

# Add input and output file arguments
parser.add_argument('input_file', help='Path to the input Python script')
parser.add_argument('output_file', help='Path to the output README.md file')

# Parse the command-line arguments
args = parser.parse_args()

# Read the content of the input Python script
with open(args.input_file, 'r') as file:
    script_content = file.read()

# Extract comments and tags from the script
comments_and_tags = extract_comments_and_tags(script_content)

# Create a Markdown formatted README.md content
markdown_content = "# README\n\n"

# Add a Description section
description_found = False
for tag, description in comments_and_tags:
    if tag == 'description':
        markdown_content += f"## Description\n\n{description}\n\n"
        description_found = True
        break

# Add a Comments and Tags section
markdown_content += "## Comments and Tags\n\n"
for tag, description in comments_and_tags:
    if tag != 'description':
        markdown_content += f"### `{tag}`\n\n{description}\n\n"

# If no Description was found, provide a default message
if not description_found:
    markdown_content += "## Description\n\n(No description provided)\n\n"

# Write the Markdown content to the output README.md file
with open(args.output_file, 'w') as readme_file:
    readme_file.write(markdown_content)

print(f"{args.output_file} generated successfully from {args.input_file}.")
