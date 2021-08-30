%% COVID CT Scan Classifier

clc, clear, close all;

%% Visualize Data

fprintf('Loading and Visualizing Data ...\n\n');

cv1=imageDatastore('archive\Face Mask Dataset\Train\Train_WithMask');
cv2=imageDatastore('archive\Face Mask Dataset\Train\Train_WithoutMask');
rawPos = readall(cv1);
rawNeg = readall(cv2);

% Clean the data set
index=1;
while index < 100
    if size(rawPos{index}, 3) ~= 3 % Remove images that do not have 3 layers
        rawPos(index) = [];
    else
        rawPos{index} = imresize(rawPos{index}, [227,227]); % Resize images to 227x227
        index = index + 1;
    end
end
index=1;
while index < 100
    if size(rawNeg{index}, 3) ~= 3
        rawNeg(index) = [];
    else
        rawNeg{index} = imresize(rawNeg{index}, [227,227]);
        index = index + 1;
    end
end

% Display randomly selected images
randvec=randi(length(rawNeg),[1,16]);
figure;
for i=1:length(randvec)
    subplot(length(randvec)/4,length(randvec)/4,i);
    imshow(rawNeg{randvec(i)});
    sgtitle('Without Mask');
end

randvec2=randi(length(rawPos),[1,16]);
figure(2);
for i=1:length(randvec2)
    subplot(length(randvec2)/4,length(randvec2)/4,i);
    imshow(rawPos{randvec2(i)});
    sgtitle('With Mask');
end

%% Assess and Report Network Accuracy

testData = imageDatastore('archive\Face Mask Dataset\Test', 'IncludeSubfolders', true, 'LabelSource', 'foldernames');
load('resnet.mat');
netimg=imread('resnet-50.png');
imshow(netimg);
title('ResNet-50');

fprintf('Running test data on resnet...\n\n');
nn_accuracy = zeros(1,1); % Preallocate

testData.ReadFcn=@(loc) imresize(imread(loc),[227,227]);

predictions = classify(trainedNetwork_1,testData);
testLabels = testData.Labels;
nn_accuracy = mean(predictions == testLabels);

log_ar = predictions==testLabels;
figure(2);
for i=1:length(log_ar)
    if log_ar(i)== 0
        bad = readimage(testData,i);
        imshow(bad)
        title(cellstr(predictions(i)));        
        pause;
        clf(figure(2))
    end
    
end
close(figure(2));

fprintf("The accuracy of ResNet-50 is %.2f[%%] \n",100*nn_accuracy);

figure;
nn_string = "ResNet-50";
xxs = categorical(nn_string);
xxs = reordercats(xxs,nn_string);
bar(xxs,nn_accuracy*100);
ylabel('Accuracy [%]');
ylim([0,100])

			

%% Classify an CT Image

fprintf('Select a test image.\n\n');
imagePath = imgetfile;
testImage = imread(imagePath);

figure;
imshow(testImage);
title('Classifying...');
pred=categorical({});

pred = predict(trainedNetwork_1,imresize(testImage,[227, 227]),'ReturnCategorical',true);

res = categories(pred);
if length(res) == 1
    title(res);
    name=res;
else
    freq = countcats(pred);
    if freq(1) > freq(2)
        title(res{1});
        name=res{1};
    else
        title(res{2});
        name=res{2};
    end
end

x=[];
for i=1:length(pred)
    if pred(i)=='WithMask'
        x(i)=1;
    else
        x(i)=0;
    end
end


%saveresults(name);
