import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import watchtower.commits_ as wtc
from hacktrack.scrape import (_get_datadir, get_project_info, PROJECT_LIST)
sns.set(style='white')


def plot_commits_by_project(since='2018-08-07', datadir=None):
    """
    Makes bar plot of commits by project

    Parameters
    ----------
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    datadir : str, optional
        Path to where data on projects should be stored. Default: None

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    datadir = _get_datadir() if datadir is None else datadir

    # get project information
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[0]
    data = info.groupby('project').count().sha

    # make plot!
    ax = sns.barplot(data.values, data.index)
    sns.despine(ax=ax)
    ax.set(xlabel='Number of commits', ylabel='')
    ax.figure.tight_layout()

    return ax


def plot_commits_by_user(project=None, since='2018-08-07', datadir=None):
    """
    Makes bar plot of commits by user

    Parameters
    ----------
    project : str, optional
        Name of project to plot commits from. Default: None
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    datadir : str, optional
        Path to where data on projects should be stored. Default: None

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    datadir = _get_datadir() if datadir is None else datadir

    # get project information
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[0]
    if project is not None:
        info = info.query(f'project=="{project}"')
        if len(info) == 0:
            return

    # grab number of commits by user
    users = (info.dropna(subset=['author']).author
                 .apply(lambda x: x.get('login', None)))
    user, counts = np.unique(users, return_counts=True)

    # make plot!
    ax = sns.barplot(counts, user)
    sns.despine(ax=ax)
    ax.set(xlabel='Number of commits',
           title=project if project is not None else '')
    ax.figure.tight_layout()

    return ax


def plot_commits_by_time(project, since='2018-08-07', frequency='10H',
                         datadir=None):
    """
    Plots commits in `project` over time

    Parameters
    ----------
    project : str, optional
        Name of project to plot commits from
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to plot commits over time. Default: '10H'
    datadir : str, optional
        Path to where data on projects should be stored. Default: None

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    datadir = _get_datadir() if datadir is None else datadir

    # get info for specific project
    user, repo = project.split('/')
    info = wtc.load_commits(user, repo, data_home=datadir).date

    # grab rolling number of commits over time
    dates = pd.date_range(since, datetime.datetime.now(), freq=frequency)
    num_commits = [np.sum(info < d) for d in dates]

    # make plot!
    ax = sns.lineplot(dates, num_commits)
    sns.despine(ax=ax)
    ax.set(xlabel='Time', ylabel='Number of commits',
           title=project, ylim=[0, ax.get_ylim()[-1] + 10])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.figure.tight_layout()

    return ax


def scatter_by_statistics(project, since='2018-08-07', frequency='10H',
                          datadir=None):
    """
    Makes scatterplot of commits in `project` by additions + deletions

    Parameters
    ----------
    project : str, optional
        Name of project to plot commits from
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to plot commits over time. Default: '10H'
    datadir : str, optional
        Path to where data on projects should be stored. Default: None

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    datadir = _get_datadir() if datadir is None else datadir

    # get info for project
    user, repo = project.split('/')
    info = wtc.load_commits(user, repo, data_home=datadir)
    info['author'] = (info.dropna(subset=['author']).author
                          .apply(lambda x: x.get('login', None)))
    ax = sns.scatterplot(x='additions', y='deletions', data=info, hue='author')

    return ax


def plot_issues_by_time(project, since='2018-08-07', frequency='10H',
                        datadir=None):
    """
    Makes plot of issues created in `project` over time

    Parameters
    ----------
    project : str, optional
        Name of project to plot commits from
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to plot commits over time. Default: '10H'
    datadir : str, optional
        Path to where data on projects should be stored. Default: None

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
