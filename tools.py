import markdown
import os
from typing import Union, List, Dict, Optional

def markdown_to_html(markdown_input: Union[str, List[str]]) -> Union[str, Dict[str, Optional[str]], None]:
    """
    Converts Markdown content to HTML.

    Args:
        markdown_input: A string containing Markdown content, 
                       or a list of file paths to Markdown files.

    Returns:
        If markdown_input is a string:
            A string containing the HTML output.
        If markdown_input is a list:
            A dictionary where keys are the input file paths and values are the corresponding HTML output.
        Returns None if there's an error (e.g., file not found).
    """

    if isinstance(markdown_input, str):  # Single Markdown string
        try:
            html = markdown.markdown(markdown_input)
            return html
        except Exception as e:
            print(f"Error converting Markdown string: {e}")
            return None

    elif isinstance(markdown_input, list):  # List of file paths
        html_outputs = {}
        for file_path in markdown_input:
            try:
                if not os.path.exists(file_path):
                    print(f"Error: File not found: {file_path}")
                    html_outputs[file_path] = None  # Or handle differently
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:  # Important to handle encoding
                    markdown_content = f.read()
                html = markdown.markdown(markdown_content)
                html_outputs[file_path] = html
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
                html_outputs[file_path] = None
        return html_outputs
    else:
        print("Invalid input. Please provide a Markdown string or a list of file paths.")
        return None

