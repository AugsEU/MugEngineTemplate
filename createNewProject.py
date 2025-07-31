import os
import shutil
import argparse
import re
import subprocess

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

def create_gitignore(project_name, gitignore_path):
    """Create .gitignore file with specified patterns."""
    gitignore_content = f"""/{project_name}/{project_name}/bin/
/{project_name}/{project_name}/obj/
/{project_name}/{project_name}/.config/
/{project_name}/{project_name}/@Data/bin/
/{project_name}/{project_name}/@Data/obj/
/{project_name}/.vs/
/{project_name}/{project_name}/{project_name}.csproj.user
"""
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)

def run_git_command(cwd, *args):
    """Run a git command in the specified directory."""
    try:
        subprocess.run(["git", *args], cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git command failed in {cwd}: git {' '.join(args)}")
        raise

def process_template(name):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "MugEngineTemplate")
    
    # Create the new directory structure
    new_root_dir = os.path.join(script_dir, name)
    new_inner_dir = os.path.join(new_root_dir, name)
    
    # Check if required folders exist
    if not os.path.exists(template_dir):
        print(f"Error: MugEngineTemplate folder not found in {script_dir}")
        return
    
    # Check if target directory already exists
    if os.path.exists(new_root_dir):
        print(f"Error: {name} folder already exists")
        return
    
    try:
        # Create the directory structure
        os.makedirs(new_inner_dir)
        
        # Copy the template into the inner directory
        print(f"Copying MugEngineTemplate to {os.path.join(name, name)}...")
        shutil.copytree(template_dir, new_inner_dir, dirs_exist_ok=True)
        
        # Initialize git repository
        print("Initializing git repository...")
        run_git_command(new_root_dir, "init")
        
        # Create .gitignore
        gitignore_path = os.path.join(new_root_dir, ".gitignore")
        print("Creating .gitignore...")
        create_gitignore(name, gitignore_path)
        
        # Add MugEngine as submodule
        print("Adding MugEngine as submodule...")
        run_git_command(new_root_dir, "submodule", "add", "https://github.com/AugsEU/MugEngine")
        
        # Initialize and update submodules recursively
        print("Updating MugEngine submodules recursively...")
        mugengine_dir = os.path.join(new_root_dir, "MugEngine")
        run_git_command(mugengine_dir, "submodule", "update", "--init", "--recursive")
        
        # Process all files in the inner directory to replace text content
        print("Replacing text in files...")
        for root, _, files in os.walk(new_inner_dir):
            for file in files:
                filepath = os.path.join(root, file)
                replace_in_file(filepath, "MugEngineTemplate", name)
        
        # Rename files and folders containing the template name in the inner directory
        print("Renaming files and folders...")
        rename_files_and_folders(new_inner_dir, "MugEngineTemplate", name)
        
        # Initial git commit
        print("Creating initial commit...")
        run_git_command(new_root_dir, "add", ".")
        run_git_command(new_root_dir, "commit", "-m", "Initial commit from template")
        
        print(f"\nSuccessfully created new project at: {new_root_dir}")
        print(f"Project structure:")
        print(f"{name}/")
        print(f"├── {name}/ (renamed MugEngineTemplate)")
        print(f"├── MugEngine/ (git submodule with all submodules initialized)")
        print(f"├── .git/")
        print(f"├── .gitignore")
        print(f"└── .gitmodules")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        if os.path.exists(new_root_dir):
            shutil.rmtree(new_root_dir)
    except Exception as e:
        # Clean up if something went wrong
        if os.path.exists(new_root_dir):
            shutil.rmtree(new_root_dir)
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a new project from MugEngineTemplate.')
    parser.add_argument('name', type=str, help='Name of the new project')
    args = parser.parse_args()
    
    process_template(args.name)