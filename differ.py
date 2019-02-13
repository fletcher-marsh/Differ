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
def create_buckets(repos, time):
    bucket_size = 60 # in seconds
    buckets = {}
    for student in repos:
        commit_history = repos[student].head.reference.log()
        for commit in commit_history:
            bucket = commit.time[0] // bucket_size * bucket_size # translate to bucket in seconds
            buckets[bucket] = buckets.get(bucket, []) + [(student, commit)]
    return buckets

# Combine 1 min intervals of commits into <time> min intervals
def get_groups(buckets, time):
    times = sorted(buckets.keys())

    # If we have less buckets than <time> in minutes, we either have:
    #   1. few submissions
    #   2. a weird situation where everybody committed at the same time
    # In either case, `buckets` already has the groupings
    if len(times) < time:
        return buckets

    # Otherwise, we can group according to the earliest time in the <time> size period
    groups = {}
    for i in range(len(times), -time):
        commit_time = times[i]
        for nearby in range(time):
            if (commit_time + (nearby * 60)) in buckets:
                # We have a grouping!
                groups[commit_time] = groups.get(commit_time, []) + [buckets[commit_time]]
    return groups

# Synthesize aggregate information for submissions
def load_repos(paths):
    all_repos = {}

    for path in paths:
        repo = git.Repo(path)
        author = repo.head.commit.author
        all_repos[author] = git.Repo(path)

    return all_repos

# Get grouped commits given time in minutes
def run_time_comparison(repos, time):
    # Bucket commits by time stamp to track commits made close together
    buckets = create_buckets(repos, time)
    print(buckets)
    # Given input time period in minutes, collect all <time> minute interval groups
    groups = get_groups(buckets, time)

def main():
    args = parser.parse_args()
    projects = os.listdir(args.directory[0])
    full_paths = map(lambda p: args.directory[0] + os.sep + p, projects)
    repos = load_repos(full_paths)
    if args.by_time:
        run_time_comparison(repos, args.by_time[0])


if __name__ == "__main__":
    main()