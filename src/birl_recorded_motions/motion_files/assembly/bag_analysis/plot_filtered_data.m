% Load the data (assuming you are in the local folder .../motion_files/assembly/bag_analysis
load "arm_notmoving.mat"

% Get size of data and create an output structure of size two greater, with first two rows with the same value
[r,c]=size(wrench);
out=zeros(r+2,c);
out(1,:)=wrench(1,:);
out(2,:)=wrench(2,:);
out(3:r+2,:)=wrench(:,:);

% We also want to insert into wrench two rows that have the same value as the first row.
wrench=out;

% Get the size again
[r,c]=size(wrench);

 %---------------------------------------------------------------------------------------------------------
 % Low pass filter - 1st order
 % Follows the state-space variable form:
 % Xn+1= AXn + Bu
 % Y   = CXn + Bu
 %
 % Where Xn starts as zero.
 %
 % The variables A,B,C,D are obtained from Matlabs butter filter function using:
 % order: 1 and a cutoff frequencies. The best one yet is 0.05.
 %
 %   MATLAB
 %   1st Order Filter
 % cutoff freq: 0.500: A = 5.5511e-017, B=1.4142, C=0.3536, D=0.5;
 % cutoff freq: 0.250: A = 0.41420, B = 0.82840, C = 0.500, D=0.2929;
 % cutoff freq: 0.050: A = 0.85410, B = 0.20640, C = 0.6555, D=0.0730;
 % cutoff freq: 0.040: A = 0.88160, B = 0.16740, C = 0.66530, D = 0.05920
 % cutoff freq: 0.030: A = 0.90990, B = 0.12740, C = 0.67530, D = 0.04500
 % cutoff freq: 0.025  a = 0.9244,  b = 0.1069,  c =  0.6804, d = 0.0378
 % cutoff freq: 0,020  a = 0.9391,  b = 0.0862,  c = 0.6856,  d = 0.0305
 % cutoff freq: 0.010  a = 0.9691,  b = 0.0437,  c = 0.6962,  d = 0.0155
 %
 % 2nd order
 % cutoff freq: 0.05  a = 0.0055    0.0111    0.0055, b = 1.0000   -1.7786    0.8008
 % cutoff freq: 0.04  a = 0.0036    0.0072    0.0036, b = 1.0000   -1.8227    0.8372
 % cutoff freq: 0.03  a = 0.0021    0.0042    0.0021, b = 1.0000   -1.8669    0.8752
 %
 %   OCTAVE
 %   1st Order Filter
 %   cutoff freq 0.025: A = 0.92439, B = 0.72751, C = 0.10000, D = 0.037805
 %   cutoff freq 0.001: A = 0.96907, B = 0.30454, C = 0.10000, D = 0.037805
 % 
 % Main recursive 2nd order equation
 % out[i] = (a0%in[i]+a1%in_t1(i)+a2%in_t2(i)-b1%out_t1(i)-b2%out_t2(i))/b0;
 %
 % Cutoff = 0.2 (octave). For 2nd order filter octave results are almost identical to matlab;
 % a_1 =  0.067455; a_2 =  0.134911; a_3 =  0.067455; b_1 =  1.0000; b_2 = -1.14298; b_3 =  0.41280;
 % out[i] = 0.067455%in[i] + 0.134911%in_t1[i] + 0.067455%in_t2[i] + 1.14298%out_t1[i] - 0.41280%out_t2[i];
 %
 % Cutoff = 0.15 (octave). For 2nd order filter octave results are almost identical to matlab;
 % a_1 =  0.041254; a_2 =  0.082507; a_3 =  0.041254; b_1 =  1.0000; b_2 = -1.34897; b_3 =  0.51398;
 % out[i] = 0.041254%in[i] + 0.082507%in_t1[i] + 0.041254%in_t2[i] + 1.34897%out_t1[i] - 0.51398%out_t2[i];
 %
 % Cutoff = 0.1 (octave). For 2nd order filter octave results are almost identical to matlab;
 % a_1 =  0.020083; a_2 =  0.040167; a_3 =  0.020083; b_1 =  1.0000; b_2 = -1.56102; b_3 =  0.64135;
 % out[i] = 0.020083%in[i] + 0.040167%in_t1[i] + 0.020083%in_t2[i] + 1.56102%out_t1[i] - 0.64135%out_t2[i];
 %
 % Cutoff = 0.095; (%%% Currently using this one %%%)
 % a_1 =  0.018299; a_2 =  0.036598; a_3 =  0.018299; b_1 =  1.0000; b_2 = -1.58255; b_3 =  0.65574;
 % out[i] = 0.018299%in[i] + 0.036598%in_t1[i] + 0.018299%in_t2[i] + 1.58255%out_t1[i] - 0.65574%out_t2[i];
 %
 % Cutoff = 0.05;
 % a_1 =  0.0055; a_2 =  0.0111; a_3 =  0.0055; b_1 =  1.0000; b_2 = -1.7786; b_3 =  0.8008;
 % out[i] = 0.0055%in[i] + 0.0111%in_t1[i] + 0.0055%in_t2[i] + 1.7786%out_t1[i] - 0.8008%out_t2[i];
 %
 % cutoff freq: 0.03
 % a = 0.0021    0.0042    0.0021, b = 1.0000   -1.8669    0.8752
 % out[i] = 0.0021%in[i] + 0.0042%in_t1[i] + 0.0021%in_t2[i] + 1.8669%out_t1[i] - 0.8752%out_t2[i];
 %-------------------------------------------------------------------------------------------------------------------------
% Now run the 2nd order filter equation for all cols
for j=1:6 
    for i=3:r
        out(i,j)=0.018299*wrench(i,j)+0.036598*wrench(i-1,j)+0.018299*wrench(i-2,j)+1.58255*out(i-1,j)-0.65574*out(i-2,j);
    end
end

%  Plot the data
% Fx Axis
subplot(6,2,1),plot(wrench(:,1)); hold on
subplot(6,2,2),plot(out(:,1));

% Fy Axis
subplot(6,2,3),plot(wrench(:,2)); hold on
subplot(6,2,4),plot(out(:,2));

% Fz Axis
subplot(6,2,5),plot(wrench(:,3)); hold on
subplot(6,2,6),plot(out(:,3));

% Mx Axis
subplot(6,2,7),plot(wrench(:,4)); hold on
subplot(6,2,8),plot(out(:,4));

% My Axis
subplot(6,2,9),plot(wrench(:,5)); hold on
subplot(6,2,10),plot(out(:,5));

% Mz Axis
subplot(6,2,11),plot(wrench(:,6)); hold on
subplot(6,2,12),plot(out(:,6));
                            
