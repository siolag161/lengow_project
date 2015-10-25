'use strict'
if typeof jQuery == 'undefined'
  throw new Error(' requires jQuery')

OrderForm = ($element) ->


  @$container = $element
  @$orderForm = $element.find('form')
  @$orderSubmit = @$orderForm.find('#submit-id-submit')
  @$orderAddButton = @$orderForm.find('#id-add-button')
  @$productHolder = $element.find('#product-holder')

  @$qtyInput = $element.find("#id_quantity")
  @$prodInput = $element.find("#id_product")

  #@$addedProducts = @$orderForm.find("id_added_products")

  @products = {}
  @productTexts = {}

  @init()
  return

OrderForm.prototype =
  constructor: OrderForm
  init: ->
    that = @
    $('#id_product > option').each ->
      if !!@value
        that.productTexts[@value] = @text
    @addListener()

  addListener: ->
    that = @
    @$orderForm.on 'submit', (eventObj) ->
      for prod, qty of that.products
        val = prod + "," + qty
        input = $('<input>').attr('type', 'hidden').attr('name', 'products').val(val)
        $("#create_order_form_id").append $(input)
      console.log $("#create_order_form_id").serializeArray()
      true
    @$orderAddButton.on 'click', $.proxy(@addProduct, this)
    return

  submitForm: =>

    return true

  addProduct: ->
    qty = @$qtyInput.val()
    prod = @$prodInput.val()
    if $.isNumeric(qty) and !!prod

      @products[prod] = qty

    @display()
    return

  display: ->
    @$productHolder.empty()
    for prod_key,count of @products
      prod_name = @productTexts[prod_key]
      elem = "<li role='presentation'><a href='#'>#{prod_name} <span class='badge'>#{count}</span></a></li>"
      console.log elem
      @$productHolder.append elem

  clearForm: ->
    @products = {}
    @$addedProducts.val {}
    @$orderForm.reset()
    return

(($) ->
  $ ->
    $form_wrapper = $('.order-create-form-wrapper')
    if $form_wrapper.length
      new OrderForm($form_wrapper)

  $(document).ready ->

    return
) jQuery
