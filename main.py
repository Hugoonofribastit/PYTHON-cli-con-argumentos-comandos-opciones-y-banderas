#!/usr/bind/env python
import click
import peewee

database = peewee.MySQLDatabase('HuguitDb', user='root', passwd='', host='localhost', port=3306)

class User(peewee.Model):
    username = peewee.CharField(max_length=50, unique=True, null=True)
    password = peewee.CharField(max_length=50, unique=True, null=True)
    email = peewee.CharField(max_length=50, unique=True, null=True)
    active = peewee.BooleanField(default=True)

    class Meta:
        database = database
        db_table = 'users'
    
    def __str__(self):
        return str(self.username)
    
class Task(peewee.Model):
    title= peewee.CharField(max_length=50)
    user = peewee.ForeignKeyField(User, backref='tasks')
    
    class Meta:
            database = database
            db_table = 'tasks'

    def __str__(self):
        return str(self.title)
    
MODELS = [User, Task]    
 

@click.group()
def main():
    pass


#COMANDOS-> ACCIONES A REALIZAR
#ARGUMENTOS -> VALORES OBLIGATORIOS PARA COMANDOS
#OPCIONES -> VALORES OPCIONALES
#BANDERAS -> VALORES U OPCIONES QUE SON BOOLEANOS


@main.command()
@click.argument('username')
@click.option('--password','-p', prompt='Enter password', hide_input=True)
@click.option('--email','-e', default='hugo@ms.com')
@click.option('--active','-a', is_flag=True, default=True)
def create_user(username,password, email, active):
    user = User.create(username=username, password=password, email=email,active=active)
    if user.id:
        print('Usuario creado exitosamente')

@main.command()
@click.argument('title')
@click.argument('username')
def create_task(title, username):
    
    user = User.select().where(User.username == username).first()
    if user:
        try:
            task = Task.create(title=title, user=user)
            print('Tarea creada!')
        except Exception as e:
            print(f'Error al crear la tarea: {e}')
    else:
        print(f'Usuario {username} no encontrado')

@main.command()
@click.argument('username')
def list_tasks(username):

    user = User.select().where(User.username == username).first()
    if user:
        for task in user.tasks:
            print(task)


@main.command()
def create_tables():
    with database:
        database.create_tables(MODELS)
        print('tablas creadas')


if __name__ == '__main__':
    main()