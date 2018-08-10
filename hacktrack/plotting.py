import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from hacktrack.scrape import (get_project_info, PROJECT_LIST)
sns.set(style='white')


def plot_commits_by_project(since='2018-08-07', datadir=None, **kwargs):
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
    # get project information
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[0]
    data = info.groupby('project').count().sha

    # make plot!
    ax = sns.barplot(data.values, data.index, **kwargs)
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
    # get project information
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[0]
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        info = info[info.project.isin(project)]

    # grab number of commits by user
    info = info.query('user!=""')
    user, counts = np.unique(info.user, return_counts=True)

    # make plot!
    ax = sns.barplot(counts, user)
    sns.despine(ax=ax)
    ax.set(xlabel='Number of commits')
    ax.figure.tight_layout()

    return ax


def plot_commits_by_time(project=None, since='2018-08-07', frequency='10H',
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
    dates = pd.date_range(since, datetime.datetime.now(), freq=frequency)

    # get project info
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[0]
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        info = info[info.project.isin(project)]

    # compile number of commits over time for each project
    plot = pd.DataFrame([], columns=['time', 'commits',  'project'])
    for proj in info.project.unique():
        cp = info.query(f'project=="{proj}"')
        num_commits = np.array([np.sum(cp.date < d) for d in dates])
        plot = plot.append(pd.DataFrame(dict(time=dates,
                                             commits=num_commits,
                                             project=proj)))
    plot.commits = plot.commits.astype(int)

    # make plot!
    ax = sns.lineplot(x='time', y='commits', hue='project', data=plot)
    sns.despine(ax=ax)
    ax.set(xlabel='Time', ylabel='Number of commits',
           ylim=[0, ax.get_ylim()[-1] + 10])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.figure.tight_layout()

    return ax


def scatter_by_statistics(project=None, hue='project', since='2018-08-07',
                          datadir=None):
    """
    Makes scatterplot of commits in `project` by additions + deletions

    Parameters
    ----------
    project : str, optional
        Name of project to plot commits from
    hue : {'project', 'user'}, optional
        One of 'project' or 'user'
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
    # get project info
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[0]
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        info = info[info.project.isin(project)]
        hue = 'user'
    info.additions = info.additions.copy().apply(np.log)
    info.deletions = info.deletions.copy().apply(np.log)

    # make plot!
    ax = sns.scatterplot(x='additions', y='deletions', hue=hue, data=info)
    ax.set(xlabel='Lines of code added (log)',
           ylabel='Lines of code deleted (log)')
    sns.despine(ax=ax)

    return ax


def plot_issues_by_project(status='opened', by_time=True, since='2018-08-07',
                           frequency='10H', datadir=None):
    """
    Makes plot of issues created in `project` over time

    Parameters
    ----------
    status : {'opened', 'closed'}, optional
        Whether to plot issues that were 'opened' or 'closed'
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
    dates = pd.date_range(since, datetime.datetime.now(), freq=frequency)

    # get project info
    info = get_project_info(PROJECT_LIST, datadir=datadir,
                            since=since, verbose=False)[1]

    data = pd.DataFrame([], columns=['time', 'opened',
                                     'closed', 'project'])
    for proj in info.project.unique():
        cp = info.query(f'project=="{proj}"')
        oi = np.array([np.sum(cp.created_at.dropna() < d) for d in dates])
        ci = np.array([np.sum(cp.closed_at.dropna() < d) for d in dates])
        data = data.append(pd.DataFrame(dict(time=dates,
                                             opened=oi,
                                             closed=ci,
                                             project=proj)),
                           sort=True)
    data.opened = data.opened.astype(int)
    data.closed = data.closed.astype(int)

    # make plot!
    if by_time:
        ax = sns.lineplot(x='time', y=status, hue='project', data=data)
    else:
        data = data.groupby('project').max()[status]
        ax = sns.barplot(data.values, data.index)
        ax.figure.tight_layout()
    ax.set(ylabel='Issues {}'.format(status))
    sns.despine(ax=ax)

    return ax
