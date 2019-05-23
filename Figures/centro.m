%%%%%%Calcolo centro di una nuvola%%%%%%%
%Per utilizzare questa funzione devi prima generare
%la matrice NX2 di particelle che salverai in una variabile, diciamo x.
%Richiami centro(x) e il gioco e' fatto
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function[c]=centro(x)
c=0;
n=length(x);
c=1/n*sum(x);

