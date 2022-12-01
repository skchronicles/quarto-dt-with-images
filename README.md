# quarto-dt-with-images

This is a proof of concept to bundle images within an R datatable. Images can be bundled within a DT in R; however, the image's container will take up the entire row's space. This means that the height of the row will be the height of the image. This is obviously not desirable.

Here are some possible solutions that have been implemented:
 - [ ] Add event listener for onClick events for the DT and open a lightbox, modal (bootstrap's modal), or image viewer (Viewer.js)
 - [X] Add a button in the DT that links to image, makes use of local images
 - [ ] Something that is a combination of the first two options

I have tried using quarto's lightbox plugin, and it does not play nice when used within a DT. It works fine outside of a DT though.
