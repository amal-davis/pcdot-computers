# products/translation.py
from modeltranslation.translator import translator, TranslationOptions
from .models import ProductType, Category, Product, Links

class ProductTypeTranslationOptions(TranslationOptions):
    fields = ('name',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class ProductTranslationOptions(TranslationOptions):
    fields = ('heading', 'description')

class LinksTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(ProductType, ProductTypeTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(Links, LinksTranslationOptions)
