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
r = 0.065; % wheel's diameter in meters
l = 0.1; % distance from the center base to the wheel%

comp1 = (r*phi1/2) + (r*phi2/2);
comp2 = zeros(1,n);
comp3 = (r*phi1/2*l) - (r*phi2/2*l);

for i = 1:n
    % Takes each component from the vector and does the matrix mult.
    vctr = [comp1(i) comp2(i) comp3(i)];
    vctr = vctr.';  % transpose
    output = Rot_matrix_inv*vctr;
    % extract just the values from omega (robot's velocity)
    omega = [omega output(3)];
end

vel_lin = 0.1*omega;
     

% criando variavel auxiliar pra encontrar o Ao
const = 0.35*ones(1,n);     % Regime permanente da saida
plot(t,const,'k')
hold on

% Reconstruct system response w/ 4.5V step
plot(t,omega,'r')
grid on


k = 0.35/54;                % 0.0065, 54 is the input velocity of the wheel
L = (10303-10180)/1000;     % 0.123s
upperlimit = 10951;

funcao = const - omega
tempo = (limiteinferior, step pra bater a mesma dimensao do omega)

lowerlimit = 
Ao = trapz(funcao,tempo);
% 3 parameter model approximation g3(s) = k/
T = Ao/k - L;
