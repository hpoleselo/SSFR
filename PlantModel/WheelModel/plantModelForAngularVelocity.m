% Reading our filtered data
[t, phi1] = readAndFilterData();

n = length(phi1);     

% Reconstruct system response w/ 30/255 from duty cycle
plot(t,phi1,'r')
grid on

% Three parameter model approximation G3(s) = e^-Ls*k/Ts+1
%y_infinite = 0.35;          % Steady state value, we checked from the grph
%k = y_infinite/54;           % 0.0065, 54 is the input velocity of the wheel
L = 10.303-10.180;           % 0.123s

% Helping function to calculate the Ao, where T2 = Ao/y_inf - L
%hold on
%const = 0.35*ones(1,n);      % Steady state of our system
%plot(t,const,'k')


%resultant = const - omega;   % Area between both curves
lowerLimit = 10.180;         % Where the curves start
upperLimit = 10.9506;        % Was chosen with ginput(1) on the graph
%tForIntegration = linspace(lowerLimit,upperLimit,n);
%Ao = trapz(tForIntegration,resultant);
%T1 = Ao/y_infinite - L; % checar area, depois q mudei a escala de t, mudou

% Another approximation for the time response T (tAB 63% from the y(inf))
% 0.63*y(inf) = 0.2205, then going to the graph with ginput(1) see which
% value we have for the time
T2 = 10.433 - 10.303;        % 10.433 foi pegando pelo ginput e 10.303 eh o atraso


% Another approximation for the time response T (tAC)

%num = [0.0065];
%den = [0.01599 0.253 1 0];
%g3 = tf(num,den);
%step(g3*54);