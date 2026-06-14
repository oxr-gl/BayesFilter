function pdfval = transition(model, thetax, ~)
% Octave smoke compatibility: density matching kalman/st_process.m.
% Input ordering for full_sol is [theta; x_t; x_{t-1}].
a = .4 + .6*normcdf(thetax(1, :));
xnew = thetax(model.d+1:model.d+model.m, :);
xold = thetax(model.d+model.m+1:model.d+2*model.m, :);
var = max(1 - a.^2, realmin);
res = bsxfun(@minus, xnew, bsxfun(@times, a, xold));
quad = sum(bsxfun(@rdivide, res.^2, var), 1);
pdfval = exp(-0.5 * quad) ./ ((2*pi).^(model.m/2) .* (var.^(model.m/2)));
end
