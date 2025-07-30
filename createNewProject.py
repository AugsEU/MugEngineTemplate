import os
import shutil
import argparse
import re

def replace_in_file(filepath, old_text, new_text):
    """Replace all occurrences of old_text with new_text in the given file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
    except UnicodeDecodeError:
        # Skip binary files
        pass
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")

def rename_files_and_folders(root_dir, old_name, new_name):
    """Recursively rename files and folders containing old_name to new_name."""
    # We need to walk from bottom up when renaming directories
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Rename files first
        for filename in files:
            if old_name in filename:
                old_path = os.path.join(root, filename)
                new_filename = filename.replace(old_name, new_name)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)
        
        # Then rename directories
        for dirname in dirs:
            if old_name in dirname:
                old_path = os.path.join(root, dirname)
                new_dirname = dirname.replace(old_name, new_name)
                new_path = os.path.join(root, new_dirname)
                os.rename(old_path, new_path)

def process_template(name):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "MugEngineTemplate")
    new_dir = os.path.join(script_dir, name)
    
    # Check if template exists
    if not os.path.exists(template_dir):
        print(f"Error: MugEngineTemplate folder not found in {script_dir}")
        return
    
    # Check if target directory already exists
    if os.path.exists(new_dir):
        print(f"Error: {name} folder already exists")
        return
    
    try:
        # Copy the template
        print(f"Copying MugEngineTemplate to {name}...")
        shutil.copytree(template_dir, new_dir)
        
        # Remove .vs folder if it exists
        vs_dir = os.path.join(new_dir, ".vs")
        if os.path.exists(vs_dir):
            print("Removing .vs folder...")
            shutil.rmtree(vs_dir)
        
        # Process all files to replace text content
        print("Replacing text in files...")
        for root, _, files in os.walk(new_dir):
            for file in files:
                filepath = os.path.join(root, file)
                replace_in_file(filepath, "MugEngineTemplate", name)
        
        # Rename files and folders containing the template name
        print("Renaming files and folders...")
        rename_files_and_folders(new_dir, "MugEngineTemplate", name)
        
        print(f"Successfully created new project: {name}")
    except Exception as e:
        # Clean up if something went wrong
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a new project from MugEngineTemplate.')
    parser.add_argument('name', type=str, help='Name of the new project')
    args = parser.parse_args()
    
    process_template(args.name)