""" Collects commit data for a single user. """
from pydriller import RepositoryMining

import pprint


# indicate path for repository by pluggin in the URL of repo (must be public)
repo_path = "https://github.com/GatorCogitate/cogitate_tool"


def collect_commits_user_email_key(repo):
    # TODO: edit the method to take in the URL for the repo
    """ Creates a dictionary of commit objects for a single user. """
    # holds email of repo members as keys, contents of commit object as values
    author_dict = {}


    # loop to turn the each Commits object into the values of the dictionary `author_dict`
    for commit in RepositoryMining(repo).traverse_commits():
        if commit.author.email not in author_dict.keys():
            author_dict[commit.author.email] = [commit]
        else:
            author_dict[commit.author.email].append(commit)
    return author_dict


def collect_commits_hash(repo):
    """
    Creates a list of dictionaries that contains commit info.

    hash (str): hash of the commit
    msg (str): commit message
    author (Developer): commit author (name, email)
    author_date (datetime): authored date
    merge (Bool): True if the commit is a merge commit
    change_type: type of the change: can be Added, Deleted, Modified, or Renamed.
    added: number of lines added
    removed: number of lines removed
    nloc: Lines Of Code (LOC) of the file
    complexity: Cyclomatic Complexity of the file
    methods: list of methods of the file.

    """

    commit_list = []

    for commit in RepositoryMining(repo).traverse_commits():

        line_added = 0
        line_removed = 0
        line_of_code = 0
        complexity = 0
        methods = []
        filename = []

        for item in commit.modifications:
            # modifications is a list of files and its changes
            line_added += item.added
            line_removed += item.removed
            if item.nloc is not None:
                line_of_code += item.nloc
            if item.complexity is not None:
                complexity += item.complexity

            for method in item.methods:
                methods.append(method.name)
            filename.append(item.filename)

        single_commit_dict = {
            "hash": commit.hash,
            "author_msg": commit.msg,
            "author_name": commit.author.name,
            "author_email": commit.author.email,
            "author_date": commit.author_date.date(),
            "merge": commit.merge,
            "line_added": line_added,
            "line_removed": line_removed,
            "lines_of_code": line_of_code,
            "complexity": complexity,
            "methods": methods,
            "filename": filename
        }

        commit_list.append(single_commit_dict)

    return commit_list
