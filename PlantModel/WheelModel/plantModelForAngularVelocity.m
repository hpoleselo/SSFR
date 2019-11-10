% Reading our filtered data
[t, w] = readNFilterData();

n = length(w);     

% Reconstruct system response w/ 30/255 from duty cycle
plot(t,w,'r')
grid on

%input vel 56 rad/s for 27% from the PWM
input = 70;                        % rad/s got from the graph from readNFilterData

% Three parameter model approximation G3(s) = e^-Ls*k/Ts+1
y_infinite = 55.29;                % Steady state value, we checked from the grph
k = y_infinite/input;
L = 0.2540 -0.1010;                % 0.153s

% Helping function to calculate the Ao, where T2 = Ao/y_inf - L
hold on
const = y_infinite*ones(1,n);      % Steady state of our system
plot(t,const,'k')

resultant = const - w;           % Area between both curves
lowerLimit = 0.1010;             % Where the curves start
% When  the system reaches the steady state
upperLimit = 0.97;               % Was chosen with ginput(1) on the graph
tForIntegration = linspace(lowerLimit,upperLimit,n);
Ao = trapz(tForIntegration,resultant);
T1 = Ao/y_infinite - L;


% Model 3 parameters without the area method
% Another approximation for the time response T (tAB 63% from the y(inf))
% 0.63*y(inf) = 0.2205, then going to the graph with ginput(1) see which
% value we have for the time
time_cte = 0.63*y_infinite;
    
T2 = 10.433 - 10.303;        % 10.433 foi pegando pelo ginput e 10.303 eh o atraso


% Another approximation for the time response T (tAC)

%num = [0.0065];
%den = [0.01599 0.253 1 0];
%g3 = tf(num,den);
%step(g3*54);