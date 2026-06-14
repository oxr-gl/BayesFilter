function rng(seed)
if nargin == 0
    seed = 'shuffle';
end
if ischar(seed) && strcmp(seed, 'shuffle')
    seed = mod(round(1e6 * rem(now, 1)), 2^31 - 1);
end
rand('seed', seed);
randn('seed', seed);
end
