from model.livro import Livro
from database.conexao_factory import ConexaoFactory
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO


class LivroDAO:

    def __init__(self, categoria_dao: CategoriaDAO, editora_dao: EditoraDAO, autor_dao: AutorDAO):
        self.__livros: list[Livro] = list()
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()
        self.__categoria_dao: CategoriaDAO = categoria_dao
        self.__editora_dao: EditoraDAO = editora_dao
        self.__autor_dao = AutorDAO = autor_dao

    def listar(self) -> list[Livro]:
        livros = list()
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            'select id, titulo, resumo, ano, paginas, isbn, categoria_id, autor_id, editora_id from livros')
        resultados = cursor.fetchall()
        for resultado in resultados:
            # por categoria ser um objeto, precisa tratar cada id para exibir a ref de cada id
            categoria = self.__categoria_dao.buscar_por_id(resultado[6])
            editora = self.__autor_dao.buscar_por_id(resultado[7])
            autor = self.__editora_dao.buscar_por_id(resultado[8])

            liv = Livro(resultado[1], resultado[2], int(resultado[3]), int(resultado[4]),
                        resultado[5], categoria, editora, autor)

            liv.id = resultado[0]
            livros.append(liv)
        cursor.close()
        conexao.close()
        return livros

    def adicionar(self, livro: Livro) -> None:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('''
            insert into livros (titulo, resumo, ano, paginas, isbn, categoria_id, autor_id, editora_id) 
                values (%(titulo)s, %(resumo)s, %(ano)s, %(paginas)s, %(isbn)s, 
                        %(categoria_id)s, %(autor_id)s, %(editora_id)s
                        )
            ''',
                       ({'titulo': livro.titulo, 'resumo': livro.resumo, 'ano': livro.ano,
                         'paginas': livro.paginas, 'isbn': livro.isbn,
                         'categoria_id': livro.categoria.id, 'autor_id': livro.autor.id,
                         'editora_id': livro.editora.id})
                       )

        conexao.commit()
        cursor.close()
        conexao.close()

    def remover(self, livro_id: int) -> bool:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('delete from livros where id=%s', (livro_id,))
        removidas = cursor.rowcount
        conexao.commit()
        cursor.close()
        conexao.close()
        if removidas == 0:
            return False
        else:
            return True

    def buscar_por_id(self, livro_id) -> Livro:
        liv = None
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "select id, titulo, resumo, ano, paginas, isbn, categoria_id, autor_id, editora_id "
            "from livros "
            "where id = %s", (livro_id,)
        )
        resultado = cursor.fetchone()  # se vier só um resultado, é fetchone
        # fechall se vier uma lista
        if resultado:
            categoria = self.__categoria_dao.buscar_por_id(resultado[6])
            editora = self.__autor_dao.buscar_por_id(resultado[7])
            autor = self.__editora_dao.buscar_por_id(resultado[8])

            liv = Livro(resultado[1], resultado[2], int(resultado[3]), int(resultado[4]),
                        resultado[5], categoria, editora, autor)

            liv.id = resultado[0]

        cursor.close()
        conexao.close()
        return liv
