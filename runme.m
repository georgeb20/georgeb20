%% COVID CT Scan Classifier

clc, clear, close all;

%% Visualize Data

fprintf('Loading and Visualizing Training Data ...\n\n');

%creating an imageDataStore to hold the WithMask and WithoutMask training
%sets

cv1=imageDatastore('archive\Face Mask Dataset\Train\WithMask');
cv2=imageDatastore('archive\Face Mask Dataset\Train\WithoutMask');

%create vector to pull 16 random test images from cv1
randvec=randi(length(cv1.Files),[1,16]);
%plot random image vector on a subplot
figure;
for i=1:length(randvec)
    subplot(length(randvec)/4,length(randvec)/4,i);
    imshow(readimage(cv1,i));
    sgtitle('Without Mask');
end

%create vector to pull 16 random test images from cv2
randvec2=randi(length(cv2.Files),[1,16]);
%plot random image vector on a subplot
figure(2);
for i=1:length(randvec2)
    subplot(length(randvec2)/4,length(randvec2)/4,i);
    imshow(readimage(cv2,i));
    sgtitle('With Mask');
end

%% Assess and Report Network Accuracy

%create imageDataStore to hold testData
testData = imageDatastore('archive\Face Mask Dataset\Test', 'IncludeSubfolders', true, 'LabelSource', 'foldernames');


fprintf('Running test data on resnet...\n\n');
load('squeezenet');

%resize test data to fit squeezenet (227,227)
testData.ReadFcn=@(loc) imresize(imread(loc),[227,227]);

%classify testData using the network
predictions = classify(trainedNetwork_1,testData);

%get labels for the data
testLabels = testData.Labels;

%logical array of correct predictions 
log_ar = predictions==testLabels;

%accuracy = average of correct predictions 
nn_accuracy = mean(log_ar);


fprintf("Press enter to step through wrong predictions.\n");

%step through the zeros (incorrect predictions) in the results
figure(3);
for i=1:length(log_ar)
    if log_ar(i)== 0
        bad = readimage(testData,i);
        imshow(bad)
        title(cellstr(predictions(i)));        
        pause;
        clf(figure(3))
    end
    
end

close(figure(3));

fprintf("The accuracy of the network is %.2f[%%] \n",100*nn_accuracy);
%% Classify an CT Image

fprintf('Select a test image.\n\n');

%get path of selected file and read the image
imagePath = imgetfile;
testImage = imread(imagePath);

%predict the test image,resize test image to fit nn
pred = classify(trainedNetwork_1,imresize(testImage,[227, 227]));

%show test img with prediction
figure(4);
imshow(testImage);
title(cellstr(pred));        

