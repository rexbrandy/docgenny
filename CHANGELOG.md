# Changelog

All notable changes to docgenny will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-08

### Added
- **JavaScript/TypeScript support** - Parse `.js`, `.ts`, `.jsx`, and `.tsx` files
- **Svelte support** - Extract functions from `.svelte` component `<script>` tags
- Extract JavaScript class definitions with methods
- Extract JavaScript function declarations
- Extract arrow functions (`const func = () => {}`)
- Support for async functions in JavaScript/TypeScript
- Automatic detection and parsing of multiple programming languages

### Changed
- Enhanced file tree to include JavaScript, TypeScript, and Svelte files
- Improved ignore patterns to exclude `.svelte-kit`, build outputs, and generated files
- Updated important file patterns to include modern JavaScript ecosystem files

### Fixed
- File tree now properly traverses `lib/` and `routes/` directories in Svelte projects
- Better handling of permission errors when scanning directories

## [0.1.0] - 2026-02-05

### Added
- Initial release of docgenny
- Automatic documentation generation from Python codebases
- Smart file tree generation with automatic filtering
- Model and class extraction with fields and methods
- Function documentation with signatures and docstrings
- Clean Markdown output
- Claude AI ready documentation format
- CLI with verbose mode and custom patterns
- Zero external dependencies (uses only Python stdlib)

### Features
- Parse Python files using AST
- Extract classes, dataclasses, and their fields
- Document function signatures with type hints
- Generate organized Markdown with table of contents
- Customizable include/exclude patterns
- Works on Python 3.8+