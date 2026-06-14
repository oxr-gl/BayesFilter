function y = mvnpdf(X, mu, Sigma)
if nargin < 2 || isempty(mu), mu = zeros(1, columns(X)); end
if nargin < 3 || isempty(Sigma), Sigma = eye(columns(X)); end
if iscolumn(mu), mu = mu'; end
Xc = bsxfun(@minus, X, mu);
[R, p] = chol(Sigma);
if p ~= 0
    error('mvnpdf: covariance must be positive definite');
end
Q = Xc / R;
q = sum(Q.^2, 2);
logdet = 2 * sum(log(diag(R)));
d = columns(X);
y = exp(-0.5 .* (d * log(2*pi) + logdet + q));
end
