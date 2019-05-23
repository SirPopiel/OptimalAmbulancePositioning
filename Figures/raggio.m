%%%%%%Calcolo raggio di una nuvola%%%%%%%
%
%Per utilizzare questa funzione devi prima generare
%la matrice NX2 di particelle che salverai in una variabile, diciamo x.
%Richiami diametro(x) e il gioco e' fatto
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function[best_raggio]=raggio(x)
 best_raggio=0;
n=length(x);
dd=0;
ccentro=centro(x);


for i=1:n
        dd=sqrt((x(i,1)-ccentro(1))^2+(x(i,2)-ccentro(2))^2);
         if (dd>best_raggio)
            best_raggio=dd;
        end
end
