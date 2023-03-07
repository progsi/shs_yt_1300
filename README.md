# SHS-YouTube1300

This is the repository for the *SHS-YouTube1300* dataset. A dataset of cover versions from *YouTube*.


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7694973.svg)](https://doi.org/10.5281/zenodo.7694973)


# Ressources that we used
- *SHS100K* as seed dataset https://github.com/NovaFrost/SHS100K
- *Re-MOVE* for cover song identification https://github.com/furkanyesiler/re-move, our fork: https://github.com/progsi/re-move  
- *You-Only-Hear-Once* (*YOHO*) for audio segmentation and subsequent estimation of ratio of music https://github.com/satvik-venkatesh/you-only-hear-once/
- *Ditto* for entity matching https://github.com/megagonlabs/ditto, our fork: https://github.com/progsi/ditto

# Environment (Pandas, Pytables etc.)

```
conda env create -f env.yml
```

# Getting our dataset 

## Getting the audio features (CREMA-PCP and CQT Spectograms)

Check our Zenodo dataset publication to get the following Audio features
- CREMA-PCP features for our full crawl of 97k videos
- CQT spectograms for our SHS-YouTube-1300 dataset and the respective versions from the SHS100k dataset
- to get the CQT spectograms for the full crawl, please contact us! 

### HDF Store structe:
`audiofeatures/YT_ID/crema`: accesses the dataset CREMA-PCP feature of the respective `YT_ID` for instance `gORyrU1xQpg` for the video: https://www.youtube.com/watch?v=gORyrU1xQpg


## Getting the metadata

Since we are not allowed to share the *YouTube* metadata publicly, please contact us in case you are interested. 

To get our full dataset metadata including labels, similarity scores by *Re-MOVE* and *Ditto*, music ratios there are two options:

### Option 1: Writing CSV 

Run the following to generate a CSV file named `shs1300.csv` with semicolon separators into the `data` subdirectory.
```
python transformations.py
```

### Option 2: Load Dataframe in Python

```
import pandas as pd
import transformations

transformations.get_dataset()
```

# Dataset Attributes
This returns a *Pandas* dataframe including the following columns:
- `set_id`: set_id from *SHS100K* corresponding to a work (not the *Secondhandsongs* ID)
- `reference_yt_id`: *YouTube* identifier of the reference used as representation of work for the annotator
- `candidate_yt_id`: *YouTube* identifier of the crawled video which is annotated in relation to the reference
- `sample_group`: uncertainty sampling group (only filled for *MTurk* and expert data). One of the following: `re-move_favs`, `ditto_favs`, `mutual_unconfident` ("Re-MOVE favored", "Ditto favored" and "mutual unconfident") as described in the paper.
- `label`: the final class label `["Match", "Version", "Other", "No Music"]`
- `nlabel`: the numerical final class label (relevance score) `[3, 2, 1, 0]`
- `origin`: origin of annotation. This is either `worker`, `expert` or `staff`
- `seed`: boolean indicating whether the *YouTube* identifier is in the SHS100K seed dataset
- `ditto_pred`: aggregated *Ditto* based similarity between multiple references representing the work and `candidate_yt_id`
- `re-move_pred`: aggregated *Re-MOVE* based cosine similarity between multiple references representing the work and `reference_yt_id` and `candidate_yt_id`
- `music_ratio`: music ratio estimated by *YOHO*
- `non_music_ratio`: ratio of non-musical content
- `overlap_ratio`: the overlap between `music_ratio` and `non_music_ratio` 

# HDF Store Structure (further data)
You can access our HDF store `data/store_public.h5` to retrieve and analyze the individual dataframes.
We recommend to use pandas for this. For example, if you want to access the dataframe of `videos` of the work with `SET_ID` 100:

```
import pandas as pd

df = pd.read_hdf('data/store_public.h5', 'crawl/100/videos')
```

HDF structure of `store_public.h5`:
- `metadata`
  - `metadata/shs100k`: the metadata from *SHS100K*; keys: `set_id`, `ver_id`
  - `metadata/version_cues`: version cues (eg. "remix", "cover") extracted from literature, key: `cue`
  - `metadata/yt_title_cues`: *YouTube* identifiers (index) mapping to cue occurance in video title, key: `yt_id`
  - `metadata/yt_descr_cues`: *YouTube* identifiers (index) mapping to cue occurance in video description, key: `yt_id`
- `annotations`: `set_id` from *SHS100K* and *YouTube* identifiers (`yt_id`) mapping to...
  - `annotations/mturk`:  ...*MTurk* annotations by multiple workers based on majority vote (minimum three judgements)
  - `annotations/expert`: ...expert annotations and comments
  - `annotations/staff`: ...staff annotations
  - `annotations/similarities`: ...aggregated similarity scores computed by *Ditto* and *Re-MOVE*
  - `annotations/yoho_music_ratio`: ...music ratios extracted based on *YOHO*
- `crawl`: 
  - `crawl/queries`: `set_id`s mapping to all our queries to *YouTube*
  - `crawl/SET_ID/re-move_preds`: N X N matrix of cosine similarities by *Re-MOVE* of N videos for set with `SET_ID`.
  - `crawl/SET_ID/videos`: N x M matrix of all N videos for set with `SET_ID` mapping to the query rank if occurring in each of M queries.
  
# Analysis Example

Please check `exploration.ipynb` for some examples on data analysis (annotation quality, dataset insights).
