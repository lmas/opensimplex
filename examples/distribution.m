rng('default') % default == using 0 as seed
samples = 10000000;
n2 = zeros(1, samples, 'double');
n3 = zeros(1, samples, 'double');
n4 = zeros(1, samples, 'double');

for i = 1:samples
    % Random 4D coordinate
    r = random('Uniform', -100000, 100000, [1,4]);
    % Generate noise samples
    % (make sure "opensimplex" package is installed and can be found in python PATH)
    n2(i) = py.opensimplex.noise2(r(1), r(2));
    n3(i) = py.opensimplex.noise3(r(1), r(2), r(3));
    n4(i) = py.opensimplex.noise4(r(1), r(2), r(3), r(4));
end

% Forcing the screen size of the drawn figure
set(gcf, 'Units', 'centimeters', 'Position', [0 0 20 20])
% Ensure same size on "printed paper" is the same as above
set(gcf, 'PaperPositionMode', 'auto')
tlayout = tiledlayout(3,1); % Split figure into 3 rows (1 column)
xlabel(tlayout, 'Bucket')
ylabel(tlayout, 'Count')
edges = -1:0.05:1; % Bucket edges for the histogram
adjust = [0.015 -0.015 0 0]; % Nudges position of the info box

t = nexttile();
histogram(n2, edges)
title("2D Noise")
info = {"min: "+min(n2), "max: "+max(n2), "avg: "+round(mean(n2),5)};
pos = get(t, 'Position');
annotation('textbox', 'String', info, 'Position', pos+adjust, 'FitBoxToText','on')

t = nexttile();
pos = get(t, 'Position');
histogram(n3, edges)
title("3D Noise")
info = {"min: "+min(n3),  "max: "+max(n3), "avg: "+round(mean(n3),5)};
pos = get(t, 'Position');
annotation('textbox', 'String', info, 'Position', pos+adjust, 'FitBoxToText','on')

t = nexttile();
pos = get(t, 'Position');
histogram(n4, edges)
title("4D Noise")
info = {"min: "+min(n4),  "max: "+max(n4), "avg: "+round(mean(n4), 5)};
pos = get(t, 'Position');
annotation('textbox', 'String', info, 'Position', pos+adjust, 'FitBoxToText','on')
