function PlotVecchie(x,y,ambloc)
close all;
load tempi_legge.mat;


pos_chiamata=Dati(:,VL_RIF_X:VL_RIF_Y);
pos_ambulanza=Dati(:,VL_RIF_X_STAZ:VL_RIF_Y_STAZ);
col=[0.6 0.6 0.6];
green=[0.3,1,0.1];

x_col=[1515781 1518471 1516988 1516033 1514272 1513018 1513536 1514123 1514263 1510198 1515561 1510026 1517534 1512243 1515164 1510023 1511210 1517525 ...
    1514601 1515858 1512113 1517394 1511999 1513383 1514354 1518911 1512786 1518298 1516105];
y_col=[5037044 5036807 5036948 5035677 5036464 5034846 5032339 5033310 5035032 5038512 5031519 5034419 5033043 5037079 5034501 5032664 5036224 5034333 ...
    5038243 5033206 5031521 5039088 5033199 5038154 5031109 5033761 5041701 5038308 5040220];
col_attuali=[x_col' y_col'];
ambloc=dlmread(ambloc);
for i=1:29
    KK1=find(Dati(:,TEMPO_ARRIVO_AMBULANZA)<7 & Dati(:,codice_stazionamento)==i);
    best_raggio2(i)=raggio(pos_chiamata(KK1,:));
    raggioMedio2(i)=raggio_medio(pos_chiamata(KK1,:));
    devRaggio2(i)=dev_raggio( pos_chiamata(KK1,:),raggioMedio2(i));
end
k=1;
minRaggio2=min(raggioMedio2);
halfRaggio2=minRaggio2/2;
b=1;
figure('Name','Copertura');
axis([1503000 1523000 5026000 5044000]);
axis square
title('Copertura Attuale');

u=dlmread(x);
z=zeros(493,1);
for i=1:1:493
z(i)=u(i,2);
end
k1=z;

y=dlmread(y);
z1=zeros(493,1);
for i=1:1:493
z1(i)=y(i,2);
end
k2=z1;

k=1;
cont=0;
for j=5043000:-(halfRaggio2):5027000 
    a=1;
     
    for i=1504000:halfRaggio2:1522000    
        
        ric_quad_tempi=find(Dati(:,VL_RIF_X)>=i & ...
            Dati(:,VL_RIF_X)<i+halfRaggio2 & ...
            Dati(:,VL_RIF_Y)<=j & Dati(:,VL_RIF_Y)>j-halfRaggio2);
        
        numeros(b,a)=length(ric_quad_tempi);
        rect=[i j-halfRaggio2 halfRaggio2 halfRaggio2];
        if((a==1)||(b==1))
            
         if(numeros(b,a)>0)
             cont=cont+1;
             num(b,a)=cont;
             copdop(b,a)=k1(cont);
             copsin(b,a)=k2(cont);
         

          if (copdop(b,a)==1) 
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',green);
          k=k+1;
          elseif ((copdop(b,a)==0) && (copsin(b,a)==1))
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[1 0.98 0]);
          k=k+1; 
          elseif ((copdop(b,a)==0) && (copsin(b,a)==0))
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[0.9 0.2 0]);
              hold on
          k=k+1;
          %%% OCIO QUESTO SOTTO SERVE PER TESTARE
          %elseif (copdop(b,a)==4)
                  %rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor','b','LineWidth',1 ...
                  %,'FaceColor','b');
              
          end
          
          else
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[1 1 1]); 

         end
        elseif((numeros(b,a)>0)||((numeros(b-1,a)>0)&&(numeros(b,a-1)>0)))
             cont=cont+1;
             num(b,a)=cont;
             copdop(b,a)=k1(cont);
             copsin(b,a)=k2(cont);     
          if (copdop(b,a)==1) 
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',green); 
             
          k=k+1; 
          elseif ((copdop(b,a)==0) && (copsin(b,a)==1))
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[1 0.98 0]); 
              hold on
         
          k=k+1;
          
%           %% IL CAPOLAVORO
% 
%            elseif ((copdop(b,a)==0) && (copsin(b,a)==0) && (numeros(b,a)==0))
%                   rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor','r','LineWidth',1 ...
%                   ,'FaceColor','c');
%               hold on
%           if ambloc(k,2)==1
%                   plot(i+0.5*halfRaggio2,j-0.5*halfRaggio2,'bo')
%           end    
%           k=k+1;

          
          elseif ((copdop(b,a)==0) && (copsin(b,a)==0))
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[0.9 0.2 0]); 
              hold on
          k=k+1;
          %%% OCIO QUESTO SOTTO SERVE PER TESTARE
          %elseif (copdop(b,a)==4)
                  %rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor','b','LineWidth',1 ...
                  %,'FaceColor','b');
          end
         else
                  rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[1 1 1]);  
         
        end
        if a==1 && b==20
            %%% Scusate per questo imbarazzante pezzo di codice, ma i
            %%% geniacci prima di me hanno inserito un easter egg che
            %%% inserisce tra le zone di Milano un'oasi bucolica tra
            %%% Cusago, Trezzano e Cascina Guascona. La cosa più comoda,
            %%% avendo già io terminato il lavoro, è annullare la variabile
            %%% relativa ad essa nei programmi lineari e impedire che venga
            %%% plottata qua
            rectangle('Curvature',[0 0],'Position', rect,'LineStyle', '-', 'EdgeColor',col,'LineWidth',1 ...
                  ,'FaceColor',[1 1 1]);
              hold on
        end
        a=a+1; 
    end
    b=b+1;
end
hold on
plot(col_attuali(:,1),col_attuali(:,2),'*b');
hold on


a=[1514973, 5034540];
scatter(a(1), a(2),'ko','filled')
text(a(1)+200, a(2)+200,'Duomo')

a=[1517885, 5036285];
scatter(a(1), a(2),'ko','filled')
text(a(1)+200, a(2)+200,'PoliMi')

% a=[1514602, 5036820];
% scatter(a(1), a(2),'ko','filled')
% text(a(1)+300, a(2)+300,'Garibaldi')

% a=[1517245, 5035205];
% scatter(a(1), a(2),'ko','filled')
% text(a(1)+200, a(2)+200,'Casa')


a=[1509698, 5036065];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'San Siro')

a=[1516264, 5040667];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'Bicocca')

% a=[1518749, 5031027];
% scatter(a(1), a(2),'ko','filled')
% text(a(1)+300, a(2)+300,'Rogoredo')

a=[1517540, 5031847];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'Corvetto')


% a=[1518786, 5029255];
% scatter(a(1), a(2),'ko','filled')
% text(a(1)+300, a(2)+300,'Chiaravalle')

a=[1512444, 5039122];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'Bovisa')

a=[1510691, 5040336];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'Quarto Oggiaro')

% a=[1516936, 5036986];
% scatter(a(1), a(2),'ko','filled')
% text(a(1)+300, a(2)+300,'Loreto')

a=[1516055, 5037079];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'Centrale')

a=[1511125, 5032822];
scatter(a(1), a(2),'ko','filled')
text(a(1)+300, a(2)+300,'Giambellino')
