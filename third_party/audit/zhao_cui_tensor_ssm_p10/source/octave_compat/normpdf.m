function y = normpdf(x, mu, sigma)
if nargin < 2 || isempty(mu), mu = 0; end
if nargin < 3 || isempty(sigma), sigma = 1; end
z = (x - mu) ./ sigma;
y = exp(-0.5 .* z.^2) ./ (sqrt(2*pi) .* sigma);
end
