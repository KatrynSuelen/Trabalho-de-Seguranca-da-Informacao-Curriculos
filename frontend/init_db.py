import pymysql

def setup_database():
    print("Iniciando verificação/criação do Banco de Dados...")
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='katryn',
            port=3306
        )

        with connection.cursor() as cursor:
            sql = "CREATE DATABASE IF NOT EXISTS `sistema_currículos` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            cursor.execute(sql)
            print("Banco de dados `sistema currículos` verificado/criado com sucesso!")

        connection.close()
        print("Banco de dados pronto. As tabelas são criadas pelo backend.")

    except Exception as e:
        print(f"\n[ERRO] Não foi possível configurar o banco de dados automaticamente: {e}")
        print("Certifique-se de que o serviço do MySQL está rodando na porta 3306 com a senha 'katryn'.")

if __name__ == '__main__':
    setup_database()
