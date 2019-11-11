function [t1, w_filtered] = readNFilterData()
    % Order of the moving averaging filter
    n = 5;

    % Read CSV data
    S_matrix = readtable('angVel1.csv');            % System response
    I_matrix = readtable('inputVelCurve.csv');      % Input

    % Separate the data in vectors and tranposes
    time1 = table2array(S_matrix(:,1)).';   % gets the time vector
    w = table2array(S_matrix(:,2)).';   % gets the phi1 vector
    
    % Doing the same but for the input of our system
    time2 = table2array(I_matrix(:,1)).';
    w2 = table2array(I_matrix(:,2)).';
    
    % Converting from miliseconds to seconds
    t1 = 0.001*time1;
    t2 = 0.001*time2;
    
    for i = n:length(w)
       w_filtered(i) = (w(i)+w(i-(n-4))+w(i-(n-3))+w(i-(n-2))+w(i-(n-1)))/n; 
    end
    
    % Filtering the input to check what is the velocity
    for i = n:length(w2)
       w2_filtered(i) = (w2(i)+w2(i-(n-4))+w2(i-(n-3))+w2(i-(n-2))+w2(i-(n-1)))/n; 
    end
    
    % Uncomment to check both filtered and unfiltered
    %hold on
    %plot(time, theta_filtered,'r');
    %grid on

    % Comparing the input graph, before and after filtering: (uncomment)
    %plot(t2,w2,'b');
    %hold on
    %plot(t2,w2_filtered,'r');
    
    
    % Another filtration if needed
    %for i = n:length(phi1_filtered)
    %   phi1_filtered1(i) = (phi1_filtered(i)+phi1_filtered(i-(n-4))+phi1_filtered(i-(n-3))+phi1_filtered(i-(n-2))+phi1_filtered(i-(n-1)))/n; 
    %end
    %hold on
    %plot(time,phi1_filtered1,'k');
end