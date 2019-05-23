%%%%%%Calcolo raggio di una nuvola%%%%%%%
%
%Per utilizzare questa funzione devi prima generare
%la matrice NX2 di particelle che salverai in una variabile, diciamo x.
%Richiami diametro(x) e il gioco e' fatto
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function[dev]=dev_raggio(x,raggio_medio)
dev=0;
 dd=0;
 
 n=length(x);
 
ccentro=centro(x);

dd=0;
for i=1:n
        dd=dd+(sqrt((x(i,1)-ccentro(1))^2+(x(i,2)-ccentro(2))^2)-raggio_medio)^2;  
end
dev=sqrt(dd/(n-1));