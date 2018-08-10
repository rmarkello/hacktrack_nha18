import datetime
import os.path as op
import numpy as np
import pandas as pd
import seaborn as sns
import watchtower.commits_ as wtc
import watchtower.issues_ as wti
sns.set(style='white')

PROJECT_LIST = op.join(op.dirname(op.abspath(__file__)),
                       'data/.projects.csv')


def get_all_project_info(project_list, datadir='./data', since='2018-08-05',
                         update=False, verbose=True):
    """
    Gets project info (commits + issues) from `project_list`

    Parameters
    ----------
    project_list : str
        Filepath to project list with columns user/repo
    datadir : str, optional
        Path to where data on projects should be stored. Default: './data'
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-05
    update : bool, optional
        Whether to update project information (query GitHub) or simply load
        already pulled information. Default: False
    verbose : bool, optional
        Whether to print messages as data are updated/loaded. Default: True

    Returns
    -------
    commits : pd.core.data.DataFrame
        Information on commits from projects in `project_list`
    issues : pd.core.data.DataFrame
        Information on issues from projects in `project_list`
    """

    # empty dataframes to store all data
    commits, issues = pd.DataFrame(), pd.DataFrame()

    # determine if updating or loading info
    gc = getattr(wtc, '{}_commits'.format('update' if update else 'load'))
    gi = getattr(wti, '{}_issues'.format('update' if update else 'load'))
    params = dict(data_home=datadir)
    if update:
        params.update(since=since)

    # go through all projects and grab information
    for idx, proj in pd.read_csv(project_list).iterrows():
        if verbose:
            print('{} commit and issue information for {}/{}'
                  .format('Updating' if update else 'Getting',
                          proj.user, proj.repo))
        com = gc(proj.user, proj.repo, **params)
        iss = gi(proj.user, proj.repo, **params)
        if com is None or iss is None:
            continue
        commits = commits.append(com.assign(project='{}/{}'.format(proj.user,
                                                                   proj.repo)),
                                 sort=False)
        issues = issues.append(iss.assign(project='{}/{}'.format(proj.user,
                                                                 proj.repo)),
                               sort=False)

    return commits, issues


def plot_commits_by_project(since='2018-08-07', datadir='./data'):
    """
    Makes bar plot of commits by project

    Parameters
    ----------
    since : str, optional
        Date (YYYY-MM-DD) from which to pull information on projects:
        Default: 2018-08-07
    datadir : str, optional
        Path to where data on projects should be stored. Default: './data'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    # get project information
    info = get_all_project_info(PROJECT_LIST, datadir=datadir,
                                since=since, verbose=False)[0]
    data = info.groupby('project').count().sha

    # make plot!
    ax = sns.barplot(data.values, data.index)
    sns.despine(ax=ax)
    ax.set(xlabel='Number of commits', ylabel='')
    ax.figure.tight_layout()

    return ax


def plot_commits_by_user(project=None, since='2018-08-07', datadir='./data'):
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
        Path to where data on projects should be stored. Default: './data'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    # get project information
    info = get_all_project_info(PROJECT_LIST, datadir=datadir,
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
                         datadir='./data'):
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
        Path to where data on projects should be stored. Default: './data'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    # get info for specifiy project
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
                          datadir='./data'):
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
        Path to where data on projects should be stored. Default: './data'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
    # get info for project
    user, repo = project.split('/')
    info = wtc.load_commits(user, repo, data_home=datadir)
    info['author'] = (info.dropna(subset=['author']).author
                          .apply(lambda x: x.get('login', None)))
    ax = sns.scatterplot(x='additions', y='deletions', data=info, hue='author')

    return ax


def plot_issues_by_time(project, since='2018-08-07', frequency='10H',
                        datadir='./data'):
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
        Path to where data on projects should be stored. Default: './data'

    Returns
    -------
    ax : matplotlib.axes.Axis
        Axis with plot
    """
