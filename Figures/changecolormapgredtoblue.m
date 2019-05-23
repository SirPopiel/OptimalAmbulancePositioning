function changecolormapgredtoblue
newmap = jet;                    
pos=1:length(newmap);
for i=1:size(newmap,1)
    newmap(pos(i),:) = [1-i/length(newmap) 0.15 i/length(newmap)];
end
colormap(newmap);
end

%%% poi cambiare scala e cambiare funzione expcover 