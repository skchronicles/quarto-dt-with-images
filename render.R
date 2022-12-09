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

# Generate HTML output
quarto::quarto_render(
    args$markdown,
    output_format = "html",
    output_file = args$output_filename,
    execute_dir = working_directory,
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
# be due to the version of pandoc installed
tmp <- file.rename(
    from = file.path(working_directory, args$output_filename),
    to = file.path(args$output_dir, args$output_filename)
)