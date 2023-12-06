import psycopg2


class ConexaoFactory:

    def get_conexao(self):
        return psycopg2.connect(
            host='berry.db.elephantsql.com',
            database='xedwyncf',
            user='xedwyncf',
            password='F2K8OEN94CkKCk2NuJ4dppbtPDHHO6tx')
