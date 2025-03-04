#!/usr/bin/env python3
"""
Functions and Types Mapper Script

This script scans the project codebase and creates comprehensive documentation
of all functions, methods, classes, and types. It generates structured maps that
help the AI understand the entire codebase at a function level.

Usage:
    python script_update_functions_and_types.py [--target-dir dir]

The script will generate two documentation files:
- memory_functions.md - Documents all functions and methods
- memory_types.md - Documents all classes, interfaces, and types
"""

import os
import sys
import re
import glob
import ast
import json
import argparse
from pathlib import Path
from collections import defaultdict
import subprocess
import datetime

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define the memory directory
MEMORY_DIR = GOD_MODE_DIR / "memory"

# Define output files
FUNCTIONS_FILE = MEMORY_DIR / "memory_functions.md"
TYPES_FILE = MEMORY_DIR / "memory_types.md"

# File extensions to analyze
CODE_EXTENSIONS = {
    'python': ['.py'],
    'javascript': ['.js', '.jsx', '.ts', '.tsx'],
    'typescript': ['.ts', '.tsx'],
    'java': ['.java'],
    'c': ['.c', '.h'],
    'cpp': ['.cpp', '.hpp', '.cc', '.hh', '.cxx', '.hxx'],
    'csharp': ['.cs'],
    'go': ['.go'],
    'ruby': ['.rb'],
    'php': ['.php'],
    'swift': ['.swift'],
    'rust': ['.rs'],
}

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    try:
        # Try to use the helper script if available
        timestamp_script = SCRIPT_DIR / "utils" / "script_timestamp.py"
        if timestamp_script.exists():
            result = subprocess.run(
                [sys.executable, str(timestamp_script)],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
    except Exception as e:
        print(f"Error using timestamp script: {e}", file=sys.stderr)
    
    # Fallback to built-in datetime
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def determine_language(file_path):
    """Determine the programming language of a file based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    for lang, extensions in CODE_EXTENSIONS.items():
        if ext in extensions:
            return lang
    return None

class PythonAnalyzer:
    """Analyze Python files for functions, classes, and other definitions."""
    
    @staticmethod
    def analyze_file(file_path):
        """
        Analyze a Python file for functions, classes, and types.
        
        Args:
            file_path (str): Path to the Python file
            
        Returns:
            tuple: (functions, types) where each is a list of dictionaries
        """
        functions = []
        types = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=file_path)
            
            # Track current class for methods
            current_class = None
            
            for node in ast.walk(tree):
                # Get file-level functions
                if isinstance(node, ast.FunctionDef) and not current_class:
                    functions.append({
                        'name': node.name,
                        'type': 'function',
                        'file': file_path,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'doc': ast.get_docstring(node) or '',
                    })
                
                # Get classes and their methods
                elif isinstance(node, ast.ClassDef):
                    current_class = node.name
                    bases = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            bases.append(base.id)
                        elif isinstance(base, ast.Attribute):
                            bases.append(f"{base.value.id}.{base.attr}")
                    
                    types.append({
                        'name': node.name,
                        'type': 'class',
                        'file': file_path,
                        'line': node.lineno,
                        'bases': bases,
                        'doc': ast.get_docstring(node) or '',
                    })
                    
                    # Get class methods
                    for class_node in node.body:
                        if isinstance(class_node, ast.FunctionDef):
                            functions.append({
                                'name': f"{current_class}.{class_node.name}",
                                'type': 'method',
                                'file': file_path,
                                'line': class_node.lineno,
                                'args': [arg.arg for arg in class_node.args.args],
                                'doc': ast.get_docstring(class_node) or '',
                            })
                    
                    current_class = None
            
            return functions, types
        
        except Exception as e:
            print(f"Error analyzing Python file {file_path}: {e}", file=sys.stderr)
            return [], []

class JavaScriptAnalyzer:
    """Analyze JavaScript/TypeScript files for functions, classes, and interfaces."""
    
    @staticmethod
    def analyze_file(file_path):
        """
        Analyze a JavaScript/TypeScript file for functions, classes, and types.
        
        Args:
            file_path (str): Path to the JS/TS file
            
        Returns:
            tuple: (functions, types) where each is a list of dictionaries
        """
        functions = []
        types = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find functions
            function_pattern = r'(function\s+(\w+)\s*\(([^)]*)\)|const\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>|(\w+)\s*\(([^)]*)\)\s*{)'
            for match in re.finditer(function_pattern, content):
                name = match.group(2) or match.group(4) or match.group(6)
                args = match.group(3) or match.group(5) or match.group(7) or ''
                line_no = content[:match.start()].count('\n') + 1
                
                functions.append({
                    'name': name,
                    'type': 'function',
                    'file': file_path,
                    'line': line_no,
                    'args': [arg.strip() for arg in args.split(',') if arg.strip()],
                    'doc': '',  # Extract JSDoc if needed
                })
            
            # Find classes
            class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{'
            for match in re.finditer(class_pattern, content):
                name = match.group(1)
                base = match.group(2) or ''
                line_no = content[:match.start()].count('\n') + 1
                
                types.append({
                    'name': name,
                    'type': 'class',
                    'file': file_path,
                    'line': line_no,
                    'bases': [base] if base else [],
                    'doc': '',  # Extract JSDoc if needed
                })
            
            # Find interfaces (TypeScript)
            if file_path.endswith(('.ts', '.tsx')):
                interface_pattern = r'interface\s+(\w+)(?:\s+extends\s+([^{]+))?\s*{'
                for match in re.finditer(interface_pattern, content):
                    name = match.group(1)
                    bases_str = match.group(2) or ''
                    bases = [b.strip() for b in bases_str.split(',') if b.strip()]
                    line_no = content[:match.start()].count('\n') + 1
                    
                    types.append({
                        'name': name,
                        'type': 'interface',
                        'file': file_path,
                        'line': line_no,
                        'bases': bases,
                        'doc': '',  # Extract JSDoc if needed
                    })
                
                # Find types (TypeScript)
                type_pattern = r'type\s+(\w+)\s*='
                for match in re.finditer(type_pattern, content):
                    name = match.group(1)
                    line_no = content[:match.start()].count('\n') + 1
                    
                    types.append({
                        'name': name,
                        'type': 'type',
                        'file': file_path,
                        'line': line_no,
                        'bases': [],
                        'doc': '',  # Extract JSDoc if needed
                    })
            
            return functions, types
        
        except Exception as e:
            print(f"Error analyzing JavaScript/TypeScript file {file_path}: {e}", file=sys.stderr)
            return [], []

def get_analyzer_for_language(language):
    """Get the appropriate analyzer for a language."""
    analyzers = {
        'python': PythonAnalyzer,
        'javascript': JavaScriptAnalyzer,
        'typescript': JavaScriptAnalyzer,
    }
    return analyzers.get(language)

def scan_directory(directory, exclude_dirs=None):
    """
    Scan a directory for code files and analyze them.
    
    Args:
        directory (str or Path): The directory to scan
        exclude_dirs (list): List of directory patterns to exclude
        
    Returns:
        tuple: (functions, types) where each is a list of dictionaries
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', 'venv', '__pycache__', '.ipynb_checkpoints']
    
    all_functions = []
    all_types = []
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not any(ex in f"{root}/{d}" for ex in exclude_dirs)]
        
        for file in files:
            file_path = os.path.join(root, file)
            language = determine_language(file_path)
            
            if language:
                analyzer = get_analyzer_for_language(language)
                if analyzer:
                    functions, types = analyzer.analyze_file(file_path)
                    all_functions.extend(functions)
                    all_types.extend(types)
    
    return all_functions, all_types

def generate_functions_markdown(functions):
    """
    Generate Markdown documentation for functions.
    
    Args:
        functions (list): List of function dictionaries
        
    Returns:
        str: Markdown content
    """
    if not functions:
        return "No functions found."
    
    # Group functions by file
    functions_by_file = defaultdict(list)
    for func in functions:
        functions_by_file[func['file']].append(func)
    
    # Sort files by name
    sorted_files = sorted(functions_by_file.keys())
    
    markdown = [
        "# Project Functions\n",
        f"*Generated: {get_timestamp()}*\n",
        "This document maps all functions and methods in the project.\n\n",
        "## Table of Contents\n",
    ]
    
    # Generate TOC
    for file_path in sorted_files:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        file_id = rel_path.replace('/', '_').replace('.', '_').replace('-', '_')
        markdown.append(f"- [{rel_path}](#{file_id})\n")
    
    # Generate function documentation by file
    for file_path in sorted_files:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        file_id = rel_path.replace('/', '_').replace('.', '_').replace('-', '_')
        
        markdown.append(f"\n## {rel_path} <a id='{file_id}'></a>\n\n")
        
        # Sort functions by line number
        file_functions = sorted(functions_by_file[file_path], key=lambda f: f['line'])
        
        for func in file_functions:
            args_str = ', '.join(func['args'])
            
            # Format the function signature based on type
            if func['type'] == 'method':
                signature = f"**{func['name']}({args_str})**"
            else:
                signature = f"**{func['name']}({args_str})**"
            
            markdown.append(f"### {signature}\n\n")
            markdown.append(f"- **Type**: {func['type']}\n")
            markdown.append(f"- **Line**: {func['line']}\n")
            
            if func['doc']:
                markdown.append(f"\n{func['doc']}\n\n")
            else:
                markdown.append("\n*No documentation available.*\n\n")
    
    return ''.join(markdown)

def generate_types_markdown(types):
    """
    Generate Markdown documentation for types.
    
    Args:
        types (list): List of type dictionaries
        
    Returns:
        str: Markdown content
    """
    if not types:
        return "No types found."
    
    # Group types by file
    types_by_file = defaultdict(list)
    for typ in types:
        types_by_file[typ['file']].append(typ)
    
    # Sort files by name
    sorted_files = sorted(types_by_file.keys())
    
    markdown = [
        "# Project Types\n",
        f"*Generated: {get_timestamp()}*\n",
        "This document maps all classes, interfaces, and types in the project.\n\n",
        "## Table of Contents\n",
    ]
    
    # Generate TOC
    for file_path in sorted_files:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        file_id = rel_path.replace('/', '_').replace('.', '_').replace('-', '_')
        markdown.append(f"- [{rel_path}](#{file_id})\n")
    
    # Generate type documentation by file
    for file_path in sorted_files:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        file_id = rel_path.replace('/', '_').replace('.', '_').replace('-', '_')
        
        markdown.append(f"\n## {rel_path} <a id='{file_id}'></a>\n\n")
        
        # Sort types by line number
        file_types = sorted(types_by_file[file_path], key=lambda t: t['line'])
        
        for typ in file_types:
            bases_str = f" extends {', '.join(typ['bases'])}" if typ['bases'] else ""
            
            markdown.append(f"### {typ['name']}{bases_str}\n\n")
            markdown.append(f"- **Type**: {typ['type']}\n")
            markdown.append(f"- **Line**: {typ['line']}\n")
            
            if typ['doc']:
                markdown.append(f"\n{typ['doc']}\n\n")
            else:
                markdown.append("\n*No documentation available.*\n\n")
    
    return ''.join(markdown)

def write_markdown_file(content, file_path):
    """Write content to a Markdown file."""
    ensure_directory_exists(os.path.dirname(file_path))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Generated {file_path}")

def main():
    """Main function to parse arguments and execute the script."""
    parser = argparse.ArgumentParser(
        description='Generate documentation of functions and types in the project'
    )
    parser.add_argument(
        '--target-dir',
        type=str,
        default=str(PROJECT_ROOT),
        help='Target directory to scan (default: project root)'
    )
    args = parser.parse_args()
    
    print(f"Scanning directory: {args.target_dir}")
    functions, types = scan_directory(args.target_dir)
    
    print(f"Found {len(functions)} functions and {len(types)} types")
    
    functions_markdown = generate_functions_markdown(functions)
    types_markdown = generate_types_markdown(types)
    
    write_markdown_file(functions_markdown, FUNCTIONS_FILE)
    write_markdown_file(types_markdown, TYPES_FILE)
    
    print("Documentation generation complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 