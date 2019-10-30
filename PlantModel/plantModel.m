% The rotation matrix will always be constant in our application
% Since the global frame doesn't matter
theta = pi/2;

Rot_matrix_inv = [cos(theta) -sin(theta) 0; sin(theta) cos(theta) 0; 0 0 1];
r = 1; % wheel's diameter
phi1 = 4; % velocity read from sensor from wheel 1
phi2 = 2; % velocity read from sensor from wheel 2
l = 1; % distance from the center base to the wheel

comp1 = (r*phi1/2) + (r*phi2/2);
comp2 = 0;
comp3 = (r*phi1/2*l) - (r*phi2/2*l);

vctr = [comp1 comp2 comp3];
% transpose
vctr = vctr.';

output = Rot_matrix_inv*vctr;
display(output);
