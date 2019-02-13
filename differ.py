#!/usr/bin/env python3

import git
import sys
import os
import argparse

parser = argparse.ArgumentParser(description="An engine for comparing Git histories")
parser.add_argument("directory", type=str, nargs=1, 
                    help="path to folder containing all projects (each containing a Git repo")
parser.add_argument("--time", dest="by_time", required=False, nargs=1, type=int,
                    help="group commits together by time buckets (in minutes)")
    

# Group commits associated with students together by time (1 min intervals)
def create_buckets(repos):
    # for every submission made at xx:xx:00 - xx:xx:59, put in bucket xx:xx
    pass

# Synthesize aggregate information for submissions
def load_repos(paths):
    all_repos = {}
    # Load repository info for every submission
    for path in paths:
        andrew_id = path # TODO: How to programmatically access andrew id
        all_repos[andrew_id] = git.Repo(path)
    return all_repos

def run_time_comparison(repos, time):
    # Bucket commits by time stamp to track commits made close together
    buckets = create_buckets(all_repos)

    # Given input time period in minutes, collect all <time> minute interval groups
    groups = get_groups(buckets, time)

def main():
    args = parser.parse_args()
    if args.by_time:
        projects = os.listdir(args.directory[0])
        full_paths = map(lambda p: args.directory[0] + os.sep + p, projects)
        repos = load_repos(full_paths)
        run_time_comparison(repos, int(args.by_time[0]))


if __name__ == "__main__":
    main()