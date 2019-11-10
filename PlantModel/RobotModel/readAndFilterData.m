function [t, phi1_filtered] = readAndFilterData()
    % Order of the moving averaging filter
    n = 5;

    % Read CSV data
    S_matrix = readtable('angularVelCurve.csv');    % System response

    % Separate the data in vectors and tranposes
    time = table2array(S_matrix(:,1)).';   % gets the time vector
    phi1 = table2array(S_matrix(:,2)).';   % gets the phi1 vector
    
    % Converting from miliseconds to seconds
    t = 0.001*time;
    
    % Uncomment to check the original graph without filtering
    %plot(t,phi1,'b');

    for i = n:length(phi1)
       phi1_filtered(i) = (phi1(i)+phi1(i-(n-4))+phi1(i-(n-3))+phi1(i-(n-2))+phi1(i-(n-1)))/n; 
    end
    
    % Uncomment to check both filtered and unfiltered
    %hold on
    %plot(time, phi1_filtered,'r');
    %grid on

    % Another filtration if needed
    %for i = n:length(phi1_filtered)
    %   phi1_filtered1(i) = (phi1_filtered(i)+phi1_filtered(i-(n-4))+phi1_filtered(i-(n-3))+phi1_filtered(i-(n-2))+phi1_filtered(i-(n-1)))/n; 
    %end
    %hold on
    %plot(time,phi1_filtered1,'k');
end
