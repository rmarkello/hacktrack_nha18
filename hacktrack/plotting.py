import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(style='white')


def plot_commits_by_project(commits, ax=None):
    """
    Makes bar plot of commits by project

    Parameters
    ----------
    commits : pd.core.data.DataFrame
        Information on commits from projects

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    # get project information
    data = commits.groupby('project').count().sha

    # make plot!
    ax = sns.barplot(data.values, data.index, ax=ax)
    sns.despine(ax=ax)
    ax.set_title('Total commits over time')
    ax.set_xlabel('Number of commits', labelpad=20)
    ax.set_ylabel('Project', labelpad=20)
    ax.figure.tight_layout()

    return ax


def plot_commits_by_user(commits, project=None, ax=None):
    """
    Makes bar plot of commits by user

    Parameters
    ----------
    commits : pd.core.data.DataFrame
        Information on commits from projects
    project : str, optional
        Name of project to plot commits from. Default: None

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    # get project information
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        commits = commits[commits.project.isin(project)]

    # grab number of commits by user
    commits = commits.query('user!=""')
    user, counts = np.unique(commits.user, return_counts=True)

    # make plot!
    ax = sns.barplot(counts, user, ax=ax)
    sns.despine(ax=ax)
    ax.set_xlabel('Number of commits', labelpad=20)
    ax.set_ylabel('Users', labelpad=20)
    ax.figure.tight_layout()

    return ax


def plot_commits_by_time(commits, project=None, since='2018-08-07',
                         frequency='10H', ax=None):
    """
    Plots commits in `project` over time

    Parameters
    ----------
    commits : pd.core.data.DataFrame
        Information on commits from projects
    project : str, optional
        Name of project to plot commits from
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to plot commits over time. Default: '10H'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    dates = pd.date_range(since, datetime.datetime.now(), freq=frequency)

    # get project info
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        commits = commits[commits.project.isin(project)]

    # compile number of commits over time for each project
    plot = pd.DataFrame([], columns=['time', 'commits',  'project'])
    for proj in commits.project.unique():
        cp = commits.query(f'project=="{proj}"')
        num_commits = np.array([np.sum(cp.date < d) for d in dates])
        plot = plot.append(pd.DataFrame(dict(time=dates,
                                             commits=num_commits,
                                             project=proj)))
    plot.commits = plot.commits.astype(int)

    # make plot!
    ax = sns.lineplot(x='time', y='commits', hue='project', data=plot, ax=ax)
    sns.despine(ax=ax)
    ax.set(xlabel='Time', ylabel='Number of commits',
           ylim=[0, ax.get_ylim()[-1] + 10],
           title='Cumulative commits across time')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.figure.tight_layout()

    return ax


def scatter_by_statistics(commits, project=None, hue='project', ax=None):
    """
    Makes scatterplot of commits in `project` by additions + deletions

    Parameters
    ----------
    commits : pd.core.data.DataFrame
        Information on commits from projects
    project : str, optional
        Name of project to plot commits from
    hue : {'project', 'user'}, optional
        One of 'project' or 'user'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    data = commits.copy()

    # get project info
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        data = data[data.project.isin(project)]
        hue = 'user'
    data.loc[:, 'additions'] = data.additions.copy().apply(np.log)
    data.loc[:, 'deletions'] = data.deletions.copy().apply(np.log)

    # make plot!
    ax = sns.scatterplot(x='additions', y='deletions', hue=hue, data=data,
                         ax=ax)
    ax.legend_.set_bbox_to_anchor((1.0, 1.0))
    ax.set(xlabel='Lines of code added (log)',
           ylabel='Lines of code deleted (log)')
    sns.despine(ax=ax)

    return ax


def _prepare_issues(issues, since='2018-08-07', frequency='10H'):
    """
    Prepares `issues` into slightly tidier data frame for plotting

    Parameters
    ----------
    issues : pd.core.data.DataFrame
        Information on issues from projects
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to group issues. Default: '10H'

    Returns
    -------
    issues : pd.core.data.DataFrame
        Organized issues!
    """
    dates = pd.date_range(since, datetime.datetime.now(), freq=frequency)

    # get project info
    data = pd.DataFrame([], columns=['time', 'number',
                                     'status', 'project'])
    for proj in issues.project.unique():
        cp = issues.query(f'project=="{proj}"')
        ci, oi = [], []
        for n, d in enumerate(dates[1:], 1):
            low, high = dates[n-1], d
            col = 'closed_at'
            ci += [len(cp.dropna(subset=[col])
                         .query(f'{col} < "{high}" & {col} >= "{low}"'))]
            col = 'created_at'
            oi += [len(cp.dropna(subset=[col])
                         .query(f'{col} < "{high}" & {col} >= "{low}"'))]
        inputs = dict(time=np.tile(dates[1:], 2),
                      number=np.hstack([oi, ci]),
                      status=np.hstack([np.repeat('opened', len(oi)),
                                        np.repeat('closed', len(ci))]),
                      project=proj)
        data = data.append(pd.DataFrame(inputs), sort=True)
    data.number = data.number.astype(int)

    return data


def plot_issues_by_project(issues, project=None, since='2018-08-07',
                           frequency='10H', ax=None):
    """
    Makes plot of `issues` by time (by project if not `by_time`)

    Parameters
    ----------
    issues : pd.core.data.DataFrame
        Information on issues from projects
    project : str, optional
        If `by_time`, the name of the project from which to plot issues
    by_time : bool, optional
        Whther to plot issues as a function of time instead of project.
        Default: True
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to plot issues. Default: '10H'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    data = _prepare_issues(issues, since=since, frequency=frequency)
    data = (data.drop('time', axis=1)
                .groupby(['project', 'status'])
                .sum()
                .reset_index())
    closed = data.query('status=="closed"')
    opened = data.query('status=="opened"')
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    ax.barh(closed.project, closed.number, label='Closed issues')
    plt.barh(opened.project, opened.number, left=closed.number,
             label='Open issues')
    ax.set(xlabel='Number of issues')
    ax.figure.tight_layout()
    plt.legend()

    sns.despine(ax=ax)

    return ax


def plot_issues_by_time(issues, project=None, since='2018-08-07',
                        frequency='10H', ax=None):
    """
    Makes plot of `issues` by time (by project if not `by_time`)

    Parameters
    ----------
    issues : pd.core.data.DataFrame
        Information on issues from projects
    project : str, optional
        If `by_time`, the name of the project from which to plot issues
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    frequency : str, optional
        Time chunks with which to plot issues. Default: '10H'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    data = _prepare_issues(issues, since=since, frequency=frequency)

    # get project info
    if project is not None:
        if not isinstance(project, list):
            project = [project]
        data = data[data.project.isin(project)]
    hue = None if len(project) == 1 else 'project'
    ax = sns.lineplot(x='time', y='number', hue=hue, style='status',
                      data=data, ax=ax)
    xticklabels = (data.time
                       .apply(lambda x: x.strftime('%Y-%m-%d %H'))
                       .unique())
    ax.set(xticks=xticklabels,
           title=project[0] if hue is None else '')
    ax.legend_.set_bbox_to_anchor((1.0, 1.0))
    ax.set_xlabel('Time', labelpad=15)
    ax.set_ylabel('Number of issues', labelpad=15)
    ax.set_xticklabels(xticklabels, rotation=45)
    sns.despine(ax=ax)

    return ax
