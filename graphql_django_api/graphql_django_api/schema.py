import graphene
from graph_app import schema
from graph_app_two import mutations


# длючение наших запов и мутаций к схеме делаются с помощью наследования
class Query(schema.Query,graphene.ObjectType):  # таким образом добавили нашу схему приложения graph_app
    pass


class Mutation(mutations.Mutation, graphene.ObjectType):
    pass


schema_my = graphene.Schema(mutation=Mutation)  # + указать в settings GRAPHENE


