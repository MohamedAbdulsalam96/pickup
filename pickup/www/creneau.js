
frappe.ready(function() {

	var pickup_slot = frappe.get_cookie("pickup_slot");

	$("[id='"+pickup_slot+"']").prop("disabled",true);

});

frappe.provide("erpnext.shopping_cart");
var shopping_cart = erpnext.shopping_cart;

var change_pickup_slot = function(slot, address) {

	//clear shopping cart if any
	var cart_count = frappe.get_cookie("cart_count");

	if(parseInt(cart_count) > 0) {
		if (!confirm("Votre panier sera perdu, souhaitez-vous continuer ?")) {
			return false;
		}
	}

	//reset the previous slot
	var pickup_slot = frappe.get_cookie("pickup_slot");
	//$("[id='"+pickup_slot+"']").prop('value', 'Choisir ce créneau');
	$("[id='"+pickup_slot+"']").prop("disabled",false);

	//update and set the cookie
	frappe.call({
		type: "POST",
		method: "pickup.templates.pages.cart.set_pickup_slot",
		freeze: true,
		args: {
			slot_name: slot,
			cart_count: cart_count || 0
		},
		callback: function(r) {
			if(r.message) {
				//console.log(r.message);
				$("[id='"+slot+"']").prop("disabled",true);

				//update navbar
				shopping_cart.set_cart_count();

				//redirect if category is specified
				var redirect_to = location.search.split('redirect-to=')[1]
				if (redirect_to) {
					window.location.href = redirect_to + '?creneau=' + slot;
				}
				else {
					window.location.href = '/produits?creneau=' + slot;
				}
				return false;
			}
			if(r.exc) {
				frappe.msgprint(r.exc);
			}
		}
	});
}