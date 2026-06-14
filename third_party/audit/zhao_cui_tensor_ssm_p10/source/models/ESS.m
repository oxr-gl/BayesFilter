function ess = ESS(w)
    w = w(:);
    w = w(~isnan(w));
    ess = sum(w)^2/sum(w.^2);
end
