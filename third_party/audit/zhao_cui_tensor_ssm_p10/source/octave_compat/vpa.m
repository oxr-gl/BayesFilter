function y = vpa(x, varargin)
% Minimal Octave smoke-test compatibility shim.
% The MATLAB code uses vpa for high-precision polynomial setup; the reduced
% smoke accepts ordinary double precision instead of requiring symbolic.
y = double(x);
end
