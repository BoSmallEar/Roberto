import numpy as np
import matplotlib.pyplot as plt

'''
data = open('train_data.txt','r')
times = []
loss = []
rpn_class_loss = []
rpn_bbox_loss = []
mrcnn_class_loss = []
mrcnn_bbox_loss = []
mrcnn_mask_loss = []
val_loss = []
val_rpn_class_loss = []
val_rpn_bbox_loss = []
val_mrcnn_class_loss = []
val_mrcnn_bbox_loss = []
val_mrcnn_mask_loss = []
for i in range(20):
    dataline = data.readline().split()
    times.append(float(dataline[0]))
    loss.append(float(dataline[4]))
    rpn_class_loss.append(float(dataline[7]))
    rpn_bbox_loss.append(float(dataline[10]))
    mrcnn_class_loss.append(float(dataline[13]))
    mrcnn_bbox_loss.append(float(dataline[16]))
    mrcnn_mask_loss.append(float(dataline[19]))
    val_loss.append(float(dataline[4+18]))
    val_rpn_class_loss.append(float(dataline[7+18]))
    val_rpn_bbox_loss.append(float(dataline[10+18]))
    val_mrcnn_class_loss.append(float(dataline[13+18]))
    val_mrcnn_bbox_loss.append(float(dataline[16+18]))
    val_mrcnn_mask_loss.append(float(dataline[19+18]))
    
epochs = np.linspace(1,20,20).astype('int')
train = plt.plot(epochs,mrcnn_mask_loss,'r.',label='train')
val = plt.plot(epochs,val_mrcnn_mask_loss,'b.',label='validate')
plt.legend()
plt.title('Mask R-CNN mask loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.xticks(epochs)
plt.savefig('roberto_data_analysis/'+'mrcnn_mask_loss'+'.png')
'''

#paperball
'''
TP = [0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
TN = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FP = [3,1,0,0,0,0,1,0,1,6,2,0,0,1,1,1,5,0,0,0,0,0,1,0,0,0,0,0,0,0,2,1,0,0,2,1,0,0,0,0]
FN = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

TP = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
TN = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FP = [0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1]
FN = [0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
'''
TP = [0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
TN = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FP = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FN = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
'''
TP = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
TN = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FP = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FN = [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
'''
precision = np.zeros((40,1))
recall = np.zeros((40,1))

for i in range(40):
    if sum(TP[:i] + FP[:i]) == 0:
        precision[i] = 1
    else:
        precision[i] = sum(TP[:i]) / sum(TP[:i] + FP[:i])
        
    if sum(TP[:i] + FN[:i]) == 0:
        recall[i] = 1
    else:
        recall[i] = sum(TP[:i]) / sum(TP[:i] + FN[:i])
        
recall_sorted_id = np.argsort(recall.T)[0]
recall_sorted = recall[recall_sorted_id]
precision_sorted = precision[recall_sorted_id]
plt.plot(recall_sorted,precision_sorted)
plt.xlabel('recall')
plt.ylabel('precision')
plt.title('Paper ball precision vs. recall')
plt.savefig('roberto_data_analysis/improved_paperball_AP.png')

num = 0
left = 0
AP = 0
for right in range(1,40):
    if recall_sorted[right - 1] != recall_sorted[right]:
        num += 1
        AP += np.max(precision_sorted[left:right])
        left = right

AP += np.max(precision_sorted[left:])
AP /= num + 1
print(AP)