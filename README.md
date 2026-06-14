\# Primer PICKR Database



This repository contains the literature-mined RT-qPCR primer dataset that powers \[primerpickr.com](https://www.primerpickr.com/). It is the companion data release for:



> Molley, T.G., Banerjee, A., Balayan, A. \*et al.\* Primer PICKR: literature-mined scoring platform for robust RT–qPCR primers. \*Nat Commun\* (2026). https://doi.org/10.1038/s41467-026-73648-2



\## What's here



\- `csv/scored/scored\_<species>/<GENE>.csv` — one CSV per gene per species, containing all primer pairs scored by the PICKR algorithm

\- 40 species across mammals, vertebrates, invertebrates, plants, fungi, and bacteria

\- \~75,000 distinct (gene, species) combinations

\- \~550,000 scored primer pairs total



\## Species covered



| Group | Species |

|---|---|

| Mammals (10) | human, mouse, rat, monkey, pig, cow, dog, sheep, rabbit, hamster |

| Other vertebrates (4) | chicken, zebrafish, frog (X. laevis), medaka |

| Invertebrates (4) | fly (D. melanogaster), worm (C. elegans), honeybee, mosquito |

| Plants (9) | arabidopsis, rice, maize, wheat, soybean, tomato, potato, grape, barley |

| Fungi (2) | yeast (S. cerevisiae), spombe (S. pombe) |

| Bacteria (11) | ecoli, bsubtilis, mtb, saureus, spneumoniae, kpneumoniae, paeruginosa, salmonella, listeria, cjejuni, hpylori |



\## CSV column reference



Each row is one scored primer pair (forward + reverse).



\*\*Sequences\*\*

\- `f\_sequence`, `r\_sequence` — primer DNA sequences (5' → 3')



\*\*Biophysics\*\*

\- `f\_Tm\_C`, `r\_Tm\_C` — melting temperature (°C)

\- `f\_GC\_pct`, `r\_GC\_pct` — GC content (%)

\- `f\_self\_comp`, `r\_self\_comp` — self-complementarity score

\- `pair\_comp` — pair complementarity (dimer potential)



\*\*Literature evidence\*\*

\- `f\_pmcid\_list`, `r\_pmcid\_list` — PubMed Central IDs citing each primer

\- `f\_pmcid\_count`, `r\_pmcid\_count` — unique PMCID counts

\- `pair\_shared\_pmcid\_list` / `pair\_shared\_pmcid\_count` — papers citing both primers together

\- `f\_reg\_pmcid\_list`, `r\_reg\_pmcid\_list` — correct-orientation citations

\- `f\_inv\_pmcid\_list`, `r\_inv\_pmcid\_list` — reverse-complement citations



\*\*Scoring (0–1 subscores, 0–100 composite)\*\*

\- `evidence\_score` — literature-evidence component

\- `biophysics\_score` — biophysical-fit component

\- `synergy\_score` — bonus for pairs strong in both above

\- `pickr\_score` — final composite score (0–100)

\- `percentile` — percentile rank across all pairs in the database



\*\*Cross-specificity\*\* (off-target hits in the same transcriptome)

\- `f\_cross\_specificity\_0` … `f\_cross\_specificity\_4` — perfect-match through 4-mismatch hits

\- Corresponding `\_seq` columns hold the matched sequences



\*\*Position\*\*

\- `f\_match\_start`, `f\_match\_end`, `r\_match\_start`, `r\_match\_end` — transcript coordinates

\- `f\_orientation`, `r\_orientation` — strand orientation



The full scoring methodology is documented in the Nature Comms paper.



\## Quick examples



\### Python

```python

import pandas as pd



df = pd.read\_csv('csv/scored/scored\_human/GAPDH.csv')

top5 = df.nlargest(5, 'pickr\_score')\[\['f\_sequence', 'r\_sequence', 'pickr\_score']]

print(top5)

```



\### R

```r

library(readr)

df <- read\_csv("csv/scored/scored\_human/GAPDH.csv")

top5 <- head(df\[order(-df$pickr\_score), ], 5)

print(top5\[, c("f\_sequence", "r\_sequence", "pickr\_score")])

```



\### Bash

```bash

\# Top 3 highest-scoring pairs for human TP53 (column 60 = pickr\_score)

head -1 csv/scored/scored\_human/TP53.csv

sort -t, -k60 -rn csv/scored/scored\_human/TP53.csv | head -3

```



\## Citation



If you use this dataset in your work, please cite the Nature Communications paper:



```bibtex

@article{Molley2026PICKR,

&#x20; author  = {Molley, Thomas G. and Banerjee, Abhishek and Balayan, Anjelika and others},

&#x20; title   = {Primer PICKR: literature-mined scoring platform for robust RT-qPCR primers},

&#x20; journal = {Nature Communications},

&#x20; year    = {2026},

&#x20; doi     = {10.1038/s41467-026-73648-2}

}

```



\## License



This dataset is released under \*\*CC BY-NC-ND 4.0\*\*. See \[LICENSE](LICENSE) for full terms.



\- ✅ Use for research and non-commercial purposes

\- ✅ Cite in publications

\- ❌ Use for commercial purposes without permission

\- ❌ Redistribute modified versions



For commercial licensing, contact the corresponding author of the Nature Comms paper.



\## Interactive search



For the full interface with filters, sorting, and shortlist/CSV/IDT export, visit \*\*\[primerpickr.com](https://www.primerpickr.com/)\*\*.



\## Contact



Questions or commercial inquiries: see the corresponding author of the Nature Comms paper, or use the contact form at https://www.primerpickr.com/contact/.

