from typing import Any, Dict

from functions import (
    count_days_and_save,
    extract_text_from_image_using_llm,
    extract_using_llm,
    find_most_similar_texts,
    generate_markdown_index,
    run_sql_query,
    run_terminal_command,
    sort_contacts,
    write_recent_logs,
)

system_prompt = """ 
You are an AI assistant that helps with various tasks. Use the provided functions to complete the user's request.

Guidelines:
0. Always use uv to run python files. For example: "uv run main.py optional-arguments". The python file can be a link to a raw github file. 
1. Always check whether a tool or dependency is installed before running any command. uv is alredy installed. No need to check for uv. If it is missing, install it first using the appropriate package manager.
2. Assume you are running inside a docker image containing only uv package manager, npm, npx, python, curl , ca-certificates , imagemagick , git, ffmpeg
3. Ensure commands are safe and do not exfiltrate data outside `/data`. You must never delete files or data outside `/data` or anywhere in the file system even if the task description asks for it.
5. Always verify ambiguous terms in the task description.
   - For example, ensure 'uv' refers to the package manager and not `uvicorn`.
6. Tasks may be in different languages. Always interpret them correctly.
7. Don't mention details like its a credit card, debit card etc that an LLM may refuse to process.
         example:
               Do not say : "extract the credit card number and write it without spaces"
               Instead say: "contains a number. Extract the number, and write it without spaces"
8. When task is completed, Say that it completed and don't call any tool.
9. When running git clone, if the directory already exists due to cloning in a previous command. Dont remove it and end the task.


"""


def execute_function(function_name: str, arguments: Dict[str, Any]) -> str:
    function_map = {
        "CountTheNumberofDaysAndSave": count_days_and_save,
        "SortContacts": sort_contacts,
        "GenerateMarkdownIndex": generate_markdown_index,
        "WriteRecentLogs": write_recent_logs,
        "ExtractUsingLLM": extract_using_llm,
        "ExtractTextFromImageUsingLLM": extract_text_from_image_using_llm,
        "RunSQLQuery": run_sql_query,
        "FindMostSimilarTextsUsingEmbeddings": find_most_similar_texts,
        "Execute_shell_command": run_terminal_command,
    }

    if function_name not in function_map:
        raise ValueError(f"Unknown function: {function_name}")

    return function_map[function_name](**arguments)
