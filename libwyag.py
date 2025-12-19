import argparse
import configparser
from datetime import datetime 
import grp, pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib

argparse = argparse.ArgumentParser(description= "The Stupidest Content Tracking System")

argsubparsers = argparse.add_subparsers(title="Commands", dest="command")  # noqa: F821
argsubparsers.required = True

def main(argv=sys.argv[1:]):
    args = argparse.parse_args(argv)
    match args.command:
        case "add"     : cmd_add(args)
        case "commit"  : cmd_commit(args)
        case "init"    : cmd_init(args)
        case "cat-file" : cmd_case_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout" : cmd_checkout(args)
        case "hash-object" : cmd_hash_object(args)
        case "log" : cmd_log(args)
        case "ls-files" : cmd_ls_files(args)
        case "ls-tree" : cmd_ls_tree(args)
        case "rev-parse" : cmd_rev_parse(args)
        case "rm" : cmd_rm(args)
        case "show-ref" : cmd_show_ref(args)
        case "status" : cmd_status(args)
        case "tag" : cmd_tag(args)
        case _ : print("Bad command")

class GitRepository(object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force = False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")
        
        #Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversionre"))
            if vers !=0:
                raise Exception("Unsupported repositoryformatversion: {vers}")
            
def repo_path(repo, *path):
    """Compute path under repo's gitdir"""
    return os.path.join(repo.gitdir, *path)
    
def repo_file(repo, *path, mkdir=False):
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)
    
    
    
def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if(os.path.isdir(path)):
            return path
        else:
            raise Exception(f"Not a directory{path}")
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def repo_create(path):
    """Create a new peository at path"""

    repo = GitRepository(path, True)

    #check if path exists

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory!")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception (f"{path} is a not empty!")
    else:
        os.makedirs(repo.worktree)

    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo,"objects", mkdir=True)
    assert repo_dir(repo,"refs", "tags", mkdir=True)
    assert repo_dir(repo,"refs", "heads", mkdir=True)
    
    # .git/description

    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD

    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo

def repo_default_config():
    """Create default repository configuration with user profile"""
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    ret.add_section("user")
    ret.set("user", "name", "Dave Jones")
    ret.set("user", "email", "beybladee763@gmail.com")

    return ret

# Command stub implementations
def cmd_add(args):
    """Add file contents to the index"""
    print("add command not yet implemented")

def cmd_commit(args):
    """Record changes to the repository"""
    print("commit command not yet implemented")

def cmd_init(args):
    """Create an empty Git repository"""
    repo_create(args.path)

def cmd_case_file(args):
    """Provide content of repository objects"""
    print("cat-file command not yet implemented")

def cmd_check_ignore(args):
    """Check path(s) against ignore rules"""
    print("check-ignore command not yet implemented")

def cmd_checkout(args):
    """Switch branches or restore working tree files"""
    print("checkout command not yet implemented")

def cmd_hash_object(args):
    """Compute object ID and optionally creates a blob from a file"""
    print("hash-object command not yet implemented")

def cmd_log(args):
    """Show commit logs"""
    print("log command not yet implemented")

def cmd_ls_files(args):
    """Show information about files in the index and the working tree"""
    print("ls-files command not yet implemented")

def cmd_ls_tree(args):
    """List the contents of a tree object"""
    print("ls-tree command not yet implemented")

def cmd_rev_parse(args):
    """Parse revision (or other objects) identifiers"""
    print("rev-parse command not yet implemented")

def cmd_rm(args):
    """Remove files from the working tree and from the index"""
    print("rm command not yet implemented")

def cmd_show_ref(args):
    """List references"""
    print("show-ref command not yet implemented")

def cmd_status(args):
    """Show the working tree status"""
    print("status command not yet implemented")

def cmd_tag(args):
    """Create, list, delete or verify a tag object"""
    print("tag command not yet implemented")

# Argument parsers for each command
argsp_init = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
argsp_init.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository.")
