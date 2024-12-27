'''
    Mediante la clase Zbarra se creará un objeto matriz que contendrá las impedancias de la red.
    Esta matriz ayudará a resolver flujos de potencia y estudios de cortocircuito.

    Recibirá una lista que contendrá los nodos j, k y el valor de la impedancia en pu.
    Ejemplo: e = [[0, 1, 0.34+1.25j]]
    e[0][0] = nodo j: 0
    e[0][1] = nodo k: 1
    e[0][2] = impedancia pu: 0.34+1.25j
    
    Mediante el método construcZbus(), evaluará los casos para la construcción de la matriz Zbus.
'''
class Zbarra:
    
    def __init__(self, elementos=[]):
        self.elementos = elementos  
        self.rango = len(self.elementos)
        
    def metodoKron(self, Matris, p):
        """Aplica el método de Kron para reducir la matriz Z."""
        Mkron = []
        for j in range(len(Matris)-1):
            fila = []
            for i in range(len(Matris)-1): 
                fila.append((Matris[j][i])-(Matris[j][p-1]*Matris[p-1][i]/Matris[p-1][p-1]))
            Mkron.append(fila)  
        return Mkron

    def Caso_1(self, Z, zb):
        """Caso 1: Se agrega un nuevo nodo aislado."""
        if Z == []:
            Z = [[zb]] # Inicializa matriz Z con el nuevo elemento
        else:
            n=len(Z)-1
            for i in range(len(Z)-n):
                fila = []
                for i in range(len(Z[0])):
                    (Z[i]).append(0) # Agrega ceros para la nueva columna
                    fila.append(0) 
                Z.append(fila) # Nueva fila
            Z[-1].append(zb)
        Zn=Z  
        return Zn
    
    def Caso_2(self, Z, zb):
        """Caso 2: Se agrega un nuevo nodo conectado."""
        n=len(Z)-1
        for i in range(len(Z)-n):
            fila = []
            for i in range(len(Z[0])):
                (Z[i]).append(Z[i][-1]) # Copia la última columna
                fila.append(Z[-1][i]) 
            Z.append(fila) # Nueva fila
        Z[-1].append(zb+Z[-2][-2])
        Zn=Z
        return Zn

    def Caso_3(self, Z, zb):
        """Caso 3: Se agrega un nuevo nodo que está conectado a más de un nodo."""
        Zcaso3=self.Caso_2(Z,zb)
        return self.metodoKron(Zcaso3, len(Zcaso3))
        
    def Caso_4(self, Z, zb, j, k):
        """Caso 4: Se agrega un nuevo nodo conectado entre dos nodos existentes."""
        Zth = Z[j-1][j-1] + Z[k-1][k-1] - 2*Z[j-1][k-1]
        n=len(Z)-1
        for i in range(len(Z)-n):
            fila =  []
            for i in range(len(Z[0])):# Ajuste de las filas
                (Z[i]).append(Z[i][j-1]-Z[i][k-1])
                fila.append(Z[j-1][i]-Z[k-1][i])
            Z.append(fila)# Nueva fila
        Z[-1].append(Zth+zb)
        return self.metodoKron(Z, len(Z))
    
    def unpack(self, lista_elementos, num_lista):
        """Separa por listas independientes los datos de nodo j, nodo k, e impredancia"""
        for _ in range(len(lista_elementos)):
            lista = []
            for _ in range(len(lista_elementos)):
                lista.append(lista_elementos[_][num_lista])
        return lista
                
    def construcZbus(self):
        nodoj = self.unpack(self.elementos,0)
        nodok = self.unpack(self.elementos,1)
        elementoz = self.unpack(self.elementos,2)
        Zbarra = []
        k2 = []
        for ite in range(self.rango):
            k2.append(nodok[ite])
            # Identificar el caso y construye Zbus
            if nodoj[ite] == 0 and k2[ite] > 0 and k2.count(k2[ite]) < 2:
                Zbarra = self.Caso_1(Zbarra, elementoz[ite])
                
            elif nodoj[ite] > 0 and k2[ite] > 0 and k2.count(k2[ite]) < 2:
                Zbarra = self.Caso_2(Zbarra, elementoz[ite])
                
            elif nodoj[ite] == 0 and k2[ite] > 0 and k2.count(k2[ite]) > 1:
                Zbarra = self.Caso_3(Zbarra, elementoz[ite])
                
            elif nodoj[ite] != 0 and nodok[ite] != 0 and k2.count(k2[ite]) > 1:
                Zbarra = self.Caso_4(Zbarra, elementoz[ite], nodoj[ite], nodok[ite])
                
            else:
                print(f'Iteración elemento {ite} no efectuada')
                
        return Zbarra
    
#evaluando la clase Zbarra 

def main():
    e = [[0,1,1.25], [1,2,0.25], [2,3,.4], [0,3,1.25], [3,4,.2],[2,4,.125]]
    e1 = [[0, 1, .1+.6j],[0, 1, 1+.4j],[0, 2, .2+.5j],[2, 3, 1+.5j],[1, 3,.12+ .2j]]
    e2=[[0, 1, .0004540766+.009989685j],
        [0, 2, .001333333+.06j],
        [0, 3, 0.012+0.357j],
        [0, 5, 0.388+1.165j],
        [1, 2,  0.038857+1.16571428j],
        [2, 3, .00523809+.07333333j],
        [2, 4, .03666666+.3666666j],
        [2, 5, .006875+.11j],
        [4, 6, .555+5j],
        [4, 7, .416+2.5j]]

    z1=Zbarra(e1)
    print('matriz Zbus realizada')
    for i in z1.construcZbus():
        print(i)
if __name__=='__main__':
    main()