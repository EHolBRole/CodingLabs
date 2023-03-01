import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    # PUT YOUR CODE HERE
    store = f"{fmt} {len(data)}\0".encode() + data

    hash_sha1 = hashlib.sha1(store).hexdigest()

    if write:
        path = pathlib.Path(repo_find() / "objects" / hash_sha1[:2])

        if not path.exists():
            path.mkdir(parents=True)

        file = pathlib.Path(path / hash_sha1[2:])

        if not file.exists():
            file.write_bytes(zlib.compress(store))

    return hash_sha1


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")

    tree_path = pathlib.Path()

    objects = []

    if gitdir.exists():
        for d in pathlib.Path(gitdir / "objects").iterdir():
            if d.is_dir() and d.name == obj_name[:2]:
                for f in d.iterdir():
                    if f.name[: len(obj_name[2:])] == obj_name[2:]:
                        objects.append(str(d.name + f.name))
    else:
        raise Exception(f"Not a {gitdir} Repository")

    if len(objects) <= 0:
        raise Exception(f"Not a valid object name {obj_name}")

    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    if gitdir.exists():
        for d in pathlib.Path(gitdir / "objects").iterdir():
            if d.is_dir() and d.name == obj_name[:2]:
                for f in d.iterdir():
                    if f.name[: len(obj_name[2:])] == obj_name[2:]:
                        return str(d.name + f.name)
        raise Exception(f"Not a valid object name {obj_name}")
    else:
        raise Exception(f"Not a {gitdir} Repository")


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    object_path = pathlib.Path(gitdir / "objects" / sha[:2] / sha[2:])
    with open(object_path, "rb") as f:
        obj_data = zlib.decompress(f.read())

    ind = obj_data.find(b"\x00")
    header = obj_data[:ind]
    fmt = header[: header.find(b" ")]
    data = obj_data[(ind + 1):]

    return fmt.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    contents = data
    ans = []
    while contents != b"":
        filemode_bytes, contents_bytes = contents.split(b" ", maxsplit=1)
        filename_bytes, contents_bytes = contents_bytes.split(b"\x00", maxsplit=1)
        sha1, contents = contents_bytes[:20], contents_bytes[20:]
        filemode = filemode_bytes.decode()
        filename = filename_bytes.decode()
        sha1_str = sha1.hex()
        fmt, _ = read_object(sha1_str, repo_find())
        ans.append((filemode, fmt, sha1_str, filename))
    return ans


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    fmt, data = read_object(obj_name, repo_find())
    if fmt == "commit":
        print(commit_parse(data))
    elif fmt == "tree":
        result = ""
        for tree_item in read_tree(data):
            result += "{filemode:0>6} {obj_type} {sha1}\t{filename}\n".format(
                    filemode=tree_item[0],
                    obj_type=tree_item[1],
                    sha1=tree_item[2],
                    filename=tree_item[3],
                )
        print(result)
    elif fmt == "blob":
        print(data.decode())
    else:
        raise Exception(f"Not a valid object name {obj_name}")

    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    fmt, data = read_object(tree_sha, repo_find())
    if fmt != "tree":
        raise Exception(f"Not a tree {tree_sha}")

    tree_items = read_tree(data)
    ans = [(name, sha) for _, _, sha, name in map(lambda x: x, tree_items)]
    return ans
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    return raw.decode()
    ...
