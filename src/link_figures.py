#!/usr/bin/env python3

# Python standard library
from __future__ import print_function
import os, sys, base64

_help = """link_figures.py: Adds buttons/relative links to local images.
@Usage: 
    ./link_figures.py \\
        sample.chromoseq.tsv \\
        images_root_directory \\
    > sample.chromoseq.images.tsv

Add a new columns called "View" and "Local" to the sample's chromoseq 
report. The View column contains buttons to view each annotation variant 
in the report. If a variant does not have an image, then there will be 
no button for viewing. At the current moment, this script has handlers 
to link local images in the image_root_directory for the following 
types/classes of variants:
 - BND
 - DEL
 - DUP
 - INV

Handlers for more variant types/classes can be added by request. 

@Required Positional Arguments:
    [1]  Sample Chromoseq report, type: file.
    [2]  Relative or absolute path to the images directory, type: path.
         The image_root_directory is the directory containing both the 
         "samplot" and "plotting" directories.

@Example images_root_directory struture:
"/path/sample/results/" is an example images_root_directory. As you can 
see below, it is the base directory which contains both the "plotting" and 
"samplot" 
folders.

/path/sample/results/
    ├── sample.chromoseq.tsv
    ├── plotting
    │   ├── DEL_chr17_142355_15155141.png
    │   ├── DEL_chr7_102457574_152407149.png
    │   ├── DEL_chr7_152408466_159331838.png
    │   ├── DEL_chr9_203751_20385694.png
    │   ├── DEL_chr9_68417082_92137939.png
    │   ├── DUP_chr3_126806258_162793355.png
    │   ├── DUP_chr3_162908546_198118671.png
    │   ├── DUP_chr8_212369_43936239.png
    │   ├── DUP_chr8_45971871_145072660.png
    │   └── NR08_S1.genomePlot.png
    └── samplot
        ├── BND_chr11_118484498_chr9_20385759.png
        ├── BND_chr1_116377720_chr21_42725018.png
        ├── BND_chr11_49953211_chrX_10410866.png
        ├── BND_chr1_22102933_chrX_22453669.png
        ├── DEL_chr17_142355_15155141.png
        ├── DEL_chr7_102457574_152407149.png
        ├── DUP_chr3_126806258_162793355.png
        ├── DUP_chr8_45971871_145072660.png
        ├── INV_chr13_26759066_30519315.png
        ├── INV_chr13_30132829_33488254.png
        └── INV_chr6_24804833_34375955.png

@Example command:
Given this directory structure and an here is an example command:
    $ ./link_figures.py \\
          /path/sample/results/sample.chromoseq.tsv \\
          /path/sample/results/ \\
        > /path/sample/results/sample.chromoseq.linked.tsv
"""

button_template = '<a class="btn btn-primary" href="__uri__" target="_blank" role="button">__type__</a>'


def err(*message, **kwargs):
    """Prints any provided args to standard error.
    kwargs can be provided to modify print functions 
    behavior.
    @param message <any>:
        Values printed to standard error
    @params kwargs <print()>
        Key words to modify print function behavior
    """
    print(*message, file=sys.stderr, **kwargs)


def fatal(*message, **kwargs):
    """Prints any provided args to standard error
    and exits with an exit code of 1.
    @param message <any>:
        Values printed to standard error
    @params kwargs <print()>
        Key words to modify print function behavior
    """
    err(*message, **kwargs)
    sys.exit(1)


def index(linelist, columns):
    """Finds the index of each value listed in columns.
    @param linelist list[<str>]:
        Line split on its delimeter
    @params columns list[<str>]:
        Column names to index
    @return indices dict[<str>] = <int>:
        Dictionary containing the index of each col name
    """
    indices = {}
    missing = []
    for col in columns:
        try:
            i = linelist.index(col)
            indices[col] = i
        except ValueError as e:
            # Column is missing,
            # error out later to
            # see if anyother cols
            # are missing
            err("Error: Missing a required column... {}".format(col))
            missing.append(col)

    # Return errors if present
    if missing:
        fatal("Fatal: Missing the following required columns:\n\t-{}".format(
                missing 
            )
        )

    return indices


def convert2base64(file):
    """Converts an image into base64.
    This function returns a base64 representation of an 
    image so it can be directly embedded in HTML. Please 
    note that PDF cannot be encoded as base64; however 
    other filetype work fine.
    @param file <str>: 
        Path to file to encode as base64.
    @returns dataurl <str>:
        Url containing a base64 converted image
    """
    # Browsers cannot handle base64
    # converted PDFs
    ext = file.split('.')[-1]
    assert ext.lower() != 'pdf'
    
    # Covert the image into base64
    binary_file = open(file, 'rb').read() 
    base64_string = base64.b64encode(binary_file).decode('utf-8')
    
    # Create a URL with the base64
    # string representation of the image
    dataurl = 'data:image/{0};base64,{1}'.format(ext, base64_string)
    
    return dataurl


if __name__ == '__main__':

    # Input chromseq SV results
    try:
        input_file = sys.argv[1]
        image_base = sys.argv[2]
    except IndexError:
        # No input file provided
        fatal(_help)

    # Add links to local images
    with open(input_file, 'r') as fh:
        # Index file header to extract
        # column information by name
        header = next(fh).rstrip().split('\t')
        new_header = header
        col2index = index(
            header, 
            ['Chromoseq_SV_Type', 'Chrom', 'Start', 'End', 'ALT']
        )
        # Add new columns for local
        # paths to images and HTML
        # buttons to local images
        new_header.insert(1, 'View')
        new_header.append('Local')
        print('\t'.join(new_header)) 

        for line in fh:
            # Extract pieces of information
            # that make up filename for each 
            # different type of figures 
            linelist = line.rstrip().split('\t')
            sv_type = linelist[col2index['Chromoseq_SV_Type']]
            chrom   = linelist[col2index['Chrom']]
            start   = linelist[col2index['Start']]
            stop    = linelist[col2index['End']]
            alt     = linelist[col2index['ALT']]
            plots = []  # placeholder to resolve multiple plots
            html  = []  # placeholder to resolve links to plots
            if sv_type.lower() == 'del' or sv_type.lower() == 'dup':
                # DEL and DUP SVs have two plots
                # example: samplot/DEL_chr9_68417082_92137939.png
                plots.append(
                    os.path.join(
                        'samplot',
                        '{}_{}_{}_{}.png'.format(
                            sv_type,
                            chrom,
                            start,
                            stop
                        )
                    )
                )
                # add second plot path
                # example: plotting/DEL_chr9_68417082_92137939.png
                plots.append(
                    os.path.join(
                        'plotting',
                        '{}_{}_{}_{}.png'.format(
                            sv_type,
                            chrom,
                            start,
                            stop
                        )
                    )
                )
            elif sv_type.lower() == 'bnd':
                # BND has one plot,
                # had ALT position in filename
                # example: BND_chr11_49953211_chrX_10410866.png
                # grab position from.......................... A[chrX:22453669[G
                achrom = alt.split(':')[0]                    # A[chrX
                achrom = achrom.split('[')[-1].split(']')[-1] # chrX
                alt = alt.split(':')[-1]                      # 22453669[G
                alt = alt.split('[')[0].split(']')[0]         # 22453669
                plots.append(
                    os.path.join(
                        'samplot',
                        '{}_{}_{}_{}_{}.png'.format(
                            sv_type,
                            chrom,
                            start,
                            achrom,
                            alt
                        )
                    )
                )
            else:
                # Remaining SVs: INV
                # example: INV_chr6_24804833_34375955.png
                plots.append(
                    os.path.join(
                        'samplot',
                        '{}_{}_{}_{}.png'.format(
                            sv_type,
                            chrom,
                            start,
                            stop
                        )
                    )
                )
            
            # Check if plot exists and 
            # filter out any plots that 
            # were not created, maybe 
            # add a warning later if a
            # local image is not found
            plots = [plt for plt in plots if os.path.exists(os.path.join(image_base,plt))]
            # Create bootstrap buttons that
            # act as links to local plots
            html  = [
                button_template.replace('__uri__', plt).replace('__type__', 'CN plot')
                    if 'plotting' in plt else button_template.replace('__uri__', plt).replace('__type__', 'SV plot')
                for plt in plots
            ]
            # Add plots and HTML button to
            # the existing SV results
            linelist.insert(1, ' '.join(html))
            linelist.append(' '.join(plots))
            print('\t'.join(linelist))
