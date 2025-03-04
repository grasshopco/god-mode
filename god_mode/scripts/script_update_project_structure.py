#!/usr/bin/env python3
"""
Project Structure Update Script

This script scans the entire project directory structure and generates an updated
project_structure.md file with descriptions of all directories and files.

Usage:
    python script_update_project_structure.py

The script will:
1. Scan the project directory structure
2. Generate a markdown file with a hierarchical representation of the structure
3. Preserve existing descriptions by parsing the current project_structure.md file
4. Update the project_structure.md file with the new structure and preserved descriptions
"""

import os
import re
import sys
from pathlib import Path
import datetime

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the path to the project structure file
PROJECT_STRUCTURE_FILE = Path(SCRIPT_DIR).parent / "memory" / "memory_project_structure.md"

# Define directories to ignore
IGNORE_DIRS = [
    '.git',
    'node_modules',
    '__pycache__',
    '.venv',
    'venv',
    'env',
    '.env',
    'build',
    'dist',
    '.DS_Store',
]

# Define files to ignore
IGNORE_FILES = [
    '.DS_Store',
    '.gitignore',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '*.so',
    '*.dll',
    '*.exe',
    '*.obj',
    '*.o',
    '*.a',
    '*.lib',
    '*.swp',
    '*.swo',
    '*.swn',
    '*~',
]

def parse_existing_structure():
    """
    Parse the existing project structure file to extract descriptions.
    
    Returns:
        dict: A dictionary mapping file/directory paths to descriptions
    """
    descriptions = {}
    
    if not PROJECT_STRUCTURE_FILE.exists():
        return descriptions
    
    with open(PROJECT_STRUCTURE_FILE, 'r') as f:
        content = f.read()
    
    # Extract file/directory descriptions
    # Look for lines like '* 📄 `file.txt` - Description here'
    # or '* **📁 directory/** - Description here'
    pattern = r'\* (?:\*\*)?[📁📄🐍🟨📝⚙️🎨]+ [`"]?([^`"\*]+)[`"]?(?:\*\*)? - (.+)'
    matches = re.findall(pattern, content)
    
    for path, description in matches:
        # Normalize path to ensure consistency
        norm_path = path.rstrip('/') + ('/' if '/' in path and not path.endswith('/') else '')
        descriptions[norm_path] = description.strip()
    
    return descriptions

def should_ignore(path):
    """
    Check if a path should be ignored.
    
    Args:
        path (Path): The path to check
        
    Returns:
        bool: True if the path should be ignored, False otherwise
    """
    # Check if the path is a directory that should be ignored
    if path.is_dir() and path.name in IGNORE_DIRS:
        return True
    
    # Check if the path is a file that should be ignored
    if path.is_file():
        if path.name in IGNORE_FILES:
            return True
        for pattern in IGNORE_FILES:
            if '*' in pattern and path.match(pattern):
                return True
    
    return False

def extract_file_description(file_path, default_description=None):
    """
    Extract a description from a file's docstring, header comment, or other sources.
    
    Args:
        file_path (Path): The path to the file
        default_description (str): A default description to use if none can be extracted
        
    Returns:
        str: The extracted description or default
    """
    if not file_path.exists() or not file_path.is_file():
        return default_description
    
    try:
        # Read the first few lines of the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f.readline() for _ in range(25)]  # Read first 25 lines
        
        # Join the lines for easier searching
        content = ''.join(lines)
        
        # Try different patterns to extract a description
        
        # Python docstring
        py_docstring = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if py_docstring:
            doc = py_docstring.group(1).strip()
            first_line = doc.split('\n')[0].strip()
            if first_line:
                return first_line
        
        # Python hash comment
        py_comment = re.search(r'# (.+)', content)
        if py_comment:
            return py_comment.group(1).strip()
        
        # JavaScript/TypeScript block comment
        js_comment = re.search(r'/\*\*(.*?)\*/', content, re.DOTALL)
        if js_comment:
            doc = js_comment.group(1).strip()
            first_line = doc.split('\n')[0].strip().lstrip('*').strip()
            if first_line:
                return first_line
        
        # JavaScript/TypeScript line comment
        js_line_comment = re.search(r'// (.+)', content)
        if js_line_comment:
            return js_line_comment.group(1).strip()
        
        # HTML comment
        html_comment = re.search(r'<!--(.*?)-->', content, re.DOTALL)
        if html_comment:
            doc = html_comment.group(1).strip()
            first_line = doc.split('\n')[0].strip()
            if first_line:
                return first_line
        
        # Markdown heading
        md_heading = re.search(r'# (.+)', content)
        if md_heading and file_path.suffix.lower() in ['.md', '.markdown']:
            return md_heading.group(1).strip()
        
        # Bash script comment
        bash_comment = re.search(r'#!.*\n# (.+)', content)
        if bash_comment:
            return bash_comment.group(1).strip()
        
        # If we couldn't find a description, return the default
        return default_description
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return default_description

def scan_directory(directory, prefix='', descriptions=None, indent_level=0, processed_paths=None):
    """
    Recursively scan a directory and generate a markdown representation.
    
    Args:
        directory (Path): The directory to scan
        prefix (str): The prefix to use for relative paths
        descriptions (dict): A dictionary mapping file/directory paths to descriptions
        indent_level (int): The current indentation level
        processed_paths (set): Set of already processed paths to avoid duplicates
        
    Returns:
        list: A list of markdown lines representing the directory structure
    """
    if descriptions is None:
        descriptions = {}
    
    if processed_paths is None:
        processed_paths = set()
    
    result = []
    indent = '  ' * indent_level
    
    try:
        # Sort directories first, then files
        dirs = []
        files = []
        
        for path in sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            if not should_ignore(path):
                # Create a relative path for checking duplicates
                rel_path = f"{prefix}{path.name}" + ('/' if path.is_dir() else '')
                
                # Skip if we've already processed this path
                if rel_path in processed_paths:
                    continue
                
                processed_paths.add(rel_path)
                
                if path.is_dir():
                    dirs.append(path)
                else:
                    files.append(path)
        
        # Process directories
        for path in dirs:
            rel_path = f"{prefix}{path.name}/"
            
            # Get description from existing descriptions or generate a default
            description = descriptions.get(rel_path, "Directory")
            
            # If the description is just "Directory", try to infer a better one
            if description == "Directory":
                # Check if there's a README.md in the directory
                readme_path = path / "README.md"
                if readme_path.exists():
                    readme_desc = extract_file_description(readme_path)
                    if readme_desc:
                        description = readme_desc
            
            # Enhanced visual hierarchy with emoji and bold formatting
            result.append(f"{indent}* **📁 {path.name}/** - {description}")
            
            # Recursively scan subdirectories
            sub_result = scan_directory(
                path, 
                prefix=f"{prefix}{path.name}/", 
                descriptions=descriptions,
                indent_level=indent_level + 1,
                processed_paths=processed_paths
            )
            
            result.extend(sub_result)
        
        # Process files
        for path in files:
            rel_path = f"{prefix}{path.name}"
            
            # Get file info
            size_kb = round(path.stat().st_size / 1024, 1) if path.exists() else 0
            lines = 0
            
            # Count lines in text files
            if path.suffix.lower() in ['.md', '.txt', '.py', '.js', '.css', '.html', '.jsx', '.tsx', '.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf']:
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = sum(1 for _ in f)
                except:
                    pass
            
            # Get file description from existing descriptions or extract from the file
            file_info = f"File ({size_kb}KB, {lines} lines)"
            description = descriptions.get(rel_path, None)
            
            # If no description exists or it's just the default file info, try to extract one
            if not description or description.startswith("File ("):
                extracted_desc = extract_file_description(path)
                if extracted_desc:
                    description = f"{file_info} - {extracted_desc}"
                else:
                    description = file_info
            
            # Use different emoji based on file type
            emoji = "📄"  # Default file emoji
            if path.suffix.lower() in ['.py']:
                emoji = "🐍"  # Python files
            elif path.suffix.lower() in ['.js', '.jsx', '.ts', '.tsx']:
                emoji = "🟨"  # JavaScript/TypeScript files
            elif path.suffix.lower() in ['.md', '.txt']:
                emoji = "📝"  # Documentation files
            elif path.suffix.lower() in ['.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf']:
                emoji = "⚙️"  # Configuration files
            elif path.suffix.lower() in ['.css', '.scss', '.sass', '.less', '.html']:
                emoji = "🎨"  # Web files
            
            # Enhanced visual hierarchy with emoji
            result.append(f"{indent}* {emoji} `{path.name}` - {description}")
    
    except Exception as e:
        result.append(f"{indent}* ❌ Error scanning {directory}: {e}")
    
    return result

def generate_structure_content(descriptions):
    """
    Generate the content for the project structure file.
    
    Args:
        descriptions (dict): A dictionary mapping file/directory paths to descriptions
        
    Returns:
        str: The content for the project structure file
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = [
        "# Project Structure",
        "",
        "This document maps the entire project codebase, providing descriptions of directories and key files to help navigate the project.",
        "",
        "## Legend",
        "",
        "* 📁 Directory",
        "* 📄 Generic file",
        "* 🐍 Python file",
        "* 🟨 JavaScript/TypeScript file",
        "* 📝 Documentation file",
        "* ⚙️ Configuration file",
        "* 🎨 Web file (HTML, CSS)",
        "",
        "## Root Directory",
        "",
    ]
    
    # Scan the project root
    content.extend(scan_directory(PROJECT_ROOT, descriptions=descriptions))
    
    content.extend([
        "",
        "---",
        "",
        f"*This document was automatically generated on {timestamp}. The AI assistant maintains it to ensure it accurately reflects the current state of the codebase.*"
    ])
    
    return '\n'.join(content)

def update_project_structure():
    """Update the project structure file."""
    print(f"Updating project structure file: {PROJECT_STRUCTURE_FILE}")
    
    # Ensure the directory exists
    os.makedirs(PROJECT_STRUCTURE_FILE.parent, exist_ok=True)
    
    # Parse existing structure to preserve descriptions
    descriptions = parse_existing_structure()
    print(f"Found {len(descriptions)} existing descriptions")
    
    # Generate new content
    content = generate_structure_content(descriptions)
    
    # Write to file
    with open(PROJECT_STRUCTURE_FILE, 'w') as f:
        f.write(content)
    
    line_count = len(content.split('\n'))
    print(f"Updated project structure file with {line_count} lines")

if __name__ == "__main__":
    update_project_structure() 