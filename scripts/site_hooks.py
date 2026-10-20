"""Expose repository sources as site downloads without maintaining duplicate files."""

from pathlib import Path
import runpy

from mkdocs.structure.files import File, InclusionLevel


ROOT = Path(__file__).resolve().parents[1]


def on_files(files, config):
    files.append(File.generated(
        config, ".nojekyll", content="\n", inclusion=InclusionLevel.INCLUDED,
    ))
    for directory in ("examples", "scripts"):
        for source in sorted((ROOT / directory).glob("*.py")):
            files.append(File.generated(
                config, source.relative_to(ROOT).as_posix(),
                abs_src_path=str(source),
            ))
    render_book = runpy.run_path(str(ROOT / "scripts" / "build_book.py"))["render_book"]
    # .txt deliberately keeps the Markdown as a downloadable source document.
    files.append(File.generated(
        config, "downloads/Python完整教程.txt", content=render_book(),
    ))
    return files
