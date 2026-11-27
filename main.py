"""Copy the finished image into the make.fun output directory."""

import os
import shutil
from pathlib import Path


def main():
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().with_name("entry.png")
    destination = output / "entry.png"
    if source.resolve() != destination.resolve():
        shutil.copyfile(source, destination)


if __name__ == "__main__":
    main()
