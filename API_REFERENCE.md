# Technical Documentation

*Auto-generated from: *

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Models & Schemas](#models--schemas)
3. [Functions & Utilities](#functions--utilities)

---

## Project Structure

```
/
├── docgenny/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── generator.py
├── examples/
├── tests/
│   ├── __init__.py
│   ├── test_generator.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── TECHNICAL_DOCS.md
├── pyproject.toml
├── setup.py
```

---

## Models & Schemas

### docgenny/generator.py

#### `DocumentationGenerator`

**Methods:**
- `__init__()`
- `should_ignore()`
- `is_important_file()`
- `build_file_tree()`
- `parse_python_file()`
- `extract_class()`
- `extract_function()`
- `scan_codebase()`
- `generate_markdown()`
- `generate()`

---

#### `Function`

**Fields:**
| Field | Type | Default |
|-------|------|---------|
| `name` | `str` | `-` |
| `file` | `str` | `-` |
| `params` | `List[str]` | `-` |
| `returns` | `str` | `-` |
| `docstring` | `str` | `-` |

---

#### `Model`

**Fields:**
| Field | Type | Default |
|-------|------|---------|
| `name` | `str` | `-` |
| `file` | `str` | `-` |
| `fields` | `List[ModelField]` | `-` |
| `methods` | `List[str]` | `-` |
| `base_classes` | `List[str]` | `-` |

---

#### `ModelField`

**Fields:**
| Field | Type | Default |
|-------|------|---------|
| `name` | `str` | `-` |
| `type` | `str` | `-` |
| `default` | `str` | `None` |

---

## Functions & Utilities

### docgenny/cli.py

#### `main()`
*Returns: `None`*

Main CLI entry point

---
