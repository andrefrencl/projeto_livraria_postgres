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
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('''
            insert into categorias (nome) values (%(nome)s)
            ''',
                       ({'nome': categoria.nome, })
                       )
        # 'insert into categorias (nome) values (%(nome)s, %(nome)s) ')
        conexao.commit()
        cursor.close()
        conexao.close()

    def remover(self, categoria_id: int) -> bool:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('delete from categorias where id=%s', (categoria_id,))
        removidas = cursor.rowcount
        conexao.commit()
        cursor.close()
        conexao.close()
        if removidas == 0:
            return False
        else:
            return True

    def buscar_por_id(self, categoria_id) -> Categoria:
        cat = None
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            'select id, nome from categorias where id = %s', (categoria_id,))
        resultado = cursor.fetchone()  # se vier só um resultado, é fetchone
        # fechall se vier uma lista
        if resultado:
            cat = Categoria(resultado[1])
            cat.id = resultado[0]
        cursor.close()
        conexao.close()
        return cat
