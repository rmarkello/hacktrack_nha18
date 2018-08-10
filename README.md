# hacktrack
A small project for making plots of hackathon statistics. Designed at Neurohackademy 2018.

# Installation and setup
It is _strongly_ encouraged you install via the following in a new conda environment or your code will very likely **not work**. Sorry!

```bash
git clone https://github.com/rmarkello/hacktrack.git
cd hacktrack
conda create -n hacktrack python=3.6 numpy matplotlib pandas seaborn tqdm
pip install git+git://github.com/rmarkello/watchtower
pip install -e .
```

You will also want to get a Github personal access token by signing in to Github and navigating to [https://github.com/settings/tokens](https://github.com/settings/tokens). It would be wise to select read-only for the majority of the options and save the access token generated. Set it up as an environmental variable `GITHUB_API` in the form username:key, as in:

```bash
$ export GITHUB_API=rmarkello:1239012803218032981390218930218939021323
```

# Usage

```python
>>> from hacktrack import PROJECT_LIST, get_all_project_info
>>> commits, issues = get_all_project_info(PROJECT_LIST, update=True)
```

`commits` and `issues` are both pandas dataframes with a whole bunch of information about commits and issues.

You can also check out `hacktrack.plotting` to do some fun plotting things.
