% phi1,phi2 are the spinning speed from the wheels 1 and 2

% Reading our filtered data
[t, phi1] = readAndFilterData();

% Has to be the opposite in order to rotate on its own axis
phi2 = -phi1;

% Import t vector from time from the readings in order to reconstruct 
% The rotation matrix will always be constant in our application
% Since the global frame doesn't matter
theta = 0;
n = length(phi1);
omega = [];
Rot_matrix_inv = [cos(theta) -sin(theta) 0; sin(theta) cos(theta) 0; 0 0 1];
r = 0.065;                  % Wheel's diameter in meters
l = 0.1;                    % Distance from the center base to the wheel

comp1 = (r*phi1/2) + (r*phi2/2);
comp2 = zeros(1,n);
comp3 = (r*phi1/2*l) - (r*phi2/2*l);

for i = 1:n
    % Takes each component from the vector and does the matrix mult.
    vctr = [comp1(i) comp2(i) comp3(i)];
    vctr = vctr.';           % Transpose
    output = Rot_matrix_inv*vctr;
    % Extract just the values from omega (robot's velocity)
    omega = [omega output(3)];
end

%vel_lin = 0.1*omega;
     

% Reconstruct system response w/ 4.5V step
plot(t,omega,'r')
grid on

% Three parameter model approximation G3(s) = e^-Ls*k/Ts+1
y_infinite = 0.35;           % Steady state value
k = y_infinite/54;           % 0.0065, 54 is the input velocity of the wheel
L = 10.303-10.180;           % 0.123s

% Helping function to calculate the Ao, where T2 = Ao/y_inf - L
hold on
const = 0.35*ones(1,n);      % Steady state of our system
plot(t,const,'k')


resultant = const - omega;   % Area between both curves
lowerLimit = 10.180;         % Where the curves start
upperLimit = 10.9506;        % Was chosen with ginput(1) on the graph
tForIntegration = linspace(lowerLimit,upperLimit,n);
Ao = trapz(tForIntegration,resultant);
T1 = Ao/y_infinite - L; % checar area, depois q mudei a escala de t, mudou

% Another approximation for the time response T (tAB 63% from the y(inf))
% 0.63*y(inf) = 0.2205, then going to the graph with ginput(1) see which
% value we have for the time
T2 = 10.433 - 10.303;        % 10.433 foi pegando pelo ginput e 10.303 eh o atraso


% Another approximation for the time response T (tAC)

%num = [0.0065];
%den = [0.01599 0.253 1 0];
%g3 = tf(num,den);
%step(g3*54);




