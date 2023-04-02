import re
from typing import List
from datetime import datetime
from .search_abc import SearchResult

def remove_commands(query: str) -> str:
    query = re.sub(r'\/page:(\S+)\s+', '', query)
    query = re.sub(r'\/site:(\S+)\s+', '', query)
    return query


def compile_prompt(results: List[SearchResult], query: str, default_prompt: str) -> str:
    formatted_results = format_web_results(results)
    current_date = datetime.now().strftime("%m/%d/%Y")
    print(default_prompt)
    return replace_variables(
        default_prompt,
        {
            '[web_results]': formatted_results,
            '[query]': remove_commands(query),
            '[current_date]': current_date,
        },
    )


def format_web_results(results: List[SearchResult]) -> str:
    return (
        "".join(
            f'[{counter}] \"{result.body}\"\nURL: {result.url}\n\n'
            for counter, result in enumerate(results, start=1)
        )
        if results
        else "No results found.\n"
    )


def replace_variables(prompt: str, variables: dict) -> str:
    new_prompt = prompt
    for key, value in variables.items():
        try:
            new_prompt = new_prompt.replace(key, value)
        except Exception as error:
            print("Search prompt error: ", error)
    return new_prompt
