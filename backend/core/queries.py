import graphene_django_optimizer as gql_optimizer
from graphene_django.debug import DjangoDebug

from core.object_types import *


class Query(graphene.ObjectType):
    post = graphene.Field(PostType, id=graphene.Int())
    category = graphene.Field(CategoryType, id=graphene.Int())
    posts = graphene.List(PostType)
    categories = graphene.List(CategoryType)
    me = graphene.Field(UserType)
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_posts(self, info):
        # return Post.objects.all()
        return gql_optimizer.query(Post.objects.all(), info)

    def resolve_categories(self, info):
        # return Category.objects.all()
        return gql_optimizer.query(Category.objects.all(), info)

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            try:
                return Post.objects.get(pk=id)
                # return gql_optimizer.query(Post.objects.get(pk=id), info)
            except:
                return None

        return None

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Category.objects.prefetch_related('post_set').get(pk=id)

        return None

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user
