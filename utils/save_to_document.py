import re
import os
from datetime import datetime
from pathlib import Path


def _sanitize_filename(text: str, max_length: int = 50) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:max_length].rstrip("_")


def save_itinerary(
    content: str,
    query: str,
    output_dir: str = "outputs",
    fmt: str = "md",
) -> str:
    """
    Save a travel itinerary to a file.

    Args:
        content: The itinerary text (markdown or plain).
        query: The original user query — used to derive the filename.
        output_dir: Directory where files are saved (created if absent).
        fmt: File format — "md" or "txt".

    Returns:
        Absolute path of the saved file.
    """
    if fmt not in ("md", "txt"):
        raise ValueError(f"Unsupported format '{fmt}'. Use 'md' or 'txt'.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    slug = _sanitize_filename(query)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_{timestamp}.{fmt}"
    file_path = output_path / filename

    if fmt == "md":
        header = f"# Travel Itinerary\n\n**Query:** {query}  \n**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}\n\n---\n\n"
        file_path.write_text(header + content, encoding="utf-8")
    else:
        header = f"Travel Itinerary\nQuery: {query}\nGenerated: {datetime.now().strftime('%B %d, %Y at %H:%M')}\n{'=' * 60}\n\n"
        file_path.write_text(header + content, encoding="utf-8")

    return str(file_path.resolve())
