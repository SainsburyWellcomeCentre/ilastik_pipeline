Ilastik Instructions

Segmentation
Load segmentation project (NLF_Segmentation or NLGF_Segmentation)

Check Export Settings on the Prediction Export tab:
Set source to 'Simple Segmentation'
On 'Choose Export Image Settings...' set format to numpy and specify your preferred export directory (by default ilastik will export to the folder containing the ROIs).

Add ROIs to the Batch Processing tab and click 'Process all files'


Percentage of Coverage Quantification
Load script (Percentage of Coverage Quantification)
Run script and provide 'brain' and 'region'. For example, if ilastik's simple segmentation outputs a file called 'ThioS_hTauNLF_M_1116530_S1_CTX_Simple Segmentation.npy', brain is 'hTauNLF_M_1116530' and region is 'CTX'.


Plaque Classification
Load segmentation project (NLF_Segmentation or NLGF_Segmentation)
Check Export Settings in the Prediction Export tab:
Set source to 'Probabilities'
On 'Choose Export Image Settings...', set format to hdf5 and specify your preferred export directory (by default ilastik will export to the folder containing the ROIs).

Load classification project (NLF_Plaque_Classification or NLGF_Plaque_Classification)
Ignore 'Export Image Settings'
On 'Configure Feature Table Export' set the export directory and choose which features you want to quantify.
In the batch processing tab, load the ROI TIFFs on 'Raw Data' and the corresponding Probabilities hdf5. Each ROI .tif must have a corresponding probability .hdf5 and the order of files must be the same.