# quarto-dt-with-images

This is a proof of concept to bundle images within an R datatable. Images can be bundled within a DT in R; however, the image's container will take up the entire row's space. This means that the height of the row will be the height of the image. This is obviously not desirable.

Here are some possible solutions that have been implemented:
 - [ ] Add event listener for onClick events for the DT and open a lightbox, modal (bootstrap's modal), or image viewer (Viewer.js)
 - [X] Add a button in the DT that links to image, makes use of local images
 - [ ] Something that is a combination of the first two options

I have tried using quarto's lightbox plugin, and it does not play nice when used within a DT. It works fine outside of a DT though.

### Create interactive report

```bash
# Add figure information 
# to chromoseq output file
./src/link_figures.py data/sample.chromoseq.tsv > data/input.example.tsv
# Render Report with links
# to local figures for SV  
quarto render datatable_images.qmd -o sample.chromoseq.html -P input_file:data/input.example.tsv -M title:"Sample SV Report"
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
