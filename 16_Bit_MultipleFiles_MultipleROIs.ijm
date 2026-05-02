macro "ROI Extraction - Multiple Files" {

    outputDir = getDirectory("Choose output folder");

    if (outputDir == "") {
        exit("No folder selected. Macro cancelled.");
    }

    totalImages = nImages();

    for (img = 1; img <= totalImages; img++) {

        selectImage(img);

        run("16-bit");
        run("Sharpen");
        run("8-bit");

        FileName = getInfo("image.filename");

        dotIndex = lastIndexOf(FileName, ".");
        if (dotIndex > 0) {
            baseName = substring(FileName, 0, dotIndex);
        } else {
            baseName = FileName;
        }

        maxROIs = getNumber("Maximum number of ROIs to extract for " + baseName + "?", 2);

        for (i = 1; i <= maxROIs; i++) {

            setTool("polygon");

            waitForUser(
                "Select ROI " + i + " for " + baseName,
                "Draw ROI " + i + ", then click OK.\n\nClick OK without selecting a ROI to stop this image."
            );

            if (selectionType() == -1) {
                break;
            }

            roiManager("Add");

            lastROI = roiManager("count") - 1;
            roiManager("Select", lastROI);

            roiStructure = getString(
                "Which structure are you selecting for ROI " + i + "?",
                "ROI" + i
            );

            roiName = baseName + "_" + roiStructure;
            roiManager("Rename", roiName);

            run("Clear Outside");

            savePath = outputDir + roiName + ".tif";
            saveAs("Tiff", savePath);

            run("Undo");

            continueROI = getBoolean("Do you want to select another ROI for this image?");

            if (continueROI == 0) {
                break;
            }
        }

        continueImages = getBoolean("Do you want to run the macro on the next open image before saving all ROIs?");

        if (continueImages == 0) {
            break;
        }
    }

    roiCount = roiManager("count");

    if (roiCount > 0) {
        roiZipPath = outputDir + "All_Selected_ROIs.zip";
        roiManager("Save", roiZipPath);
        print("Saved all ROI sets: " + roiZipPath);
    }

    print("ROI extraction complete.");
}