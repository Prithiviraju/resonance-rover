% Resonance Rover: Acoustic TDR & Geophone Array Simulation
% Team: Aura Nodes | Mahendra College of Engineering
% Evaluates subsurface resonance frequencies from MEMS geophone data

fs = 16000; % Sampling frequency (Hz)
t = 0:1/fs:2-1/fs; % 2-second time vector
f_resonance = 310; % Simulated void resonance (Hz)

% Generate simulated ground vibration with white noise
geophone_raw = 0.5*sin(2*pi*f_resonance*t) + 1.2*randn(size(t));

% Apply 6th-order Butterworth Bandpass Filter (20 Hz - 4000 Hz)
[b, a] = butter(6, [20 4000]/(fs/2), 'bandpass');
filtered_signal = filter(b, a, geophone_raw);

% Perform Fast Fourier Transform (FFT)
N = length(filtered_signal);
Y = fft(filtered_signal);
P2 = abs(Y/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(0:(N/2))/N;

% Anomaly Detection Thresholding
[max_amp, max_idx] = max(P1);
detected_freq = f(max_idx);

if detected_freq > 100 && detected_freq < 800 && max_amp > 0.1
    disp(['VICTIM / VOID ANOMALY DETECTED AT: ', num2str(detected_freq), ' Hz']);
else
    disp('STRUCTURE CLEAR.');
end