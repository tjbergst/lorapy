BWval = [10.4e3, 15.6e3, 0, 0, 0, 0, 125e3,250e3,500e3];
filename = 'LoRa_Recording_OTA/Location0/lora_BW9_SF10_915MHz_1Msps_L0.dat';

BW = str2double(filename(37));% Gives a character
BW = BWval(BW);
SF = str2double(filename(41:42));

s = read_complex_binary(filename);
sN = abs(real(s(10e3:length(s))));
Fs = 1e6;
%numSymbols = 8;

sampPerSym = round(((2^SF)/BW)*Fs);
pcktLen = round(30.2*sampPerSym);

th = 0.4e-3;
% sN = normalize(real(s), 'center', 'median');
% 
% for i=1:length(sN)
%     if sN(i) > th
%         sN(i) = ceil(sN(i));
%     elseif sN(i) < -th
%         sN(i) = floor(sN(i));
%     else
%         sN(i) = 0;
%     end
% end


N = 17e3;
index = [0];
for i=1:length(sN)
    (sN(i))
    if sN(i) > th
        if sN(i+1) <= th % End of Packet
            if i-index(end) >= pcktLen*0.7 
                index = [index, i];
            end
        end
    elseif sN(i) <= th
        if sN(i+1) > th % Start of Packet
            if i-index(end) > N
                index = [index, i];
            end
        end
    end
end