
% Read CSV data
S_matrix = readtable('pid2wdisturb2.csv');

% Separate the data in vectors and tranposes
time1 = table2array(S_matrix(:,1)).';   % gets the time vector
w = table2array(S_matrix(:,2)).';   % gets the phi1 vector
e = table2array(S_matrix(:,3)).';   % gets the error vector

% Converting from miliseconds to seconds
t1 = 0.001*time1;

for i = 1:length(w)
   e(i) = e(i)^2;   % Erro quadrático
end

sum_e_quad = sum(e);
disp('Quadratic error summation:');
display(sum_e_quad);

% Uncomment to check both filtered and unfiltered
%hold on
%plot(time, theta_filtered,'r');
%grid on