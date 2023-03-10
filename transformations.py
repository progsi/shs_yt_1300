import pandas as pd


def get_dataset(tertiary=False):
    """
    loads the SHS-YouTube-1300 dataset as a pandas dataframe
    :param tertiary: whether to aggregate to tertiary labels (interpreting label "Match" as "Version")
    :return: dataframe of dataset
    """
    return pd.merge(
        pd.merge(
            get_annotations(tertiary=tertiary).reset_index().drop('ver_id', axis=1),
            pd.read_hdf('data/store_public.h5', 'annotations/similarities').reset_index().drop('ver_id', axis=1),
            how='inner', left_on=['set_id', 'candidate_yt_id'],
            right_on=['set_id', 'yt_id']),
        pd.read_hdf('data/store_public.h5', 'annotations/yoho_musicratio'), how='left', on='yt_id'
    ).drop('yt_id', axis=1)


def get_mturk_pivot(value_col='label_worker'):
    """
    pivots the mturk data, each task (MTurk HIT) mapping to multiple assignments
    :param value_col: label to consider for showing (either "label_worker" for string label in ["Match", "Version",
    "Other", "No Music"] or "nlabel_worker" for numerical relevance score in [0, 1, 2, 3]
    :return: pivoted dataframe in dimension N*M for N tasks and M maximal worker assignments
    """
    df = pd.read_hdf('data/store_public.h5', 'annotations/mturk').reset_index()

    def attach_assignment_counter_column(df: pd.DataFrame):
        df_counter = df[['reference_yt_id', 'AssignmentId']].drop_duplicates()
        df_counter['Counter'] = df_counter.groupby('reference_yt_id').cumcount()

        return pd.merge(df, df_counter, how='left', on=['reference_yt_id', 'AssignmentId'])

    df = attach_assignment_counter_column(df)

    df = df[~df.sample_group.str.contains('match')]

    df = df.pivot(index=["set_id", "ver_id", "reference_yt_id", "candidate_yt_id",
                         "sample_group"], columns=["Counter"], values=value_col)

    df.columns = ["worker_ind" + str(col) for col in df.columns]

    return df.iloc[:, :5] # limiting to five, because one HIT has to many assignments (bug)


def get_annotations_expert():
    """
    loading expert annotations
    :return: expert annotation dataframe
    """
    return pd.read_hdf('data/store_public.h5', 'annotations/expert')


def get_annotations_mturk_mv(tertiary=False):
    """
    get the respective MTurk annotations as a dataframe (aggregated pivot)
    :param tertiary: whether to aggregate to tertiary labels (interpreting label "Match" as "Version")
    :return: MTurk annotation dataframe
    """

    df = get_mturk_pivot()

    if tertiary:
        # reduce classes to three
        df = df.replace('Match', 'Version')

    def get_mode(row):
        mode = row.mode().iloc[0]
        return mode, row.value_counts().loc[mode]

    df['label_worker_mv'], df['mv_mode'] = zip(*df.apply(get_mode, axis=1))

    return df[['label_worker_mv', 'mv_mode']]


def get_annotations_mturk_mean():
    """
    get mean aggregated MTurk annotations as dataframe
    :return: MTurk annotation dataframe (mean)
    """
    df = get_mturk_pivot('nlabel_worker')

    def get_mean(row):
        mean = row.mean()
        return mean, row.count()

    df['label_worker_mean'], df['mean_count'] = zip(*df.apply(get_mean, axis=1))

    return df[['label_worker_mean', 'mean_count']]


def get_annotations_staff():
    """
    get staff anotation dataframe, filtering only for the cases where both annotators agree
    :return: staff annotation dataframe
    """
    df = pd.read_hdf('data/store_public.h5', 'annotations/staff')

    df = df[df["label_staff1"] == df["label_staff2"]]

    df["label_staff"] = df["label_staff1"]
    df["nlabel_staff"] = df["nlabel_staff1"]

    return df[["label_staff", "nlabel_staff"]]


def get_annotations(lean=True, tertiary=False):
    """
    get all annotations
    :param lean: lean for less columns
    :param tertiary: whether to aggregate to tertiary labels (interpreting label "Match" as "Version")
    :return: dataframe with all annotations mapped to by set_ids and candidate YouTube IDs
    """
    df = get_annotations_staff().join(
        get_annotations_mturk_mean().join(
            get_annotations_mturk_mv(tertiary=tertiary)).join(
                pd.read_hdf('data/store_public.h5', 'annotations/expert')
        ), how="outer"
    )

    def get_class_label(x):
        if pd.notna(x.label_expert):
            return x.label_expert, 'expert'
        elif pd.notna(x.label_staff):
            return x.label_staff, 'staff'
        elif pd.notna(x.label_worker_mv):
            return x.label_worker_mv, 'worker'

    df["label"], df["origin"] = zip(*df.apply(get_class_label, axis=1))

    if tertiary:
        df["label"] = df["label"].str.replace('Match', 'Version')

    def get_nlabel(x):
        if x == 'Match':
            return 3
        elif x == 'Version':
            return 2
        elif x == "Other":
            return 1
        elif x == "No Music":
            return 0
        else:
            return None

    df["nlabel"] = df["label"].apply(get_nlabel)

    if lean:
        return df[["label", "nlabel", "origin"]]
    else:
        return df[["label", "nlabel", "origin", "nlabel_staff", "label_worker_mean", "nlabel_expert",
                   "comment_expert", "category_expert"]]


if __name__ == "__main__":
    get_dataset().to_csv('data/shs1300.csv', index=None, sep=';')

