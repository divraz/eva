# MobiNet V2 Training and Deployment on Serverless for Custom Dataset
- 88.14 % Accuracy

## Contents
- Serverless API Endpoint
- Data Collection
- Transfer Learning
- Data Augmentation
- Graphs
- Misclassified Images

## Serverless API Endpoint
- https://ie8mujag6h.execute-api.ap-south-1.amazonaws.com/dev/classify [POST]
	- Headers : 'content-type: multipart/form-data'
	- Body : Image file with empty key

## Data Collecction
- 21,500 images have been collected via group effort over four classes:
	- Flying Birds
	- Small QuadCopters
	- Large QuadCopters
	- Winged Drones
- Images here vary in size and type.
- Dataset is divided into train and validation set with ratio of 9:1

## Transfer Learning
- A MobileNet V2 model is picked up with pretrained weights.
```
model_ft = models.mobilenet_v2 (pretrained = True)
```
- Final Layer of Model changed to give out_features as 4 instead of 1000 (ImageNet)
```
model_ft.classifier[1] = torch.nn.Linear(in_features=model_ft.classifier[1].in_features, out_features=4)
```
- Converting to use GPU, and defining other parameters
```
model_ft = model_ft.to(device)
criterion = nn.CrossEntropyLoss()
optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)
```
- Finally Training for 25 epochs.
```
model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=25)
```

## Data Augmentation
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/d_aug.png)
- To solve the huge variation in image size, all image have been resized to 300, and then random crop of 224 x 224
- Augmentation techniques used:
	- rotation
	- horizontal and vertical flip
	- random erasing
- Pipeline for training set:
```
    'train': transforms.Compose([
        transforms.Resize(300),
        transforms.RandomRotation ([0, 180]),
        transforms.RandomCrop (224, pad_if_needed=True),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ToTensor(),
        transforms.RandomErasing (),
    ])
```
- Pipeline for validation set:
```
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
```
## Graphs
- Accuracy graph:
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/acc.png)
- Loss graphs:
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/loss.png)

## Misclassified Images
- Flying Birds
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/mis_birds.png)
- Large QuadCopters
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/mis_ltors.png)
- Small QuadCopters
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/mis_stors.png)
- Winged Drones
![](https://github.com/divyanshuraj6815/eva/blob/master/V2%20Experiment%202/images/mis_drones.png)
