from model.editora import Editora
from database.conexao_factory import ConexaoFactory


class EditoraDAO:

    def __init__(self):
        self.__editoras: list[Editora] = list()
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()

    def listar(self) -> list[Editora]:
        editoras = list()
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('select id, nome, endereco, telefone from editoras')
        resultados = cursor.fetchall()
        for resultado in resultados:
            # 1 ref. ao nome no select
            edi = Editora(resultado[1], resultado[2], resultado[3])
            edi.id = resultado[0]
            editoras.append(edi)
        cursor.close()
        conexao.close()
        return editoras

    def adicionar(self, editora: Editora) -> None:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('''
            insert into editoras (nome, endereco, telefone) values (%(nome)s, %(endereco)s, %(telefone)s)
            ''',
                       ({'nome': editora.nome, 'endereco': editora.endereco,
                        'telefone': editora.telefone, })
                       )
        # 'insert into categorias (nome) values (%(nome)s, %(nome)s) ')
        conexao.commit()
        cursor.close()
        conexao.close()

    def remover(self, editora_id: int) -> bool:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('delete from editoras where id=%s', (editora_id,))
        removidas = cursor.rowcount
        conexao.commit()
        cursor.close()
        conexao.close()
        if removidas == 0:
            return False
        else:
            return True

    def buscar_por_id(self, editora_id) -> Editora:
        edi = None
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            'select id, nome,endereco, telefone from editoras where id = %s', (editora_id,))
        resultado = cursor.fetchone()  # se vier só um resultado, é fetchone
        # fechall se vier uma lista
        if resultado:
            edi = Editora(resultado[1], resultado[2], resultado[3])
            edi.id = resultado[0]
        cursor.close()
        conexao.close()
        return edi
