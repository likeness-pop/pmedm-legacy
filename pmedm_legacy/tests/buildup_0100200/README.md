# PUMA 0100200

## Limestone County – Alabama

* The data in this directory is pre-built for testing and can be regenerated with the script below.
* The path to your census API key may need to change.

```python
%load_ext watermark
%watermark

import pathlib

import geopandas
import likeness_vitals
import numpy
import pandas
import pmedm_legacy

import livelike

%watermark -w
%watermark -iv

key = likeness_vitals.vitals.get_censusapikey(pathlib.Path("..", "..", "livelike", ""))

# -- Limestone County – Alabama
puma_fips = "0100200"

pup = livelike.acs.puma(
    puma_fips,
    censusapikey=key,
    cache=True,
    target_zone="trt",
    make_trt_geo=True,
    keep_geo=True,
)

pandas.DataFrame(pup.wt, columns=["wt"]).to_parquet("wt.parquet")
pup.est_ind.to_parquet("est_ind.parquet")
pup.est_g1.to_parquet("est_g1.parquet")
pup.est_g2.to_parquet("est_g2.parquet")
pup.se_g1.to_parquet("se_g1.parquet")
pup.se_g2.to_parquet("se_g2.parquet")
pup.g1.to_frame().to_parquet("g1.parquet")
pup.g2.to_frame().to_parquet("g2.parquet")

pmd = pmedm_legacy.PMEDM(
    pup.year,
    pup.wt,
    pup.est_ind,
    pup.est_g2,
    pup.est_g1,
    pup.se_g2,
    pup.se_g1,
    g1=pup.g1,
    g2=pup.g2,
    tr_iter=50,
    tr_tol=1e-3,
)

pmd.solve()

pandas.DataFrame(pmd.pmedm_res["almat"]).to_parquet("almat.parquet")
```
