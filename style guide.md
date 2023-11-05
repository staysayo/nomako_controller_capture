```markdown
# Python Code Commenting and Documentation Style Guide

## 1. File Header Comments
### Purpose
At the top of each Python file, include a comment block with the file's name, author, creation date, and a brief description of the file's purpose.

### Format
```python
"""
Filename: example.py
Author: [Your Name]
Creation Date: [Date]
Description: Implements a solution for [Problem/Task].
"""
```

## 2. Class and Function Documentation
### Purpose
Each class and function must have a docstring explaining its purpose, parameters, return values, and usage.

### Format
```python
class MyClass:
    """
    Brief description of the class.

    Attributes:
        attr1 (type): Description of attr1.
        attr2 (type): Description of attr2.

    Methods:
        method1: Description of method1.
    """
    
def my_function(arg1, arg2):
    """
    Brief description of the function.

    Parameters:
        arg1 (type): Description of arg1.
        arg2 (type): Description of arg2.

    Returns:
        type: Description of the return value.
    """
```

## 3. Inline Comments
### Purpose
Use inline comments sparingly to explain complex code segments.

### Format
Place the inline comment at the end of the line of code, separated by two spaces and a `#`.

## 4. Block Comments
### Purpose
Use block comments to describe more complex code logic that spans multiple lines.

### Format
```python
# This is a block comment that can be used to describe
# the following block of code. Each line starts with a #.
```

## 5. TODO Comments
### Purpose
Mark areas of code that require future attention with a `TODO` comment.

### Format
```python
# TODO: Implement feature XYZ or fix bug related to ABC
```

## 6. Markdown Structure in Comments
### Purpose
Structure any block comments or docstrings that will be extracted as markdown files with proper markdown syntax.

### Format
- Use markdown headers (`#`, `##`, `###`, etc.) for titles and subtitles.
- Use unordered (`-`) or ordered (`1.`) lists for bullet points or numbered lists.
- Use backticks (`` ` ``) for inline code and triple backticks for code blocks.
- Use `[Text](URL)` for hyperlinks.

## 7. Extraction Markers
### Purpose
Define unique markers or tags to denote comments that should be extracted for documentation.

### Format
```python
# MARKDOWN_START
# This is a markdown-compatible comment block that should be extracted.
# MARKDOWN_END
```

## Categories for Documentation
- **Introduction**: A brief introduction to the software.
- **Installation**: Steps to install the software.
- **Usage**: How to use the software, with examples.
- **Configuration**: Configuration options available to the user.
- **Contribution**: Guidelines for contributing to the software project.
- **License**: License information for the software.
- **Credits**: Acknowledgements and credits to contributors.
```