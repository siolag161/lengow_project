# -*- coding: UTF-8 -*-

from braces.views import LoginRequiredMixin
import django.views.generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from .models import (Order, CartLine, Product)
from .forms import (OrderFilterForm, OrderCreateForm, OrderUpdateForm)
from .forms import ProductSearchForm


class OrderListView(django.views.generic.ListView):
    paginate_by = 3
    context_object_name = 'orders'
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        form = OrderFilterForm(self.request.GET)
        qs = Order.objects.all()
        if form.is_valid():
            qs = self.get_filtered_queryset(qs, form)
        return qs.order_by('-purchase_date')

    @staticmethod
    def get_filtered_queryset(qs, form):  # @todo prefetch & stuff
        mk = form.cleaned_data.get('marketplace', None)
        if mk:
            qs = qs.filter(marketplace=mk)
        status = form.cleaned_data.get('lengow_status', None)
        if status:
            qs = qs.filter(lengow_status__in=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context['form'] = OrderFilterForm()
        return context


class OrderDetailView(django.views.generic.DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    slug_field = 'hashed_id'
    context_object_name = 'order'


class OrderDeleteView(LoginRequiredMixin, django.views.generic.DeleteView):
    slug_field = 'hashed_id'
    success_message = 'Deleted Successfully'
    model = Order
    success_url = reverse_lazy('order-list')
    context_object_name = 'order'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(django.views.generic.DeleteView, self) \
            .delete(request, *args, **kwargs)


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, django.views.generic.CreateView):
    model = Order
    success_message = 'New Order Created Successfully'
    success_url = reverse_lazy('order-list')
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'

    def form_valid(self, form):
        order = form.save(commit=True)
        product_params = self.request.POST.getlist('products')
        sku_qtys = self.__retrieve_product_quantity(product_params)
        skus = [sku for sku, _ in sku_qtys]
        associated_products = Product.objects.filter(pk__in=skus)
        qtys = [qty for _, qty in sku_qtys]
        cart_lines = [CartLine(order=order, product=product, quantity=qty,
                               unit_price=product.unit_price, tax_rate=product.tax_rate)
                      for (product, qty) in zip(associated_products, qtys)]
        CartLine.objects.bulk_create(cart_lines)
        order.update_values_according_to_cart()
        order.save()

        return super(OrderCreateView, self).form_valid(form)

    @classmethod
    def to_list(cls, val=None):
        """""
        :param val:
        :return: convert to list if not already one
        """""
        if val is None:
            return []
        return val if isinstance(val, list) else [val]

    def __retrieve_product_quantity(self, product_param):
        """""
        :param product_param: supposedly a list
        :return:
        """""
        product_param = self.to_list(product_param)
        sku_qtys = (pq.split(',') for pq in product_param)
        return [(sku, int(qty)) for (sku, qty) in sku_qtys]


class OrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, django.views.generic.UpdateView):
    model = Order
    success_message = 'Order Updated Successfully'
    success_url = reverse_lazy('order-list')
    form_class = OrderUpdateForm
    template_name = 'orders/order_update.html'
    slug_field = 'hashed_id'
    context_object_name = 'order'


class ProductDetailView(django.views.generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'id_lengow'



class ProductListView(django.views.generic.TemplateView):
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update(**kwargs)
        context['form'] = ProductSearchForm()
        return context
