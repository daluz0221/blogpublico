from django.db import models



class Ppio(models.Manager):


    def listar_post_category(self, categoria):

        return self.filter(
            category__name=categoria
        ).order_by('publish')