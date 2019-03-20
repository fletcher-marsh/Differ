# Differ: A comparison engine for Git histories

## How to use Differ
NOTE: These are instructions for a linux-based OS!  
  
In a clean directory run:
```
sh path/to/setup.sh
```
This should put the `differ` binary in your environment as well as download all student repositories for a given phase. Now you can use the program by typing:
```
differ [parent directory of repositories] [option] [val]
```
Or:
```
differ [repo1_dir] [repo2_dir] [repo3_dir] ... [option] [val]
```
## Supported options
`--time [n]`  
  
### Summary:  
Group commits from repositories by commit time. Groups in chunks of minutes according to `n`.
  
### Example:
```
differ /path/to/repos --time 3
```
This will group commits into batches made with **3 minutes of each other**.

## Dependencies
 * [GitPython](https://gitpython.readthedocs.io/en/stable/)

