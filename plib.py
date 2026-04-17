import argparse
import configparser
from datetime import datetime
import math
try:
    import grp, pwd
except ModuleNotFoundError:
    pass
from fnmatch import fnmatch
import hashlib
from math import ceil
import os, sys, re, zlib

# defining argparsers
argparser = argparse.ArgumentParser(description="pgit git written by kushal copying wyag")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add" : cmd_add(args)
        case "cat-file" : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout" : cmd_checkout(args)
        case "commit" : cmd_commit(args)
        case "hash-object" : cmd_hash_object(args)
        case "init" : cmd_init(args)
        case "log" : cmd_log(args)
        case "ls-files" : cmd_ls_files(args)
        case "ls-tree" : cmd_ls_tree(args)
        case "rev-parse" : cmd_rev_parse(args)
        case "rm" : cmd_rm(args)
        case "show-ref" : cmd_show_ref(args)
        case "status" : cmd_status(args)
        case "tag" : cmd_tag(args)
        case _ : print("Bad command.")

class GitRepository:
    workTree = None
    conf = None
    gitDir = None # git dir

    def __init__(self, path, force=False):
        self.workTree = path
        self.gitDir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitDir)):
                raise Exception("{} is not a Git Repository".format(path))

        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read(cf)
        elif not force:
            raise Exception("Configuration file expected at {} missing".format(cf))

        if not force:
            vers = int(self.conf.get("core"). "repositoryFormatVersion")
            if vers != 0:
                raise Exception(f"Unsupported repositoryFormatVersion {vers}") # got reminded of this one

# what does the star here mean?
# makes the function variadic (new term learned)
def repo_path(repo, *path):
    return os.path.join(repo.gitDir, *path)

def repo_dir(repo, *path, mkdir=False):
    """IG same as report path but returns the path only cases where
    a) path exists and directory
    b) if not existing then mkdir is given as True"""
    path = repo_path(repo, *path)
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"{path} is not a Directory")

    if mkdir:
        os.mkdir(path)
        return path
    else:
        return None

def repo_file(repo, *path, mkdir=False):
    """
    IG this checks for if the repo file is actually under a vali directory? and returns the path?
    if the repo dir needs to be created then its created first
    """
    if repo_dir(repo, *path[:-1], mkdir):
        return repo_path(repo, path)

