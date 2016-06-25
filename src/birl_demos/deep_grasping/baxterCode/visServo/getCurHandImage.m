% Reads an image taken from Baxter's hand camera
% Assumes that we're dumping hand images to ~/.ros/frame*.jpg
% Takes the second-latest image from that directory (to make sure we don't
% take a half-written image)
% Here, 'latest' is determined by file ordering, for speed. Since the ROS
% image-dumping code pads with zeros to four digits, passing 9999 will
% cause this code to continually return image 9999 instead.

function I = getCurHandImage()

IMG_DIR = '~/.ros/';

imgFiles = dir(sprintf('%s/frame*.jpg',IMG_DIR));

myFile = imgFiles(end-1).name;
myFile = sprintf('%s/%s',IMG_DIR,myFile);

I = imread(myFile);

