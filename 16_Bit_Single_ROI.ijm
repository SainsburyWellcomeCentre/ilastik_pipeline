macro "ROI Extraction" {
   run("16-bit");
   run("Sharpen");
   run("8-bit");
   setTool("polygon");
   waitForUser("Please select ROI now.", "Click OK after selecting ROI.");
   roiManager("Add");
   SelectLastROI = roiManager("count") - 1;
   FileName = getInfo("image.filename");
   roiManager("Select", SelectLastROI);
   roiStructure1= getString("Which structure are you selecting?", "");
   roiManager("Rename", roiStructure1);
   run("Clear Outside");
   saveAs("Tiff");
 
}