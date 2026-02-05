# docgenny 📚

> Automatically generate comprehensive technical documentation from your Python codebase

[![PyPI version](https://badge.fury.io/py/docgenny.svg)](https://badge.fury.io/py/docgenny)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🌳 **Smart File Tree** - Generates a clean directory structure showing only important files
- 📦 **Model Extraction** - Automatically documents all classes, fields, and methods
- 🔧 **Function Documentation** - Captures function signatures, parameters, and return types
- 📝 **Markdown Output** - Creates beautifully formatted, easy-to-read documentation
- 🎯 **Claude AI Ready** - Perfect for adding to Claude Projects for AI-assisted development
- ⚡ **Fast & Lightweight** - Pure Python with minimal dependencies

## 🚀 Quick Start

### Installation

```bash
pip install docgenny
```

### Basic Usage

```bash
# Generate docs for current directory
docgenny

# Generate docs for specific project
docgenny /path/to/your/project

# Custom output file
docgenny -o API_DOCS.md

# Specify custom patterns
docgenny --include "*.js,*.ts" --exclude "test_*"
```

## 📖 Usage Examples

### Python API

```python
from docgenny import DocumentationGenerator

# Generate documentation
generator = DocumentationGenerator(
    root_path="./my_project",
    output_file="TECHNICAL_DOCS.md"
)
generator.generate()
```

### Command Line

```bash
# Basic usage
docgenny

# With all options
docgenny /path/to/project \
  --output DOCS.md \
  --include "*.py,*.md,*.yml" \
  --exclude "__pycache__,*.pyc"
```

## 📋 What Gets Documented

### Models & Classes
- Class names and inheritance hierarchy
- All fields with types and default values
- Public methods and special methods (`__init__`, `__str__`)

### Functions
- Function signatures with type hints
- Parameter names and types
- Return types
- Docstrings (first line)

### Project Structure
- Directory tree with important files only
- Automatic filtering of common build/cache directories
- Customizable include/exclude patterns

## 🎯 Perfect For

- 🤖 **AI-Assisted Development** - Add to Claude Projects for better context
- 👥 **Team Onboarding** - Quick reference for new developers
- 📚 **API Documentation** - Keep docs in sync with code
- 🔄 **CI/CD Pipelines** - Auto-generate docs on every commit

## 🛠️ Configuration

Create a `.docgenny.yml` file in your project root:

```yaml
output: TECHNICAL_DOCS.md
include_patterns:
  - "*.py"
  - "*.md"
  - "requirements*.txt"
exclude_patterns:
  - "__pycache__"
  - "*.pyc"
  - ".git"
  - "venv"
```

## 📊 Example Output

The generated documentation includes:

1. **Table of Contents** - Quick navigation
2. **Project Structure** - Visual file tree
3. **Models & Schemas** - Detailed class documentation
4. **Functions & Utilities** - Function reference

See [example output](examples/sample_output.md) for a full example.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/docgenny.git
cd docgenny

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

If you find this tool useful, please consider giving it a star on GitHub!

## 📮 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Issues: [GitHub Issues](https://github.com/yourusername/docgenny/issues)

## 🙏 Acknowledgments

Built with ❤️ for developers who value good documentation.

---

**Made with Python** | **Powered by AST parsing**