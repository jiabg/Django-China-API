from django.db import models
from django.contrib.contenttypes.models import ContentType
from django_comments.abstracts import CommentAbstractModel
from mptt.models import MPTTModel, TreeForeignKey


class Reply(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey(
        'self',
        verbose_name="上级回复",
        related_name='children',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta(CommentAbstractModel.Meta):
        verbose_name = "回复"
        verbose_name_plural = "回复"

    def descendants(self):
        """
        获取回复的全部子孙回复，按回复时间正序排序
        """
        return self.get_descendants().order_by('submit_date')

    @property
    def ctype(self):
        return ContentType.objects.get_for_model(self)

    @property
    def ctype_id(self):
        return self.ctype.id
