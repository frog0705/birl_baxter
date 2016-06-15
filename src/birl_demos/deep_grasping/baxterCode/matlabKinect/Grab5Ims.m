PAUSE_TIME = 0.5;


%figure;
I=mxNiPhoto(KinectHandles); I=permute(I,[3 2 1]);
D=mxNiDepth(KinectHandles); D=permute(D,[2 1]);
%subplot(1,2,1),h1=imshow(I); 
%subplot(1,2,2),h2=imshow(D,[0 9000]); colormap('jet');

imFolder = 'kinectIms/';
    
for i = 1:5
    
    I=mxNiPhoto(KinectHandles); I=permute(I,[3 2 1]);
    D=mxNiDepth(KinectHandles); D=permute(D,[2 1]);
    mxNiUpdateContext(KinectHandles);
    %set(h1,'CDATA',I);
    %set(h2,'CDATA',D);
    
    imwrite(I,sprintf('%s/pcd%04dr.png',imFolder,imNum));
    imwrite(D,sprintf('%s/pcd%04dd.png',imFolder,imNum));
    
    imNum = imNum + 1;
    %drawnow;
    
    pause(PAUSE_TIME);
end
