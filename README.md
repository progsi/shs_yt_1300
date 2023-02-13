# shs_yt_1300
This is the repository for the SHS-YouTube1300 dataset. A dataset of cover versions from YouTube.

HDF structure of `store_public.h5`:
- `metadata`
  - `metadata/shs100k`: the metadata from SHS100K
  - `metadata/version_cues`: version cues (eg. "remix", "cover") extracted from literature
  - `metadata/yt_title_cues`: YouTube identifiers (index) mapping to cue occurance in video title
  - `metadata/yt_descr_cues`: YouTube identifiers (index) mapping to cue occurance in video description
- `annotations`: set_ids from SHS100K and YouTube identifiers mapping to...
  - `annotations/mturk`:  ...MTurk annotations by multiple workers
  - `annotations/expert`: ...expert annotations and comments
  - `annotations/staff`: ...staff annotations
  - `annotations/similarities`: ...aggregated similarity scores computed by Ditto and Re-MOVE
  - `annotations/yoho_music_ratio`: ...music ratios extracted based on You-Only-Hear-Ones (YOHO)
- `crawl`: 
  - `crawl/queries`: set_ids mapping to all our queries to YouTube
  - `crawl/SET_ID/re-move_preds`: N X N matrix of cosine similarities by Re-MOVE of N videos for set with `SET_ID`.
  - `crawl/SET_ID/videos`: N x M matrix of all N videos for set with `SET_ID` mapping to the query rank if occurring in each of M queries.
