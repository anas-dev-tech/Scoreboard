from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

# Define a TagCategory model to group tags
class TagCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Tag Category"
        verbose_name_plural = "Tag Categories"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_tag_category_name",
                violation_error_message="Tag category with this name already exists.")
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Convert the name to lowercase before saving to ensure case-insensitive uniqueness
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class CategorizedTag(TagBase):
    category = models.ForeignKey(TagCategory, related_name="tags", on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        constraints = [
            models.UniqueConstraint(fields=["name", "category"], name="unique_tag_name_category")
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Convert the name to lowercase before saving to ensure case-insensitive uniqueness
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


# Extend the default TaggedItem to use our CategorizedTag
class CategorizedTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(CategorizedTag, related_name="tagged_items", on_delete=models.CASCADE)
