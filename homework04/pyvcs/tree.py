import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # PUT YOUR CODE HERE
    tree = b""
    for f in index:
        files = oct(f.mode)[2:].encode()
        if "/" in f.name:
            num = f.name.find("/")
            dirname = f.name[:num]
            new_f = files + b" " + f.name[num + 1 :].encode() + b"\0" + f.sha1
            hashh = bytes.fromhex(hash_object(new_f, fmt="tree", write=True))
            tree += b"40000 " + dirname.encode() + b"\0" + hashh
        else:
            tree += files + b" " + f.name.encode() + b"\0" + f.sha1
    return hash_object(data=tree, fmt="tree", write=True)
    ...


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    commit_time = int(time.mktime(time.localtime()))
    commit_timezone = time.strftime("%z", time.localtime())
    parent_str = f"\nparent {parent}" if parent else ""
    content =  f"tree {tree}" + parent_str + f"\nauthor {author} {commit_time} {commit_timezone}\ncommitter {author} {commit_time} {commit_timezone}\n\n{message}\n"
    commit_sha = hash_object(content.encode(), "commit", write=True)
    return commit_sha
