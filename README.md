# hacktrack
A small project for making plots of hackathon statistics. Designed at Neurohackademy 2018.

# Installation and setup
It is _strongly_ encouraged you install via the following in a new `conda` environment or your code will very likely **not work**. Sorry!

```bash
# create a new conda env with the required modules
conda create -n hacktrack python=3.6 numpy matplotlib pandas seaborn tqdm
source activate hacktrack
# install rmarkello/watchtower, forked form docathon/watchtower
pip install git+git://github.com/rmarkello/watchtower
# install hacktrack in developer mode
git clone https://github.com/rmarkello/hacktrack.git
cd hacktrack
pip install -e .
```

You will also want to get a GitHub personal access token by signing in to GitHub and navigating to [https://github.com/settings/tokens](https://github.com/settings/tokens). It would be wise to select read-only for the majority of the options and save the access token generated. Set it up as an environmental variable `GITHUB_API` in the form username:key, as in:

```bash
$ export GITHUB_API=rmarkello:1239012803218032981390218930218939021323
```

# Usage
```python
>>> from hacktrack import PROJECT_LIST, get_project_info
>>> commits, issues = get_project_info(PROJECT_LIST, update=True)
```

`commits` and `issues` are both pandas `DataFrame` objects with a whole bunch of information about commits and issues.

You can also check out `hacktrack.plotting` to do some fun plotting things!
