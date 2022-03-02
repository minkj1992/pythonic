"""
refs:
    PEP604: type union
    PEP613: TypeAlias
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import shutil
from dataclasses import dataclass
from typing import Literal

HashKeys = Literal["source", "dest"]


@dataclass(frozen=True)
class HashedFile:
    name: str
    hashed_contents: str


def do_sync(actions):
    for action, *paths in actions:
        if action == "COPY":
            shutil.copyfile(*paths)
        if action == "MOVE":
            shutil.move(*paths)
        if action == "DELETE":
            os.remove(paths[0])


class SyncFile:
    """
    Synchronize file source and destination
    condition
      - file name is changed
      - file value is changed
    """

    BLOCKSIZE: int = 65536

    def __init__(self, source: str | pathlib.Path, dest: str | pathlib.Path):
        self._source = source
        self._dest = dest
        self._hashes = dict[HashKeys, HashedFile]

    def sync(self):
        self._read_paths_and_hashes()
        actions = self._determine_actions()
        do_sync(actions)

    def _hash_file(self):
        pass

    def _read_paths_and_hashes(self, hash_key, path):
        for folder, _, files in os.walk(path):
            for file_name in files:
                hashed_content = self._hash_file(pathlib.Path(folder) / file_name)
                self._hashes[hash_key] = file_name
        return hashes

    def _determine_actions(
        self, source_hashes, dest_hashes, source_folder, dest_folder
    ):
        pass


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source_folder) / filename
            destpath = Path(dest_folder) / filename
            yield "COPY", sourcepath, destpath

        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest_folder) / dest_hashes[sha]
            newdestpath = Path(dest_folder) / filename
            yield "MOVE", olddestpath, newdestpath

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield "DELETE", dest_folder / filename
