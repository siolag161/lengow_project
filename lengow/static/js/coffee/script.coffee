'use strict'
if typeof jQuery == 'undefined'
  throw new Error(' requires jQuery')

products = {}
OrderForm = ($element) ->

  @$container = $element
  @$orderForm = $element.find('form')
  @$orderSubmit = @$orderForm.find('#submit-id-submit')
  @$orderAddButton = @$orderForm.find('#id-add-button')
  @$productHolder = $element.find('#product-holder')

  @$qtyInput = $element.find("#id_quantity")
  @$prodInput = $element.find("#id_product")

  #@$addedProducts = @$orderForm.find("id_added_products")

  @productTexts = {}

  @init()
  return

OrderForm.prototype =
  constructor: OrderForm
  init: ->
    products = {}
    that = @
    $('#id_product > option').each ->
      if !!@value
        that.productTexts[@value] = @text
    @addListener()

  addListener: ->
    that = @
    @$orderForm.on 'submit', $.proxy(@submitForm, this)
    @$orderAddButton.on 'click', $.proxy(@addProduct, this)
    return

  submitForm: ->
    if Object.keys(products).length <= 0
      e = '<div class="alert alert-danger" role="alert">'
      e = e + '<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>'
      e = e+ '<span class="sr-only">Error:</span>You have to enter at least one product</div>'
      $('#product-holder').append e
      return false
    else
      for prod, qty of products
        val = prod + "," + qty
        input = $('<input>').attr('type', 'hidden').attr('name', 'products').val(val)
        $("#create_order_form_id").append $(input)
      return true

  addProduct: ->
    qty = @$qtyInput.val()
    prod = @$prodInput.val()
    if $.isNumeric(qty) and !!prod
      products[prod] = qty

    @display()
    return

  display: ->
    @$productHolder.empty()
    for prod_key,count of products
      prod_name = @productTexts[prod_key]
      elem = "<li role='presentation'><a href='#'>#{prod_name} <span class='badge'>#{count}</span></a></li>"
      console.log elem
      @$productHolder.append elem

  clearForm: ->
    products = {}
    @$addedProducts.val {}
    @$orderForm.reset()
    return

ProductFilterForm = ($element) ->
  @$container = $element
  @$form = $element.find('form')
  @$productHolder = $element.find('#product_list_holder')
  @init()
  return

ProductFilterForm.prototype =
  constructor: ProductFilterForm
  init: ->
    @addListener()

  addListener: ->
    console.log @$form
    @$form.on 'submit', $.proxy(@submitForm, this)

  submitForm: ->
    $('#product_list_holder').html('').load(
      '/products/search',
      $('#product_search_form_id').serialize()
    )
    return false

(($) ->
  $ ->

    $form_wrapper = $('.order-create-form-wrapper')
    if $form_wrapper.length
      new OrderForm($form_wrapper)

    $product_filter_form_wrapper = $('#product_filter_wrapper')
    console.log $product_filter_form_wrapper
    if $product_filter_form_wrapper.length
      new ProductFilterForm($product_filter_form_wrapper)
) jQuery

