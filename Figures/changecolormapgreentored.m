function changecolormapgreentored
newmap = jet;                    %starting map
ncol = size(newmap,1);           %how big is it?
pos=1:length(newmap);
for i=1:size(newmap,1)
    newmap(pos(i),:) = [(i/length(newmap)) 1-i/length(newmap) 0];
end
colormap(newmap);
end