// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// shopping cart
frappe.provide("erpnext.shopping_cart");
var shopping_cart = erpnext.shopping_cart;

$.extend(shopping_cart, {
	show_shoppingcart_dropdown: function() {
		if(frappe.session.user==="Guest") {
			$('.shopping-cart-menu').html("Le panier est vide.");
		} else {
			$(".shopping-cart").on('shown.bs.dropdown', function() {
				if (!$('.shopping-cart-menu .cart-container').length) {
					return frappe.call({
						method: 'erpnext.shopping_cart.cart.get_shopping_cart_menu',
						callback: function(r) {
							if (r.message) {
								$('.shopping-cart-menu').html(r.message);
							}
						}
					});
				}
			});
		}
	},

	set_cart_count: function() {
		var cart_count = frappe.get_cookie("cart_count");
		if(frappe.session.user==="Guest") {
			cart_count = 0;
		}

		$(".shopping-cart").toggleClass('hidden', false);	// always displayed

		var $cart = $('.cart-icon');
		var $badge = $cart.find("#cart-count");

		if(parseInt(cart_count) === 0 || cart_count === undefined) {
			//$cart.css("display", "none");
			$(".cart-items").html('Cart is Empty');
			$(".cart-tax-items").hide();
			$(".btn-place-order").hide();
			$(".cart-addresses").hide();
			$(".cart-pickup").hide();
		}
		else {
			$cart.css("display", "inline");
		}

		if(parseInt(cart_count)) {
			$badge.html(cart_count);
		} else {
			$badge.html(0);
		}

		//pickup slot
		var pickup_slot = frappe.get_cookie("pickup_slot");

		var $cart = $('.cart-icon');
		var $badge = $cart.find("#pickup-slot");

		if(pickup_slot) {
			$badge.html(pickup_slot);
		} else {
			$badge.html("Choisir un créneau de retrait");
		}
	},

});
