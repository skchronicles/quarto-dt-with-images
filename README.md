# quarto-dt-with-images

<img width="1040" alt="image" src="https://user-images.githubusercontent.com/18038345/227644659-c4314a3b-12d7-40a9-97af-f813d28c4a19.png">



This is a proof of concept to bundle images within an R datatable. Images can be bundled within a DT in R; however, the image's container will take up the entire row's space. This means that the height of the row will be the height of the image. This is obviously not desirable. An example interactive report can be found [here](https://www.sudosight.com/quarto-dt-with-images/). 

Here are some possible solutions that have been implemented:
 - [ ] Add event listener for onClick events for the DT and open a lightbox, modal (bootstrap's modal), or image viewer (Viewer.js)
 - [X] Add a button in the DT that links to image, makes use of local images
 - [ ] Something that is a combination of the first two options

I have tried using quarto's lightbox plugin, and it does not play nice when used within a DT. It works fine outside of a DT though.

### Create interactive report

```bash
# Step 0. Load dependencies:
# python3 (>=3.5), quarto-cli, 
# R/4.X, R-quarto, R-rmarkdown,
# R-DT, R-argparse, R-knitr
module load R/4.2.2
export R_LIBS_USER=/data/OpenOmics/dev/R/%v/library
export PATH="/data/OpenOmics/dev/quarto-1.2.475/bin:$PATH"

# Step 1. Add figure information 
# to chromoseq output file, links
# each SV event to its local image
./src/link_figures.py \
  data/sample.chromoseq.tsv \
  data/ \
> data/input.example.tsv

# Step 2. Render Report with links
# to local figures for each SV in 
# a searchable, interactive datatable   
Rscript render.R \
    -m datatable_images.qmd \
    -i data/input.example.tsv \
    -o data/ \
    -f sample.chromoseq.html \
    -t "Example Sample SV Report" \
    -g data/plotting/sample.genomePlot.png

# The resulting HTML file will be in
# folder specified by the -o option.
# The HTML file uses relative links
# to images, as so, it is important 
# maintain the file structure defined
# below. To send the resulting report,
# you will need to create a tarball of
# the html report and its images. You 
# to this with the following command.
files=$(
  awk -F '\t' '{print $NF}' data/input.example.tsv \
    | sed '/^$/d' \
    | tail -n+2 \
    | tr '\n' ' ' \
    | tr -d '\n'
)
tar -zcf sample_chromoseq_report.tar.gz \
  input.example.tsv \
  sample.chromoseq.html \
  $files \
  -C data/
```

Images are not embedded in HTML due to file size constraints. As so, the resulting HTML file expects images to be in their respective `plotting` and `samplot` folders relative to the HTML report. 

Here is an example folder structure for a sample:
```text
NR08_S1
  ├── NR08_S1.chromoseq.html
  ├── plotting
  │     ├── DEL_chr17_142355_15155141.png
  │     ├── DEL_chr7_102457574_152407149.png
  │     ├── DEL_chr7_152408466_159331838.png
  │     ├── DUP_chr7_97442634_102457574.png
  │     ├── DUP_chr8_212369_43936239.png
  │     ├── DUP_chr8_45971871_145072660.png
  │     └── NR08_S1.genomePlot.png
  └── samplot
        ├── BND_chr11_118484498_chr9_20385759.png
        ├── BND_chr11_49953211_chrX_10410866.png
        ├── BND_chr13_21854176_chr9_137925802.png
        ├── BND_chr17_748658_chr3_126802227.png
        ├── BND_chr1_116377720_chr21_42725018.png
        ├── BND_chr1_22102933_chrX_22453669.png
        ├── BND_chr1_62836730_chr9_6627124.png
        ├── INV_chr13_30132829_33488254.png
        └── INV_chr6_24804833_34375955.png
```

> _**Please note**_: If you want to send someone the results/report, please create a ZIP file or tarball of the entire directory!
