from model.categoria import Categoria
from database.conexao_factory import ConexaoFactory


class CategoriaDAO:

    def __init__(self):
        self.__categorias: list[Categoria] = list()
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()

    def listar(self) -> list[Categoria]:
        categorias = list()
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('select id,nome from categorias')
        resultados = cursor.fetchall()
        for resultado in resultados:
            cat = Categoria(resultado[1])  # 1 ref. ao nome no select
            cat.id = resultado[0]
            categorias.append(cat)
        cursor.close()
        conexao.close()
        return categorias

    def adicionar(self, categoria: Categoria) -> None:
        self.__categorias.append(categoria)

    def remover(self, categoria_id: int) -> bool:
        encontrado = False
        for c in self.__categorias:
            if (c.id == categoria_id):
                index = self.__categorias.index(c)
                self.__categorias.pop(index)
                encontrado = True
                break
        return encontrado

    def buscar_por_id(self, categoria_id) -> Categoria:
        cat = None
        for c in self.__categorias:
            if (c.id == categoria_id):
                cat = c
                break
        return cat
