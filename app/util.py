from pathlib import Path


def save_image(image: bytes, path: Path) -> None:
    """
    Save an image at specific path based on input image bytes.
    Args:
        image (bytes): Image represented as bytes.
        path (Path): Location to save image.
    """
    with open(path, "wb") as file:
        file.write(image)


def load_image(path: Path) -> bytes:
    """
    Load an image as bytes from specified path.
    Args:
        path (Path): Path to image.
    Returns:
        content (bytes): Image as bytes.
    """
    with open(path, "rb") as file:
        content = file.read()
    return content


def delete_file(path: Path) -> None:
    """
    Removes a file at specified path if file exists.
    Args:
        path (Path): Path to location of file.
    """
    if path.exists():
        Path.unlink(path)
