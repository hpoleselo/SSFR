% Import t vector from time from the readings in order to reconstruct 
% The rotation matrix will always be constant in our application
% Since the global frame doesn't matter
theta = pi/2;
n = 4;
omega = [];
Rot_matrix_inv = [cos(theta) -sin(theta) 0; sin(theta) cos(theta) 0; 0 0 1];
r = 1; % wheel's diameter in meters
%phi1 = 0.9; % velocity read from sensor from wheel 1
%phi2 = -0.9; % velocity read from sensor from wheel 2
l = 1; % distance from the center base to the wheel%
phi1 = [1 2 3 4];
phi2 = [-1 -2 -3 2];

comp1 = (r*phi1/2) + (r*phi2/2);
% Nao sei se precisa gerar um comp2 com 0 de mesma dimensao que os outros
% comp para realizar a operacao matricial
comp2 = [0 0 0 0];
comp3 = (r*phi1/2*l) - (r*phi2/2*l);

for i = 1:n
    % Takes each component from the vector and does the matrix mult.
    vctr = [comp1(i) comp2(i) comp3(i)];
    vctr = vctr.';  % transpose
    output = Rot_matrix_inv*vctr;
    % extract just the values from omega (robot's velocity)
    omega = [omega output(3)];
end

display(omega);

% Reconstruct system response w/ 3.5V step
%plot(omega,t)
