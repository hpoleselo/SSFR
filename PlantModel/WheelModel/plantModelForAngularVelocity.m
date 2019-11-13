% Reading our filtered data
[t, w] = readNFilterData();

n = length(w); 

% 4.92V ou 120 bits de 255 do pwm
input = 4.92;

% System input, used for the System Identification
t2 = t;
u = input*ones(1,n);
u(1) = 0;

% Remove points the first 5 elements from a vector
%w = w(6:end);
% Remove the last five points from the vector
%t = t(1:end-5);
plot(t,w,'r');

showTransferFunction = false;

% Three parameter model approximation G3(s) = e^-Ls*k/Ts+1
y_infinite = 69.66;                % Steady state value, we checked from the grph
k = y_infinite/input;
L = 0.2030 -0.0504;                % 0.1526s

% Helping function to calculate the Ao, the area between both curves
hold on
const = y_infinite*ones(1,n);      % Steady state of our system
plot(t,const,'k')
xlabel('Tempo (s)')
ylabel('Velocidade Angular (rad/s)')

resultant = const - w;           % Area between both curves
lowerLimit = 0.0504;             % Where the curves start
% When  the system reaches the steady state
upperLimit = 1.3028;               % Was chosen with ginput(1) on the graph
tForIntegration = linspace(lowerLimit,upperLimit,n);
Ao = trapz(tForIntegration,resultant);

% Two parameter G(s) = k/Ts+1
T1 = Ao/k;
disp("Modelo a dois parametros:");
display(T1);
display(k);

% Model 3 parameters with the area method
T2 = Ao/k - L;
disp("Modelo a tres parametros:");
display(T2);
display(k);
display(L);

% Model 3 parameters with the area method
% Another approximation for the time response T (tAB 63% from the y(inf))
% 0.63*y(inf) = 0.2205, then going to the graph with ginput(1) see which
% value we have for the time
time_cte = 0.63*y_infinite;

syms s;
% Set showTransferFunction to true if you want to check the approximation
if showTransferFunction == true
    num = [14.1585];
    den = [0.2571 1];
    g2 = tf(num,den);
    step(g2*input,'m')
    
end

% Likewise...
if showTransferFunction == true
    num = [14.1585];
    den = [0.0159 0.2571 1];
    g3 = tf(num,den);
    step(g3*input,'b');
end

% TF from the SystemIdentification

if showTransferFunction == true
     % 0 zero 2 poles
     num = [1186];
     den = [1 16.49 84.71];
     g5 = tf(num,den);
     step(g5*input,'k')
end

if showTransferFunction == true
    % 0 zero 1 pole
    num = [65.36];
    den = [1 4.656];
    g6 = tf(num,den);
    step(g6*input,'g')
end








