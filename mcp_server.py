import asyncio
import os
from pathlib import Path
from typing import List, Union

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from deepsearcher import configuration
from deepsearcher.configuration import Configuration, init_config
from deepsearcher.offline_loading import load_from_local_files, load_from_website
from deepsearcher.online_query import query

mcp = FastMCP("deepsearcher")

config = Configuration()
init_config(config)

MOUNT_ROOT = Path(os.environ.get("DEEPSEARCHER_MOUNT_DIR", "/app/mounted_data")).resolve()
MOUNT_ROOT.mkdir(parents=True, exist_ok=True)


def _normalize_paths(paths: Union[str, List[str]]) -> List[str]:
    if isinstance(paths, str):
        paths = [paths]
    normalized: List[str] = []
    for raw_path in paths:
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = (MOUNT_ROOT / raw_path).resolve()
        normalized.append(str(candidate))
    return normalized


@mcp.tool()
async def query_tool(original_query: str, max_iter: int = 3) -> TextContent:
    result_text, _, consume_token = await asyncio.to_thread(query, original_query, max_iter)
    message = f"{result_text}\n\nTokens used: {consume_token}"
    return TextContent(type="text", text=message)


@mcp.tool()
async def load_from_local_files_tool(
    paths_or_directory: Union[str, List[str]],
    collection_name: str | None = None,
    collection_description: str | None = None,
    batch_size: int = 256,
) -> TextContent:
    resolved_paths = _normalize_paths(paths_or_directory)
    await asyncio.to_thread(
        load_from_local_files,
        resolved_paths,
        collection_name,
        collection_description,
        False,
        1500,
        100,
        batch_size,
    )
    collection = collection_name or configuration.vector_db.default_collection
    message = f"Loaded {len(resolved_paths)} path(s) into collection '{collection}'."
    return TextContent(type="text", text=message)


@mcp.tool()
async def load_from_website_tool(
    urls: Union[str, List[str]],
    collection_name: str | None = None,
    collection_description: str | None = None,
    batch_size: int = 256,
) -> TextContent:
    if isinstance(urls, str):
        urls = [urls]
    await asyncio.to_thread(
        load_from_website,
        urls,
        collection_name,
        collection_description,
        False,
        1500,
        100,
        batch_size,
    )
    collection = collection_name or configuration.vector_db.default_collection
    message = f"Loaded {len(urls)} URL(s) into collection '{collection}'."
    return TextContent(type="text", text=message)


if __name__ == "__main__":
    mcp.run()
