from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (Order, MarketPlace, Product)
from .fields import (LengowStatus)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Fieldset, MultiField
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse

from crispy_forms.bootstrap import (
    PrependedAppendedText, AppendedText, PrependedText, InlineRadios,
    Tab, TabHolder, AccordionGroup, Accordion, Alert, InlineCheckboxes,
    FieldWithButtons, StrictButton
)


class OrderFilterForm(forms.Form):
    lengow_status = forms.TypedMultipleChoiceField(required=False, choices=LengowStatus.choices(), label=_(u'Status'),
                                                   coerce=str, widget=forms.widgets.CheckboxSelectMultiple)
    marketplace = forms.ModelChoiceField(required=False, queryset=MarketPlace.objects.all(),
                                         label=_(u'Maketplace'),
                                         widget=forms.Select())

    class Meta:
        model = Order
        fields = ('marketplace', 'lengow_status',)

    def __init__(self, *args, **kwargs):
        super(OrderFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'order_filter_form'
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('lengow_status', css_class='order-status-box selectpicker'),
            Field('marketplace', css_class='order-marketplace-box selectpicker'),
            # Div(
            # Div(Field('lengow_status', css_class='order-status-box selectpicker'), css_class="col-sm-4"),
            # Div(Field('marketplace', css_class='order-marketplace-box selectpicker'), css_class="col-sm-6"),
            FormActions(Submit('submit', 'Submit', css_class='')),
            # ),
        )


import logging
logger = logging.getLogger('werkzeug')


class OrderPostForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('marketplace_status', 'lengow_status', 'marketplace',
                  'shipping_fees', 'commission_fees', 'processing_fees',
                  'currency',
                  'delivery_address',
                  )


    def __init__(self, *args, **kwargs):
        super(OrderPostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = ''
        self.helper.form_method = "POST"
        self.helper.form_action = reverse(self.view_url)
        self.helper.form_id = self.form_id
        self.helper.layout = Layout(
            Fieldset(
                '',
                'marketplace_status', 'lengow_status', 'marketplace',
                'shipping_fees', 'commission_fees', 'processing_fees',
                'currency',
                'delivery_address',
            ),

        )


class OrderCreateForm(OrderPostForm):
    view_url = 'order_create'
    form_id = "create_order_frm_id"

    product = forms.ModelChoiceField(required=True, queryset=Product.objects.all(),
                                     label=_(u'Product'),
                                     widget=forms.Select(
                                         attrs={"placeholder": "product", 'class': 'form-control input-sm'}))
    quantity = forms.IntegerField(label=_(u"Quantity"), required=True, min_value=0,
                                  widget=forms.TextInput(
                                      attrs={"placeholder": "quantity", 'class': 'form-control input-sm'}))
    products = forms.Field(required=False)

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.helper.layout.extend([
            Div(
                Div(Field('product', css_class='order-status-box selectpicker'), css_class="col-sm-7"),
                Div(Field('quantity', css_class='order-status-box selectpicker'), css_class="col-sm-3"),
                Div(StrictButton("Add", css_class="add-button", css_id="id-add-button"), css_class=""),
                css_class='row',
            ),
            FormActions(Submit('submit', 'Submit', css_class=''))
        ])



class  OrderUpdateForm(OrderPostForm):
    view_url = 'order_create'
    form_id = "create_order_frm_id"

    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.extend([
            # Div(
            #     Div(Field('product', css_class='order-status-box selectpicker'), css_class="col-sm-7"),
            #     Div(Field('quantity', css_class='order-status-box selectpicker'), css_class="col-sm-3"),
            #     Div(StrictButton("Add", css_class="add-button", css_id="id-add-button"), css_class=""),
            #     css_class='row',
            # ),
            FormActions(Submit('submit', 'Submit', css_class=''))
        ])