import graphene

import djangowebapp.schema


class Query(djangowebapp.schema.GetStudents, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(djangowebapp.schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)