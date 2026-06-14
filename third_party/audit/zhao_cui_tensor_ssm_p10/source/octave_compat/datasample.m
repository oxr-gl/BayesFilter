function y = datasample(data, k, varargin)
weights = [];
for i = 1:2:numel(varargin)
    key = lower(varargin{i});
    if strcmp(key, 'weights')
        weights = varargin{i+1};
    end
end
n = rows(data);
if isempty(weights)
    ind = randi(n, k, 1);
else
    w = weights(:);
    w = w ./ sum(w);
    edges = cumsum(w);
    u = rand(k, 1);
    ind = arrayfun(@(a) find(edges >= a, 1, 'first'), u);
end
y = data(ind, :);
end
