function p = normcdf(x, mu, sigma)
if nargin < 2 || isempty(mu), mu = 0; end
if nargin < 3 || isempty(sigma), sigma = 1; end
p = 0.5 .* erfc(-(x - mu) ./ (sigma .* sqrt(2)));
end
