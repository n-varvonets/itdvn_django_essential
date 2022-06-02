import graphene
from graph_app import schema
from graph_app_two import mutations
import graphql_jwt


# поддлючение наших запов и мутаций к схеме делаются с помощью наследования
class Query(schema.Query,graphene.ObjectType):  # таким образом добавили нашу схему приложения graph_app
    pass


class Mutation(mutations.Mutation, graphene.ObjectType):

    # добавляем для возомжности аутен нашего юезра через токен(они уже готовые, которые вытягиваем из библиотек)
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()


schema_my = graphene.Schema(mutation=Mutation)  # + указать в settings GRAPHENE


