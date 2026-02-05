"""
docgenny - Automatically generate comprehensive technical documentation from Python codebases
"""

from .generator import DocumentationGenerator, Model, Function, ModelField

__version__ = "0.1.0"
__author__ = "Bailey Armitage"
__email__ = "bailey.sdev@gmail.com"

__all__ = [
    "DocumentationGenerator",
    "Model",
    "Function",
    "ModelField",
]