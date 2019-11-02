function [time, phi1_filtered1] = readAndFilterData()
    % Order of the moving averaging filter
    n = 10;

    % Read CSV data
    T_matrix = readtable('measurements1.csv');

    % Separate the data in vectors and tranposes
    time = table2array(T_matrix(:,1)).';   % gets the time vector
    phi1 = table2array(T_matrix(:,2)).';   % gets the phi1 vector
%     plot(time,phi1,'b');

    for i = n:length(phi1)
       phi1_filtered(i) = (phi1(i)+phi1(i-(n-4))+phi1(i-(n-3))+phi1(i-(n-2))+phi1(i-(n-1)))/n; 
    end

    %hold on
    %plot(time, phi1_filtered,'r');


    for i = n:length(phi1_filtered)
       phi1_filtered1(i) = (phi1_filtered(i)+phi1_filtered(i-(n-4))+phi1_filtered(i-(n-3))+phi1_filtered(i-(n-2))+phi1_filtered(i-(n-1)))/n; 
    end
%     hold on
%     plot(time,phi1_filtered1,'k');
end
