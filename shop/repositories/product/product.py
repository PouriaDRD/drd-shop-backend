from django.db.models import Prefetch, QuerySet

from shop.models import ProductModel, ProductPlanModel, PlanFeatureModel


class ProductRepository:
    """
    Database access layer for products.
    """

    @staticmethod
    def get_queryset() -> QuerySet[ProductModel]:
        return ProductModel.objects.filter(is_active=True)

    @staticmethod
    def get_all() -> QuerySet[ProductModel]:
        return ProductRepository.get_queryset()

    @staticmethod
    def get_by_id(product_id: str):
        return (
            ProductRepository.get_queryset()
            .filter(id=product_id)
            .prefetch_related(
                Prefetch(
                    "plans",
                    queryset=ProductPlanModel.objects.filter(
                        is_active=True
                    ).prefetch_related(
                        Prefetch(
                            "features",
                            queryset=PlanFeatureModel.objects.select_related("feature"),
                        )
                    ),
                )
            )
            .first()
        )

    @staticmethod
    def get_by_slug(slug: str):
        return (
            ProductRepository.get_queryset()
            .filter(slug=slug)
            .prefetch_related(
                Prefetch(
                    "plans",
                    queryset=ProductPlanModel.objects.filter(
                        is_active=True
                    ).prefetch_related(
                        Prefetch(
                            "features",
                            queryset=PlanFeatureModel.objects.select_related("feature"),
                        )
                    ),
                )
            )
            .first()
        )
