# SHS-YouTube1300
This is the repository for the *SHS-YouTube1300* dataset. A dataset of cover versions from *YouTube*.

[![DOI](https://zenodo.org/badge/601052917.svg)](https://zenodo.org/badge/latestdoi/601052917)

# Ressources that we used
- *SHS100K* as seed dataset https://github.com/NovaFrost/SHS100K
- *Re-MOVE* for cover song identification https://github.com/furkanyesiler/re-move, our fork: https://github.com/progsi/re-move  
- *You-Only-Hear-Once* (*YOHO*) for audio segmentation and subsequent estimation of ratio of music https://github.com/satvik-venkatesh/you-only-hear-once/
- *Ditto* for entity matching https://github.com/megagonlabs/ditto, our fork: https://github.com/progsi/ditto

# Environment (Pandas, Pytables etc.)

```
conda env create -f environment.yml
```

# Getting our dataset (metadata)
Since we are not allowed to share the *YouTube* metadata publicly, please contact us in case you are interested. 
To get our full dataset metadata including labels, similarity scores by *Re-MOVE* and *Ditto*, music ratios as a CSV run:

```
python transformations.py
```
or you can load the Dataframe using our provided Script (for instance when using a Jupyter Environment)

```
import pandas as pd
import transformations

transformations.get_dataset()
```

This returns a *Pandas* dataframe including the following columns:
- `set_id`: set_id from *SHS100K* corresponding to a work (not the *Secondhandsongs* ID)
- `reference_yt_id`: *YouTube* identifier of the reference used as representation of work for the annotator
- `candidate_yt_id`: *YouTube* identifier of the crawled video which is annotated in relation to the reference
- `sample_group`: uncertainty sampling group (only filled for *MTurk* and expert data). One of the following: `re-move_favs`, `ditto_favs`, `mutual_unconfident` ("Re-MOVE favored", "Ditto favored" and "mutual unconfident") as described in the paper.
- `label`: the final class label `["Match", "Version", "Other", "No Music"]`
- `ǹlabel`: the numerical final class label (relevance score) `[3, 2, 1, 0]`
- `origin`: origin of annotation. This is either `worker`, `expert` or `staff`
- `seed`: boolean indicating whether the *YouTube* identifier is in the SHS100K seed dataset
- `ditto_pred`: aggregated *Ditto* based similarity between multiple references representing the work and `candidate_yt_id`
- `re-move_pred`: aggregated *Re-MOVE* based cosine similarity between multiple references representing the work and `reference_yt_id` and `candidate_yt_id`
- `music_ratio`: music ratio estimated by *YOHO*
- `ǹon_music_ratio`: ratio of non-musical content
- `overlap_ratio`: the overlap between `music_ratio` and `overlap_ratio` 

# HDF Store Structure
HDF structure of `store_public.h5`:
- `metadata`
  - `metadata/shs100k`: the metadata from *SHS100K*
  - `metadata/version_cues`: version cues (eg. "remix", "cover") extracted from literature
  - `metadata/yt_title_cues`: *YouTube* identifiers (index) mapping to cue occurance in video title
  - `metadata/yt_descr_cues`: *YouTube* identifiers (index) mapping to cue occurance in video description
- `annotations`: set_ids from *SHS100K* and *YouTube* identifiers mapping to...
  - `annotations/mturk`:  ...*MTurk* annotations by multiple workers based on majority vote (minimum three judgements)
  - `annotations/expert`: ...expert annotations and comments
  - `annotations/staff`: ...staff annotations
  - `annotations/similarities`: ...aggregated similarity scores computed by *Ditto* and *Re-MOVE*
  - `annotations/yoho_music_ratio`: ...music ratios extracted based on *YOHO*
- `crawl`: 
  - `crawl/queries`: set_ids mapping to all our queries to *YouTube*
  - `crawl/SET_ID/re-move_preds`: N X N matrix of cosine similarities by *Re-MOVE* of N videos for set with `SET_ID`.
  - `crawl/SET_ID/videos`: N x M matrix of all N videos for set with `SET_ID` mapping to the query rank if occurring in each of M queries.
