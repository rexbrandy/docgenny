"""
Command-line interface for docgenny
"""

import argparse
import sys
from pathlib import Path
from .generator import DocumentationGenerator


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="docgenny",
        description="Generate comprehensive technical documentation from Python codebases",
        epilog="Example: docgenny /path/to/project -o DOCS.md"
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
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    parser.add_argument(
        "--include",
        help="Additional file patterns to include (comma-separated)"
    )
    
    parser.add_argument(
        "--exclude",
        help="Additional patterns to exclude (comma-separated)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_dir():
        print(f"Error: Path '{args.path}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Create generator
        generator = DocumentationGenerator(args.path, args.output)
        
        # Apply custom patterns if provided
        if args.include:
            patterns = [p.strip() for p in args.include.split(",")]
            generator.important_patterns.update(patterns)
        
        if args.exclude:
            patterns = [p.strip() for p in args.exclude.split(",")]
            generator.ignore_patterns.update(patterns)
        
        # Generate documentation
        generator.generate()
        
        if args.verbose:
            print(f"\n✓ Successfully generated documentation")
            print(f"  Models: {len(generator.models)}")
            print(f"  Functions: {len(generator.functions)}")
            print(f"  Files: {len(generator.file_tree)}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()