#!/usr/bin/env python3

import git
import sys
import os
import argparse
import time

parser = argparse.ArgumentParser(description="An engine for comparing Git histories")
parser.add_argument("directories", type=str, nargs="+",
                    help="paths to folders containing all projects (each containing a Git repo)")
parser.add_argument("--time", dest="by_time", required=False, nargs=1, type=int,
                    help="group commits together by time buckets (in minutes)")

# Group commits associated with students together by time (1 min intervals)
def create_buckets(repos, time):
    bucket_size = 60 # in seconds
    buckets = {}
    for owner in repos:
        for commit in repos[owner].iter_commits():
            bucket = commit.committed_date // bucket_size * bucket_size # translate to bucket in seconds
            buckets[bucket] = buckets.get(bucket, []) + [(commit.author.name, commit.message)]
    return buckets

# Combine 1 min intervals of commits into <time> min intervals
def get_groups(buckets, time):
    times = sorted(buckets.keys())

    if len(times) < time:
        # If we have less buckets than <time> in minutes, we either have:
        #       1. few submissions
        #       2. a weird situation where everybody committed at the same time
        # In either case, `buckets` already has the groupings
        return buckets

    # Otherwise, we can group according to the earliest time in the <time> size period
    groups = {}
    for i in range(len(times) - time + 1):
        commit_time = times[i] # commit1
        added_commit = False
        for nearby in range(1, time+1):
            try_time = commit_time + (nearby * 60) # commit2
            if try_time in buckets:
                # We have a grouping!
                if not added_commit:
                    # Only add commit1 once
                    groups[commit_time] = groups.get(commit_time, []) + buckets[commit_time]
                    added_commit = True
                groups[commit_time] += buckets[try_time]
    return groups

# Synthesize aggregate information for submissions
def load_repos(paths):
    all_repos = {}

    for path in paths:
        repo = git.Repo(path)
        author = repo.head.commit.author.name
        all_repos[author] = git.Repo(path)

    return all_repos

# Get grouped commits given time in minutes
def run_time_comparison(repos, time):
    # Bucket commits by time stamp to track commits made close together
    buckets = create_buckets(repos, time)

    # Given input time period in minutes, collect all <time> minute interval groups
    groups = get_groups(buckets, time)

    return groups


def bold(s):
    return "\033[1m" + s + "\033[0m"

def section_header(s):
    return "========================\n" + bold(s) + "\n========================\n"

def output(groups):
    for grp in sorted(groups.keys()):
        tup_time = time.gmtime(grp)
        readable_time = time.asctime(tup_time)
        print(section_header(readable_time))
        for commit in groups[grp]:
            print(bold(commit[0]) + ": " + commit[1].strip())
            print()
        print()

# Handle various directory inputs to Differ
def get_all_paths(dirs):
    if len(dirs) == 1:
        try:
            # User provided a single valid repo
            git.Repo(dirs[0])
            return dirs
        except:
            # User provided a parent directory to repos
            projects = os.listdir(dirs[0])
            paths = map(lambda p: dirs[0] + os.sep + p, projects)
            return paths
    else:
        # User provided exact paths to repos, no need to do any parsing
        return dirs

# Handle logistics based off of type of comparison requested
def main():
    args = parser.parse_args()
    full_paths = get_all_paths(args.directories)
    repos = load_repos(full_paths)
    if args.by_time:
        groups = run_time_comparison(repos, args.by_time[0])
        output(groups)

if __name__ == "__main__":
    main()
