from model.autor import Autor
from database.conexao_factory import ConexaoFactory


class AutorDAO:

    def __init__(self):
        self.__autores: list[Autor] = list()
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()

    def listar(self) -> list[Autor]:
        autores = list()
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('select id,nome, email, telefone, bio from autores')
        resultados = cursor.fetchall()
        for resultado in resultados:
            aut = Autor(resultado[1], resultado[2], resultado[3], resultado[4])
            aut.id = resultado[0]
            autores.append(aut)
        cursor.close()
        conexao.close()
        return autores

    def adicionar(self, autor: Autor) -> None:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('''
            insert into autores (nome, email, telefone, bio) values (%(nome)s, %(email)s, %(telefone)s, %(bio)s)
            ''',
                       ({'nome': autor.nome, 'email': autor.email,
                        'telefone': autor.telefone, 'bio': autor.bio, })
                       )
        # 'insert into categorias (nome) values (%(nome)s, %(nome)s) ')
        conexao.commit()
        cursor.close()
        conexao.close()

    def remover(self, autor_id: int) -> bool:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('delete from autores where id=%s', (autor_id,))
        removidas = cursor.rowcount
        conexao.commit()
        cursor.close()
        conexao.close()
        if removidas == 0:
            return False
        else:
            return True

    def buscar_por_id(self, autor_id) -> Autor:
        aut = None
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            'select id, nome, email, telefone, bio from autores where id = %s', (autor_id,))
        resultado = cursor.fetchone()  # se vier só um resultado, é fetchone
        # fechall se vier uma lista
        if resultado:
            aut = Autor(resultado[1], resultado[2], resultado[3], resultado[4])
            aut.id = resultado[0]
        cursor.close()
        conexao.close()
        return aut
