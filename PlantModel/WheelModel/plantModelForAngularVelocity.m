% Reading our filtered data
[t, w] = readNFilterData();

n = length(w);     

% Reconstruct system response w/ 30/255 from duty cycle
plot(t,w,'r')
grid on

%input vel 56 rad/s for 27% from the PWM
input = 4.92;                       % 4.92V ou 120 bits de 255 do pwm

% Three parameter model approximation G3(s) = e^-Ls*k/Ts+1
y_infinite = 69.66;                % Steady state value, we checked from the grph
k = y_infinite/input;
L = 0.2030 -0.0504;                % 0.1526s

% Helping function to calculate the Ao, the area between both curves
hold on
const = y_infinite*ones(1,n);      % Steady state of our system
plot(t,const,'k')

resultant = const - w;           % Area between both curves
lowerLimit = 0.0504;             % Where the curves start
% When  the system reaches the steady state
upperLimit = 1.3028;               % Was chosen with ginput(1) on the graph
tForIntegration = linspace(lowerLimit,upperLimit,n);
Ao = trapz(tForIntegration,resultant);

% Two parameter G(s) = k/Ts+1
T1 = Ao/k;
display("Modelo a dois parametros:");
display(T1);
display(k);


% Model 3 parameters with the area method
T2 = Ao/k - L;
display("Modelo a tres parametros:");
display(T2);
display(k);
display(L);

% Model 3 parameters with the area method
% Another approximation for the time response T (tAB 63% from the y(inf))
% 0.63*y(inf) = 0.2205, then going to the graph with ginput(1) see which
% value we have for the time
time_cte = 0.63*y_infinite;


% Uncomment to check if the two model approximation is good
%num = [14.1585];
%den = [0.2571 1];
%g2 = tf(num,den);
%step(g2*4.92);

% Uncomment to check if the three param. model approx. is good
%num = [14.1585];
%den = [0.0159 0.2571 1];
%g3 = tf(num,den);
%step(g3*4.92);


