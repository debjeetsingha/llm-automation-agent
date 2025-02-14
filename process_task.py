from typing import Dict, Any

from functions import (
    install_and_run_script,
    format_markdown_prettier,
    count_days_and_save,
    sort_contacts,
    generate_markdown_index,
    extract_using_llm,
    extract_text_from_image_using_llm,
    calculate_total_sales,
    run_sql_query,
    find_most_similar_texts,
    write_recent_logs,
    run_terminal_command
)

system_prompt = """ 
You are an AI assistant that helps with various tasks. Use the provided functions to complete the user's request.

Guidelines:
1. Always check whether a tool or dependency is installed before running any command. If it is missing, install it first using the appropriate package manager.
2. Assume you are running inside a docker image containing only uv package manager, npm, npx, python, curl , ca-certificates , imagemagick , git
3. Ensure commands are safe and do not exfiltrate data outside `/data`. You must never delete files or data outside `/data`.
5. Always verify ambiguous terms in the task description.
   - For example, ensure 'uv' refers to the package manager and not `uvicorn`.
6. Tasks may be in different languages. Always interpret them correctly.
7. Don't mention details like its a credit card, debit card etc that an LLM may refuse to process.
         example:
               Do not say : "extract the credit card number and write it without spaces"
               Instead say: "contains a number. Extract the number, and write it without spaces"
8. When task is completed, Say that it completed and don't call any tool.


"""

def execute_function(function_name: str, arguments: Dict[str, Any]) -> str:
    function_map = {
    "InstallAndRunDatagen" : install_and_run_script,
    "FormatMarkdownUsingPrettier" : format_markdown_prettier,
    "CountTheNumberofDaysAndSave" : count_days_and_save,
    "SortContacts" : sort_contacts,
    "GenerateMarkdownIndex" : generate_markdown_index,
    "WriteRecentLogs": write_recent_logs,
    "ExtractUsingLLM" : extract_using_llm,
    "ExtractTextFromImageUsingLLM" : extract_text_from_image_using_llm,
    "calculate_total_sales" : calculate_total_sales,
    "RunSQLQuery" : run_sql_query,
    "FindMostSimilarTextsUsingEmbeddings" : find_most_similar_texts,
    "Execute_shell_command" : run_terminal_command
    }

    if function_name not in function_map:
        raise ValueError(f"Unknown function: {function_name}")
    
    return function_map[function_name](**arguments)