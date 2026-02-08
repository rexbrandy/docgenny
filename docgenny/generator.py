#!/usr/bin/env python3
"""
Technical Documentation Generator
Generates comprehensive documentation from Python and JavaScript/TypeScript codebases
"""

import os
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass, asdict


@dataclass
class ModelField:
    name: str
    type: str
    default: str = None


@dataclass
class Model:
    name: str
    file: str
    fields: List[ModelField]
    methods: List[str]
    base_classes: List[str]


@dataclass
class Function:
    name: str
    file: str
    params: List[str]
    returns: str
    docstring: str


class DocumentationGenerator:
    def __init__(self, root_path: str, output_file: str = "TECHNICAL_DOCS.md"):
        self.root_path = Path(root_path)
        self.output_file = output_file
        self.models = []
        self.functions = []
        self.file_tree = []
        
        # Files/directories to ignore
        self.ignore_patterns = {
            '__pycache__', '.git', '.pytest_cache', 'node_modules',
            '.venv', 'venv', 'env', '.env', 'dist', 'build',
            '.DS_Store', '*.pyc', '*.pyo', '*.egg-info',
            '.svelte-kit', 'output', 'generated', '__package__'
        }
        
        # Important file patterns to include
        self.important_patterns = {
            '*.py', '*.js', '*.ts', '*.svelte', '*.md', 
            'requirements*.txt', '*.yml', '*.yaml',
            'Dockerfile', '.env.example', 'setup.py', 
            'pyproject.toml', 'package.json'
        }

    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        parts = path.parts
        for pattern in self.ignore_patterns:
            if any(pattern.strip('*') in str(part) for part in parts):
                return True
        return False

    def is_important_file(self, path: Path) -> bool:
        """Check if file matches important patterns"""
        for pattern in self.important_patterns:
            if pattern.startswith('*'):
                if path.suffix == pattern[1:]:
                    return True
            elif path.name == pattern or path.match(pattern):
                return True
        return False

    def build_file_tree(self) -> List[str]:
        """Build a tree structure of important files"""
        tree_lines = []
        
        def add_to_tree(path: Path, prefix: str = ""):
            if self.should_ignore(path):
                return
                
            if path.is_file():
                if self.is_important_file(path):
                    tree_lines.append(f"{prefix}├── {path.name}")
            elif path.is_dir():
                rel_path = path.relative_to(self.root_path)
                if rel_path != Path('.'):
                    tree_lines.append(f"{prefix}├── {path.name}/")
                
                try:
                    items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                    for item in items:
                        add_to_tree(item, prefix + "│   ")
                except PermissionError:
                    pass
        
        tree_lines.append(f"{self.root_path.name}/")
        for item in sorted(self.root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name)):
            add_to_tree(item, "")
        
        return tree_lines

    def parse_python_file(self, file_path: Path):
        """Parse a Python file to extract models and functions"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            rel_path = str(file_path.relative_to(self.root_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.extract_class(node, rel_path)
                elif isinstance(node, ast.FunctionDef):
                    if not any(isinstance(parent, ast.ClassDef) 
                             for parent in ast.walk(tree)):
                        self.extract_function(node, rel_path)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    def parse_javascript_file(self, file_path: Path):
        """Parse JavaScript/TypeScript files to extract functions and classes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rel_path = str(file_path.relative_to(self.root_path))
            
            # Extract class definitions
            class_pattern = r'(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                base_class = match.group(2) if match.group(2) else None
                
                # Extract methods from this class
                methods = self.extract_js_methods(content, match.start())
                
                self.models.append(Model(
                    name=class_name,
                    file=rel_path,
                    fields=[],  # Could be enhanced to extract properties
                    methods=methods,
                    base_classes=[base_class] if base_class else []
                ))
            
            # Extract function definitions
            func_pattern = r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1)
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                
                self.functions.append(Function(
                    name=func_name,
                    file=rel_path,
                    params=params,
                    returns="unknown",
                    docstring=""
                ))
            
            # Extract arrow functions assigned to const/let
            arrow_pattern = r'(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>'
            for match in re.finditer(arrow_pattern, content):
                func_name = match.group(1)
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                
                self.functions.append(Function(
                    name=func_name,
                    file=rel_path,
                    params=params,
                    returns="unknown",
                    docstring=""
                ))
                
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    def extract_js_methods(self, content: str, class_start: int) -> List[str]:
        """Extract method names from a JavaScript class"""
        methods = []
        # Find the class block
        brace_count = 0
        start_found = False
        class_content = ""
        
        for i in range(class_start, len(content)):
            char = content[i]
            if char == '{':
                brace_count += 1
                start_found = True
            elif char == '}':
                brace_count -= 1
            
            if start_found:
                class_content += char
                
            if start_found and brace_count == 0:
                break
        
        # Extract method names
        method_pattern = r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{'
        for match in re.finditer(method_pattern, class_content):
            method_name = match.group(1)
            if method_name not in ['if', 'for', 'while', 'switch']:
                methods.append(method_name)
        
        return methods

    def parse_svelte_file(self, file_path: Path):
        """Parse Svelte files to extract script content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract script tag content
            script_pattern = r'<script[^>]*>(.*?)</script>'
            matches = re.findall(script_pattern, content, re.DOTALL)
            
            if matches:
                # Parse the script content as JavaScript
                rel_path = str(file_path.relative_to(self.root_path))
                
                for script_content in matches:
                    # Extract functions
                    func_pattern = r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'
                    for match in re.finditer(func_pattern, script_content):
                        func_name = match.group(1)
                        params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                        
                        self.functions.append(Function(
                            name=func_name,
                            file=rel_path,
                            params=params,
                            returns="unknown",
                            docstring=""
                        ))
                    
                    # Extract const/let functions
                    arrow_pattern = r'(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>'
                    for match in re.finditer(arrow_pattern, script_content):
                        func_name = match.group(1)
                        params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                        
                        self.functions.append(Function(
                            name=func_name,
                            file=rel_path,
                            params=params,
                            returns="unknown",
                            docstring=""
                        ))
                        
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    def extract_class(self, node: ast.ClassDef, file_path: str):
        """Extract class/model information from Python"""
        fields = []
        methods = []
        base_classes = [base.id if isinstance(base, ast.Name) else str(base) 
                       for base in node.bases]
        
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_type = ast.unparse(item.annotation) if item.annotation else "Any"
                default = ast.unparse(item.value) if item.value else None
                fields.append(ModelField(
                    name=item.target.id,
                    type=field_type,
                    default=default
                ))
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        default = ast.unparse(item.value)
                        fields.append(ModelField(
                            name=target.id,
                            type="Any",
                            default=default
                        ))
            elif isinstance(item, ast.FunctionDef):
                if not item.name.startswith('_') or item.name in ['__init__', '__str__']:
                    methods.append(item.name)
        
        self.models.append(Model(
            name=node.name,
            file=file_path,
            fields=fields,
            methods=methods,
            base_classes=base_classes
        ))

    def extract_function(self, node: ast.FunctionDef, file_path: str):
        """Extract function information from Python"""
        params = []
        for arg in node.args.args:
            param_str = arg.arg
            if arg.annotation:
                param_str += f": {ast.unparse(arg.annotation)}"
            params.append(param_str)
        
        returns = ast.unparse(node.returns) if node.returns else "None"
        docstring = ast.get_docstring(node) or ""
        
        self.functions.append(Function(
            name=node.name,
            file=file_path,
            params=params,
            returns=returns,
            docstring=docstring.split('\n')[0] if docstring else ""
        ))

    def scan_codebase(self):
        """Scan the entire codebase"""
        print("Scanning codebase...")
        
        # Build file tree
        self.file_tree = self.build_file_tree()
        
        # Parse files based on extension
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file() and not self.should_ignore(file_path):
                if file_path.suffix == '.py':
                    self.parse_python_file(file_path)
                elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                    self.parse_javascript_file(file_path)
                elif file_path.suffix == '.svelte':
                    self.parse_svelte_file(file_path)
        
        print(f"Found {len(self.models)} models/classes")
        print(f"Found {len(self.functions)} functions")

    def generate_markdown(self) -> str:
        """Generate markdown documentation"""
        lines = []
        
        # Header
        lines.append("# Technical Documentation")
        lines.append(f"\n*Auto-generated from: {self.root_path.name}*\n")
        lines.append("---\n")
        
        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("1. [Project Structure](#project-structure)")
        lines.append("2. [Models & Schemas](#models--schemas)")
        lines.append("3. [Functions & Utilities](#functions--utilities)")
        lines.append("\n---\n")
        
        # File Tree
        lines.append("## Project Structure\n")
        lines.append("```")
        lines.extend(self.file_tree)
        lines.append("```\n")
        lines.append("---\n")
        
        # Models
        lines.append("## Models & Schemas\n")
        
        if not self.models:
            lines.append("*No models or classes found*\n")
        else:
            # Group models by file
            models_by_file = {}
            for model in sorted(self.models, key=lambda x: (x.file, x.name)):
                if model.file not in models_by_file:
                    models_by_file[model.file] = []
                models_by_file[model.file].append(model)
            
            for file_path, models in models_by_file.items():
                lines.append(f"### {file_path}\n")
                
                for model in models:
                    lines.append(f"#### `{model.name}`")
                    
                    if model.base_classes:
                        lines.append(f"*Inherits from: {', '.join(model.base_classes)}*\n")
                    else:
                        lines.append("")
                    
                    if model.fields:
                        lines.append("**Fields:**")
                        lines.append("| Field | Type | Default |")
                        lines.append("|-------|------|---------|")
                        for field in model.fields:
                            default = field.default if field.default else "-"
                            lines.append(f"| `{field.name}` | `{field.type}` | `{default}` |")
                        lines.append("")
                    
                    if model.methods:
                        lines.append("**Methods:**")
                        for method in model.methods:
                            lines.append(f"- `{method}()`")
                        lines.append("")
                    
                    lines.append("---\n")
        
        # Functions
        lines.append("## Functions & Utilities\n")
        
        if not self.functions:
            lines.append("*No functions found*\n")
        else:
            # Group functions by file
            functions_by_file = {}
            for func in sorted(self.functions, key=lambda x: (x.file, x.name)):
                if func.file not in functions_by_file:
                    functions_by_file[func.file] = []
                functions_by_file[func.file].append(func)
            
            for file_path, functions in functions_by_file.items():
                lines.append(f"### {file_path}\n")
                
                for func in functions:
                    params_str = ", ".join(func.params) if func.params else ""
                    lines.append(f"#### `{func.name}({params_str})`")
                    lines.append(f"*Returns: `{func.returns}`*\n")
                    
                    if func.docstring:
                        lines.append(f"{func.docstring}\n")
                    
                    lines.append("---\n")
        
        return "\n".join(lines)

    def generate(self):
        """Generate the documentation"""
        print(f"Generating documentation for: {self.root_path}")
        
        self.scan_codebase()
        markdown = self.generate_markdown()
        
        output_path = self.root_path / self.output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"\n✓ Documentation generated: {output_path}")
        print(f"  - {len(self.models)} models documented")
        print(f"  - {len(self.functions)} functions documented")
        print(f"  - {len(self.file_tree)} files in tree")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate technical documentation from Python codebase"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root path of the codebase (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output",
        default="TECHNICAL_DOCS.md",
        help="Output file name (default: TECHNICAL_DOCS.md)"
    )
    
    args = parser.parse_args()
    
    generator = DocumentationGenerator(args.path, args.output)
    generator.generate()


if __name__ == "__main__":
    main()