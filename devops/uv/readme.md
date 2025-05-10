# uv : rust based python project/package manager

### uv scripts
executes standalone python scripts (.py files)

No need to create separate envs to run scripts, uv creats a env internally to execute it without affecting or interacting with any of the existing env 

```bash
# execute file
uv run script.py

# create a new script
uv init --script file_name.py python-version

# add external dependencies to script -> will update script with dependencies (check with_dependencies.py)
uv add --script file_name.py 'dep-1' 'dep-2' 'requests' 'pandas'

uv run file_name.py

# create lock file for the script
uv lock --script file_name.py
```

### uv projects
well formatted and orchestrated python projects
the project can either be a python application or library


```bash
# initialize a project
uv init app-name

uv run app-name.py

# initialize a package (something to be installed rather than run/executed. build stage will be included in .toml)
uv init --package app-name

uv run exe-pkg-name    (name will be declared in .toml under python scripts)

# initilaze library (library will always be a package)
uv init --lib app-name

# just .toml file (bare)
uv init app-name --bare


# Add dependency to a project
uv add 'lib-name'

# import from requirements.txt
uv add -r requirements.txt

# remove dependency
uv remove 'lib-name'
```

### uv tools
executes python packages published as tools liek ruff, black


### uv utilty
manage uv's states

```bash
# removes all cache
uv cache clean 


# remove specific lib from cache
uv cache remove 'lib-name'

# remove unused cache entries
uv cache prune
```


## uv lock

```bash
uv pip compile requirements.txt -o requirements.lock

uv pip compile pyproject.toml -o requirements.lock

uv pip install -r requirements.lock

# create lock file for a script
uv lock 

# sync with env
uv sync
```
