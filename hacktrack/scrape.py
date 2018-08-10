import os.path as op
import pandas as pd
import watchtower.commits_ as wtc
import watchtower.issues_ as wti

PROJECT_LIST = op.join(op.dirname(op.abspath(__file__)),
                       'data/.projects.csv')


def _get_datadir():
    """ Gets data directory where `PROJECT_LIST` is located
    """
    return op.dirname(PROJECT_LIST)


def get_project_info(project_list, datadir=None, since='2018-08-05',
                     update=False, verbose=True):
    """
    Gets project info (commits + issues) from `project_list`

    Parameters
    ----------
    project_list : str
        Filepath to project list with columns user/repo
    datadir : str, optional
        Path to where data on projects should be stored. Default: None
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
    datadir = _get_datadir() if datadir is None else datadir

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
