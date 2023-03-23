#!/usr/bin/env Rscript

# USAGE: Renders Quarto markdown into HTML file
# Rscript render.R \
#     -m datatable_images.qmd \
#     -i data/input.example.tsv \
#     -o "$PWD" \
#     -f sample.chromoseq.html \
#     -t "Sample SV Report"

library(argparse)
library(quarto)
library(rmarkdown)


# Helper functions
err <- function(...) {
    # Print to standard error
    cat(sprintf(...), sep = "", file = stderr())
}

fatal <- function(...) {
    # Print to standard error and exit
    err(...); quit(status = 1)
}

this_is_the_way <- function(fp, type) {
    # Something, something, something... The Mandalorian!
    # Given a file or directory, it will convert a relative
    # path into an absolute path.
    # @param fp <chr>: file or path to convert
    # @param type <enum {"file"|"dir"}>: fp's type, either file or dir
    # @return abspath <chr>: Absolute path of file/directory
    abspath <- fp
    if (type == "directory" || type == "dir") {
        # Assume it's a directory/folder,
        # join abs path of fp with its
        # basename
        abspath <- normalizePath(fp)
    } else if (type == "file") {
        abspath <- file.path(
            normalizePath(dirname(fp)),
            basename(fp)
        )
    } else {
        fatal(
            "type: %s is not supported! Select either: 'file' or 'dir'.",
            type
        )
    }
    return(abspath)
}

here <- function() {
    # Gets the absolute path of this script
    args <- commandArgs(trailingOnly = FALSE)
    # Parses the file option
    # from cli args to get the
    # path of the current script
    needle <- "--file="
    match <- grep(needle, args)
    if (length(match) > 0) {
            # Was run from Rscript
            return(
                this_is_the_way(sub(needle, "", args[match]), "dir")
            )
    } else {
            # Was 'source' via R console
            return(
                this_is_the_way(sys.frames()[[1]]$ofile, "dir")
            )
    }
}


# Create arg parser
parser <- ArgumentParser(description = "Renders Quarto markdown into HTML file")

# Quarto markdown file
# to render into HTML
parser$add_argument(
    "-m", "--markdown",
    type = "character",
    required = TRUE,
    help = "Required File: Quarto rmarkdown file to render."
)

# Input file, SV results
parser$add_argument(
    "-i", "--input_file",
    type = "character",
    required = TRUE,
    help = "Required File: Input SV results."
)

# Input file, Genome-wide Plot
parser$add_argument(
    "-g", "--genome_plot",
    type = "character",
    required = TRUE,
    help = "Required Image: Input genome-wide plot."
)

# Output directory
parser$add_argument(
    "-o", "--output_dir",
    type = "character",
    required = TRUE,
    help = "Required Path: Output directory to write report."
)

# Output HTML Filename
parser$add_argument(
    "-f", "--output_filename",
    type = "character",
    required = FALSE,
    default = "datatable_images.html",
    help = "Optional: Name of output report, default: 'datatable_images.html'."
)

# Display sample names
parser$add_argument(
    "-t", "--title",
    type = "character",
    default = "SV Report",
    help = "Optional: Set report title, default: 'SV Report'."
)

# Parse cli args
args <- parser$parse_args()

# Convert any relative paths
# that may have been provided 
# to absolute paths
args$markdown <- this_is_the_way(args$markdown, "file")
args$input_file <- this_is_the_way(args$input_file, "file")
args$genome_plot <- this_is_the_way(args$genome_plot, "file")
args$output_dir <- this_is_the_way(args$output_dir, "dir")
args$output_filename <- basename(args$output_filename)

# Get current working directory
# to setwd() of rmarkdown, else
# paths must be absolute, this
# allows for relative paths to
# this script 
working_directory <- getwd()

# Create output directory
if (!dir.exists(file.path(args$output_dir))) {
    # if it does not exist
    dir.create(
        file.path(args$output_dir),
        showWarnings = FALSE
    )
}

# There is a bug/issue with quarto
# where if you are rendering the
# HTML file in another directory
# other than where the QMD file
# exists, it will not embed the
# css/js correctly, as so, I am
# copying over the QMD file, the
# input file, and genome plot to 
# a temp directory to render every-
# thing there, and then moving the 
# output file back into its correct
# user defined location, the joys of
# untested software!
tmp <- tempdir() 
t <- file.copy(args$markdown, tmp)
t <- file.copy(args$input_file, tmp)
t <- file.copy(args$genome_plot, tmp)
setwd(tmp)


# Generate HTML output
quarto::quarto_render(
    basename(args$markdown),
    output_format = "html",
    output_file = args$output_filename,
    execute_dir = tmp,
    execute_params = list(
        input_file = args$input_file,
        genome_plot = args$genome_plot
    ),
    pandoc_args = rmarkdown::pandoc_metadata_arg("title", args$title)
)

# Quarto cannot render an `output_file`
# that contains a path :(, this is part
# of the reason this wrapper exists, also
# `output_dir` also does not work, it may
# be due to the version of pandoc installed,
# must use file.copy instead of file.rename
# because temp_dir could be on another file-
# system/device (which is the case on Biowulf).
t <- file.copy(
    from = file.path(tmp, args$output_filename),
    to = file.path(args$output_dir, args$output_filename),
    overwrite = TRUE
)