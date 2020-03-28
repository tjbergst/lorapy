
BWval = [10.4e3, 15.6e3, 0, 0, 0, 0, 125e3,250e3,500e3];
filename = 'LoRa_Recording_OTA/Location0/lora_BW9_SF11_915MHz_1Msps_L0.dat';

BW = str2double(filename(37));% Gives a character
BW = BWval(BW);
SF = str2double(filename(41:42));

s = read_complex_binary(filename);


Fs = 1e6;
lb = 12;
numSampsP = 17770;
numSymbols = 8;
N = length(s);



sampPerSym = round(((2^SF)/BW)*Fs);
pcktLen = round(30.2*sampPerSym);

padding = transpose(zeros(numSampsP,1));
th = 0.03;
sN = normalize(real(s));
for i=1:length(sN)
    if sN(i) > th
        sN(i) = ceil(sN(i));
    elseif sN(i) < -th
        sN(i) = floor(sN(i));
    else
        sN(i) = 0;
    end
end

k = strfind(transpose(sN(1:1e6)), padding);
%k = regexp(transpose(round(real(s))), padding, 'once');
s = s(k(1)+numSampsP:length(s));
l = 1;

data.IQ = [];
data.label = [];
for i=1:1:length(s)
    for j = 1:numSymbols
        sym = s(l:l+sampPerSym);
        l = l + sampPerSym;
        data.IQ = [data.IQ, sym];
        data.label = [data.label, lb];

    end
    
    if length(data.label) == 2800
        break 
    end
    
    if mod(length(data.label),100) == 0
        display(length(data.label));
    end
    
    l = l+(pcktLen-(numSymbols*sampPerSym));
    temp = sN(l:length(sN));
    l_temp = find(temp~=0,1,'first');
    if ~isempty(l_temp)
        l = l +l_temp(1);
    else
        display("Error");
    end
    %plot((real(sym)))
end


subplot(4,1,1);
plot(data.IQ(:,1));
subplot(4,1,1);
plot(data.IQ(:,100));
subplot(4,1,1);
plot(data.IQ(:,1000));
subplot(4,1,1);
plot(data.IQ(:,1250));