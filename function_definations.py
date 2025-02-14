from pydantic import BaseModel, Field
from typing import Optional, List
from openai import pydantic_function_tool


class InstallAndRunDatagen(BaseModel):
    """Model for installing dependencies (if required) and running a Python script."""
    script_url: str = Field(...,
        description="URL to the Python script to be downloaded and executed."
    )

    email : str = Field(...,
        description="The email that is passed as the argument"
    )

class FormatMarkdownUsingPrettier(BaseModel):
    """Model for formatting a Markdown file using Prettier."""
    file_path: str = Field(..., description="Path to the Markdown file to be formatted.")
    prettier_version: str = Field(..., description="Version of Prettier to use for formatting. Return Example: 3.4.2 ")


class CountTheNumberofDaysAndSave(BaseModel):
    day: str = Field(..., description="Name of the day")
    input_file: str = Field(..., description="Path to the file containing a list of dates.")
    output_file: str = Field(..., description="Path to the file to write the count of the days.")

#maybe changed to sort files
class SortContacts(BaseModel):
    input_file: str = Field(..., description="Path to the JSON file containing contacts.")
    output_file: str = Field(..., description="Path to the JSON file to write the sorted contacts.")
    sort_keys: List[str] = Field(..., description="List of keys to sort by, in order of priority.")


#maybe changed to handle other extension as well
class WriteRecentLogs(BaseModel):
    directory: str = Field(..., description="Path to the directory containing log files.")
    output_file: str = Field(..., description="Path to the file to write the recent logs.")
    num_files: int = Field(..., description="Number of recent files to process.")
    num_lines: int = Field(..., description="Number of lines to extract from each file.")
    extension: str = Field(..., description="File extension to filter by, e.g., '.log'.")

#List
class GenerateMarkdownIndex(BaseModel):
    directory: str = Field(..., description="Path to the directory containing Markdown files.")
    output_file: str = Field(..., description="Path to the JSON file to write the index.")
    tags: List[str] = Field(..., description="List of Markdown tags to extract, e.g., ['#', '##'].")

#maybe changed to pass general text to llm
class ExtractUsingLLM(BaseModel):
    input_file: str = Field(..., description="Path to the file containing the text to be processed.")
    output_file: str = Field(..., description="Path to the file to write the extracted information.")
    instructions: str = Field(..., 
                              description="""Instructions for the LLM to extract the desired information.
                              Follow the Instruction exactlty. Example: If it says to JUST extract the email: Remember to prompt the tool to just output the email and nothing else.
                              """)


class ExtractTextFromImageUsingLLM(BaseModel):
    """
    Model for extracting specific information from an image using an LLM.
    """
    input_image: str = Field(..., description="Path to the image file.")
    query: str = Field(..., description="""Query specifying what to extract from the image . Specify with or without spaces.).
                       Remember to focus on important details.
                       """)
    output_file: Optional[str] = Field(..., description="Path to the file to write the extracted text. If None, no file will be written.")


class FindMostSimilarTextsUsingEmbeddings(BaseModel):
    """
    Pydantic model for the `find_most_similar_texts` function.
    """
    input_file: str = Field(..., description="Path to the file containing the text items, one per line.")
    max_items: Optional[int] = Field(..., description="Maximum number of items to process from the file.")
    output_file: Optional[str] = Field(..., description="Path to the file to write the most similar pair. If None, output is not written to a file.")

class CalculateTotalTicketSales(BaseModel):
    database_file: str = Field(..., description="Path to the SQLite database file.")
    output_file: str = Field(..., description="Path to the file to write the total sales.")
    ticket_type: str = Field(..., description="The ticket type to calculate total sales for.")


# class FetchDataFromAPI(BaseModel):
#     """Model for fetching data from an API and saving it to a file."""
#     api_url: str = Field(..., description="The URL of the API to fetch data from.")
#     output_file: str = Field(..., description="Path to the file to save the fetched data.")


# class CloneGitRepoAndCommit(BaseModel):
#     """Model for cloning a Git repository and making a commit."""
#     repo_url: str = Field(..., description="The URL of the Git repository to clone.")
#     commit_message: str = Field(..., description="The commit message for the changes.")
#     file_path: Optional[str] = Field(None, description="Path to the file to modify before committing.")
#     file_content: Optional[str] = Field(None, description="Content to write to the file before committing.")


class RunSQLQuery(BaseModel):
    database_file: str = Field(..., description="Path to the SQLite or DuckDB database file.")
    query: str = Field(..., description="The SQL query to be executed.")
    output_file: Optional[str] = Field(..., description="Path to the file to save the query output. If None, no output will be saved.")
    database_type: str = Field(..., description="The type of database. Either 'sqlite' or 'duckdb'.")
    output_format: Optional[str] = Field(..., description="The format of the output file. Either 'csv' or 'txt'. Defaults to 'csv'.")


# class ExtractDataFromWebsite(BaseModel):
#     """Model for extracting data from (i.e. scraping) a website."""
#     website_url: str = Field(..., description="The URL of the website to scrape.")
#     output_file: str = Field(..., description="Path to the file to save the scraped data.")
#     css_selector: Optional[str] = Field(None, description="CSS selector to target specific elements (optional).")


# class CompressOrResizeImage(BaseModel):
#     """Model for compressing or resizing an image."""
#     input_image: str = Field(..., description="Path to the input image file.")
#     output_image: str = Field(..., description="Path to the output image file.")
#     width: Optional[int] = Field(None, description="Target width for resizing (optional).")
#     height: Optional[int] = Field(None, description="Target height for resizing (optional).")
#     quality: Optional[int] = Field(None, description="Quality level for compression (1-100, optional).")


# class TranscribeAudio(BaseModel):
#     """Model for transcribing audio from an MP3 file."""
#     audio_file: str = Field(..., description="Path to the MP3 audio file to transcribe.")
#     output_file: str = Field(..., description="Path to the file to save the transcription text.")


# class ConvertMarkdownToHTML(BaseModel):
#     """Model for converting Markdown to HTML."""
#     markdown_file: str = Field(..., description="Path to the Markdown file to convert.")
#     output_file: str = Field(..., description="Path to the file to save the converted HTML.")


# class WriteAPIEndpointForCSVFilter(BaseModel):
#     """Model for writing an API endpoint that filters a CSV file and returns JSON data."""
#     csv_file: str = Field(..., description="Path to the CSV file to filter.")
#     filter_column: str = Field(..., description="The column name to filter data on.")
#     filter_value: str = Field(..., description="The value to filter the column by.")
#     output_file: Optional[str] = Field(None, description="Path to save the filtered JSON data (optional).")

class Execute_shell_command(BaseModel):
    command: str = Field(..., description="Shell commnands to execute in the terminal")


tools = [
    # A
    pydantic_function_tool(InstallAndRunDatagen),
    pydantic_function_tool(FormatMarkdownUsingPrettier),
    pydantic_function_tool(CountTheNumberofDaysAndSave),
    pydantic_function_tool(SortContacts),
    pydantic_function_tool(WriteRecentLogs),
    pydantic_function_tool(GenerateMarkdownIndex),
    pydantic_function_tool(ExtractUsingLLM),
    pydantic_function_tool(ExtractTextFromImageUsingLLM),
    pydantic_function_tool(FindMostSimilarTextsUsingEmbeddings),
    pydantic_function_tool(CalculateTotalTicketSales),    
    # B
    # pydantic_function_tool(FetchDataFromAPI),
    # pydantic_function_tool(CloneGitRepoAndCommit),
    pydantic_function_tool(RunSQLQuery),
    # pydantic_function_tool(ExtractDataFromWebsite),
    # pydantic_function_tool(CompressOrResizeImage),
    # pydantic_function_tool(TranscribeAudio),
    # pydantic_function_tool(ConvertMarkdownToHTML),
    # pydantic_function_tool(WriteAPIEndpointForCSVFilter),
    # Very important and dangerous
    pydantic_function_tool(Execute_shell_command)
]