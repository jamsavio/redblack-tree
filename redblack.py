# Red Black Tree implementation in Python 2.7
# Tutorial URL: https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/

import sys

# estrutura de dados que representa um nó na árvore
class Node():
    def __init__(self, data):
        self.data = data  # armazena a chave
        self.pai = None # ponteiro para o pai
        self.esquerdo = None # ponteiro para o filho esquerdo
        self.direito = None # ponteiro para o filho direito
        self.cor = 1 # 1 . Red, 0 . Black

    def __repr__(self):
        try:
            self._pai = self.pai.data if self.pai is not None else None
            return "key:%s\npai:%s\nesquerdo:%s\ndireito:%s\ncor:%s\n" % (self.data, self._pai, self.esquerdo.data, self.direito.data, self.cor)
        except: 
            return "Nó não encontrado.\n"

# class RedBlackTree implementa as operações
class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.cor = 0
        self.TNULL.esquerdo = None
        self.TNULL.direito = None
        self.raiz = self.TNULL

    def __pre_order_helper(self, node):
        if node != self.TNULL:
            sys.stdout.write(node.data + " ")
            self.__pre_order_helper(node.esquerdo)
            self.__pre_order_helper(node.direito)

    def __in_order_helper(self, node):
        if node != self.TNULL:
            self.__in_order_helper(node.esquerdo)
            sys.stdout.write(node.data + " ")
            self.__in_order_helper(node.direito)

    def __post_order_helper(self, node):
        if node != self.TNULL:
            self.__post_order_helper(node.esquerdo)
            self.__post_order_helper(node.direito)
            sys.stdout.write(node.data + " ")

    def __search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.__search_tree_helper(node.esquerdo, key)
        return self.__search_tree_helper(node.direito, key)

    # corrigir a árvore rb modificada pela operação de exclusão
    def __fix_delete(self, x):
        while x != self.raiz and x.cor == 0:
            if x == x.pai.esquerdo:
                s = x.pai.direito
                if s.cor == 1:
                    # caso 3.1
                    s.cor = 0
                    x.pai.cor = 1
                    self.esquerda_rotacionar(x.pai)
                    print("\nRotação a esquerda:\n")
                    self.pretty_print()
                    s = x.pai.direito

                if s.esquerdo.cor == 0 and s.direito.cor == 0:
                    # caso 3.2
                    s.cor = 1
                    x = x.pai
                else:
                    if s.direito.cor == 0:
                        # caso 3.3
                        s.esquerdo.cor = 0
                        s.cor = 1
                        self.direita_rotacionar(s)
                        print("\nRotação a direita:\n")
                        self.pretty_print()
                        s = x.pai.direito

                    # caso 3.4
                    s.cor = x.pai.cor
                    x.pai.cor = 0
                    s.direito.cor = 0
                    self.esquerda_rotacionar(x.pai)
                    print("\nRotação a esquerda:\n")
                    self.pretty_print()
                    x = self.raiz
            else:
                s = x.pai.esquerdo
                if s.cor == 1:
                    # caso 3.1
                    s.cor = 0
                    x.pai.cor = 1
                    self.direita_rotacionar(x.pai)
                    print("\nRotação a direita:\n")
                    self.pretty_print()
                    s = x.pai.esquerdo

                if s.esquerdo.cor == 0 and s.direito.cor == 0:
                    # caso 3.2
                    s.cor = 1
                    x = x.pai
                else:
                    if s.esquerdo.cor == 0:
                        # caso 3.3
                        s.direito.cor = 0
                        s.cor = 1
                        self.esquerda_rotacionar(s)
                        print("\nRotação a esquerda:\n")
                        self.pretty_print()
                        s = x.pai.esquerdo 

                    # caso 3.4
                    s.cor = x.pai.cor
                    x.pai.cor = 0
                    s.esquerdo.cor = 0
                    self.direita_rotacionar(x.pai)
                    print("\nRotação a direita:\n")
                    self.pretty_print()
                    x = self.raiz
        x.cor = 0

    def __rb_transplant(self, u, v):
        if u.pai == None:
            self.raiz = v
        elif u == u.pai.esquerdo:
            u.pai.esquerdo = v
        else:
            u.pai.direito = v
        v.pai = u.pai

    def __delete_node_helper(self, node, key):
        # encontre o nó que contém a chave
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.direito
            else:
                node = node.esquerdo

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_cor = y.cor
        if z.esquerdo == self.TNULL:
            x = z.direito
            self.__rb_transplant(z, z.direito)
        elif (z.direito == self.TNULL):
            x = z.esquerdo
            self.__rb_transplant(z, z.esquerdo)
        else:
            y = self.minimum(z.direito)
            y_original_cor = y.cor
            x = y.direito
            if y.pai == z:
                x.pai = y
            else:
                self.__rb_transplant(y, y.direito)
                y.direito = z.direito
                y.direito.pai = y

            self.__rb_transplant(z, y)
            y.esquerdo = z.esquerdo
            y.esquerdo.pai = y
            y.cor = z.cor
        if y_original_cor == 0:
            self.__fix_delete(x)
    
    # corrigir a árvore rb
    def  __fix_inserir(self, k):
        while k.pai.cor == 1:
            if k.pai == k.pai.pai.direito:
                u = k.pai.pai.esquerdo # tio
                if u.cor == 1:
                    # caso 3.1
                    u.cor = 0
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    k = k.pai.pai
                else:
                    if k == k.pai.esquerdo:
                        # caso 3.2.2
                        k = k.pai
                        self.direita_rotacionar(k)
                        print("\nRotação a direita:\n")
                        self.pretty_print()
                    # caso 3.2.1
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    self.esquerda_rotacionar(k.pai.pai)
                    print("\nRotação a esquerda:\n")
                    self.pretty_print()
            else:
                u = k.pai.pai.direito # tio

                if u.cor == 1:
                    # espelho do caso 3.1
                    u.cor = 0
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    k = k.pai.pai 
                else:
                    if k == k.pai.direito:
                        # espelho do caso 3.2.2
                        k = k.pai
                        self.esquerda_rotacionar(k)
                        print("\nRotação a esquerda:\n")
                        self.pretty_print()
                    # espelho do caso 3.2.1
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    self.direita_rotacionar(k.pai.pai)
                    print("\nRotação a direita:\n")
                    self.pretty_print()
            if k == self.raiz:
                break
        self.raiz.cor = 0

    def __print_helper(self, node, indent, last):
        # imprime a estrutura da árvore na tela
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_cor = "RED" if node.cor == 1 else "BLACK"
            print(str(node.data) + "(" + s_cor + ")")
            self.__print_helper(node.esquerdo, indent, False)
            self.__print_helper(node.direito, indent, True)
    
    # Pre-Order traversal
    # Node.esquerdo Subtree.direito Subtree
    def preorder(self):
        self.__pre_order_helper(self.raiz)

    # In-Order traversal
    # esquerdo Subtree . Node . direito Subtree
    def inorder(self):
        self.__in_order_helper(self.raiz)

    # Post-Order traversal
    # esquerdo Subtree . direito Subtree . Node
    def postorder(self):
        self.__post_order_helper(self.raiz)

    # procure na árvore a key k
    # e retorne o nó correspondente
    def searchTree(self, k):
        return self.__search_tree_helper(self.raiz, k)

    # encontre o nó com a key mínima
    def minimum(self, node):
        while node.esquerdo != self.TNULL:
            node = node.esquerdo
        return node

    # encontre o nó com a key máxima
    def maximum(self, node):
        while node.direito != self.TNULL:
            node = node.direito
        return node

    # encontre o sucessor de um determinado nó
    def successor(self, x):
        # se a subárvore direita é not None,
        # o sucessor é o nó mais a esquerda na
        # subárvore direita
        if x.direito != self.TNULL:
            return self.minimum(x.direito)

        # caso contrário, é o antecessor mais baixo de x, cujo
        # filho esquerdo também é um antecessor de x.
        y = x.pai
        while y != self.TNULL and x == y.direito:
            x = y
            y = y.pai
        return y

    # encontre o antecessor de um determinado nó
    def predecessor(self,  x):
        # se a subárvore esquerda é not None,
        # o antecessor é o nó mais à direita na
        # subárvore esquerda
        if (x.esquerdo != self.TNULL):
            return self.maximum(x.esquerdo)

        y = x.pai
        while y != self.TNULL and x == y.esquerdo:
            x = y
            y = y.pai

        return y

    # gire para a esquerda no nó x
    def esquerda_rotacionar(self, x):
        y = x.direito
        x.direito = y.esquerdo
        if y.esquerdo != self.TNULL:
            y.esquerdo.pai = x

        y.pai = x.pai
        if x.pai == None:
            self.raiz = y
        elif x == x.pai.esquerdo:
            x.pai.esquerdo = y
        else:
            x.pai.direito = y
        y.esquerdo = x
        x.pai = y

    # gire para a direita no nó x
    def direita_rotacionar(self, x):
        y = x.esquerdo
        x.esquerdo = y.direito
        if y.direito != self.TNULL:
            y.direito.pai = x

        y.pai = x.pai
        if x.pai == None:
            self.raiz = y
        elif x == x.pai.direito:
            x.pai.direito = y
        else:
            x.pai.esquerdo = y
        y.direito = x
        x.pai = y

    # insira o valor na árvore em sua posição apropriada
    # e corrige a árvore
    def inserir(self, key):
        # Ordinary Binary Search inseririon
        node = Node(key)
        node.pai = None
        node.data = key
        node.esquerdo = self.TNULL
        node.direito = self.TNULL
        node.cor = 1 # novo nó deve ser vermelho

        y = None
        x = self.raiz

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.esquerdo
            else:
                x = x.direito

        # y é pai de x
        node.pai = y
        if y == None:
            self.raiz = node
        elif node.data < y.data:
            y.esquerdo = node
        else:
            y.direito = node

        # se novo nó for um nó raiz, basta retornar
        if node.pai == None:
            node.cor = 0
            return

        # se o avô é None, basta retornar
        if node.pai.pai == None:
            return

        self.pretty_print()
        # corrige a árvore
        self.__fix_inserir(node)

    def get_raiz(self):
        return self.raiz

    # exclua o nó da árvore
    def delete_node(self, data):
        self.__delete_node_helper(self.raiz, data)

    # imprime a estrutura da árvore na tela
    def pretty_print(self):
        self.__print_helper(self.raiz, "", True)

if __name__ == "__main__":
    bst = RedBlackTree()
    while True:
        resp = int(input("\n\n1-Inserir | 2-Deletar | 3-Procurar : "))
        if resp == 1:
            key = input("Valor? ")
            print("\n")
            bst.inserir(key)
            print("\nResultado final:\n")
            bst.pretty_print()
        elif resp == 2:
            key = input("Valor? ")
            print("\n")
            bst.delete_node(key)
            print("\nResultado final:\n\n")
            bst.pretty_print()
        elif resp == 3:
            key = input ("Valor? ")
            print("\n")
            print(bst.searchTree(key))