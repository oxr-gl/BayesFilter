script_dir = fileparts(mfilename('fullpath'));
audit_root = fileparts(script_dir);

addpath([audit_root, '/octave_compat']);
cd([audit_root, '/deep-tensor.dev']);
load_dir;
addpath([audit_root, '/models']);
addpath([audit_root, '/models/tensordot']);
addpath([audit_root, '/models/kalman']);

name = 'kalman';
d = 2;
m = 3;
n = 3;
T = 1;
N = 64;
rank = 4;
sqr = 1;
epd_Lag = 3;

myModel = ssmodel(name, d, m, n, T);
myModel = setup(myModel);
myModel = complete(myModel);

dom = BoundedDomain([-1, 1]);
poly = ApproxBases(Lagrange1(8), dom, d + 2*m);
opt = TTOption('tt_method', 'random', ...
    'als_tol', 1E-6, 'local_tol', 1E-3, 'max_rank', rank, ...
    'max_als', 1, 'init_rank', 2, 'kick_rank', 1);
lowopt = TTOption('tt_method', 'random', ...
    'als_tol', 1E-6, 'local_tol', 1E-3, 'max_rank', rank, ...
    'max_als', 1, 'init_rank', 2, 'kick_rank', 1);

mySolsqr = full_sol(myModel, sqr, poly, opt, lowopt, N, epd_Lag);
mySolsqr = solve(mySolsqr);
disp('P10_OCTAVE_SMOKE_DONE');
disp(mySolsqr.logmarginal_likelihood);
