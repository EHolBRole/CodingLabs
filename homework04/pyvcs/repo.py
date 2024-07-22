import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir_path = pathlib.Path(workdir).absolute()
    repo_dir_name = os.environ.get("GIT_DIR", ".git")

    if repo_dir_name in workdir_path.parts[1:]:
        gitdir = workdir_path.parts[0] + "/".join(
            workdir_path.parts[1 : workdir_path.parts.index(repo_dir_name) + 1]
        )
        gitdir_path = pathlib.Path(gitdir)
    else:
        gitdir_path = workdir_path / repo_dir_name

    if os.path.exists(gitdir_path):
        return pathlib.Path(gitdir_path)
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)

    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")

    repo_dir = pathlib.Path(workdir / os.environ.get("GIT_DIR", ".git"))
    os.mkdir(repo_dir)

    standart_repo_subdirs = [
        "branches",
        "objects",
        "objects/pack",
        "refs",
        "refs/heads",
        "refs/tags",
    ]

    for subdir in standart_repo_subdirs:
        os.mkdir(repo_dir / subdir)

    with open(repo_dir / "HEAD", "w+") as f:
        f.write("ref: refs/heads/master\n")
    with open(repo_dir / "config", "w+") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    with open(repo_dir / "description", "w+") as f:
        f.write("Unnamed pyvcs repository.\n")

    return repo_dir
