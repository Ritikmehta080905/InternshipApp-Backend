import graphene
from myapp import schema as myapp_schema

# Combine app-level Queries
class Query(myapp_schema.Query, graphene.ObjectType):
    """
    This combines all Queries from different apps.
    You can add project-level Queries here if needed.
    """
    pass

# Combine app-level Mutations
class Mutation(myapp_schema.Mutation, graphene.ObjectType):
    """
    This combines all Mutations from different apps.
    You can add project-level Mutations here if needed.
    """
    pass

# Create the actual GraphQL schema object for GraphQLView
schema = graphene.Schema(query=Query, mutation=Mutation)
