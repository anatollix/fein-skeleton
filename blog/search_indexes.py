from haystack import indexes

from blog.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user', null=True)
    published_on = indexes.DateTimeField(model_attr='published_on')

    def get_model(self):
        return Post

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.published()
