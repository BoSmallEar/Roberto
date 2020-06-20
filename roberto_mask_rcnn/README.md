# Roberto Mask R-CNN

## Instructions to Run
1. Download and setup from [Mask_RCNN](https://github.com/matterport/Mask_RCNN)
2. Run src/train_roberto.py to train the network. However we are not able to provide our own dataset on paper balls and clothes. You will need to configure your own dataset.
3. Run src/test_roberto.py to load the latest model we have trained in logs/objects20200423T2055 and evaluate images from images/trash_test. The way we generate all the images is introduced in section 2.
4. Run src/train_data_analysis.py to generate figures we use for section 4.3