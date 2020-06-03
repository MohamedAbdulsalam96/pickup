// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

window.get_product_list = function() {
	$(".more-btn .btn").click(function() {
		window.get_product_list()
	});

	if(window.start==undefined) {
		throw "product list not initialized (no start)"
	}

	$.ajax({
		method: "GET",
		url: "/",
		data: {
			cmd: "pickup.templates.pages.product_search.get_product_list",
			start: window.start,
			search: window.search,
			product_group: window.product_group,
			pickup_slot: frappe.get_cookie("pickup_slot")
		},
		dataType: "json",
		success: function(data) {
			window.render_product_list(data.message || []);
		}
	})
}

window.render_product_list = function(data) {
	var table = $("#search-list .table");
	if(data.length) {
		if(!table.length)
			var table = $("<table class='table'>").appendTo("#search-list");

		$.each(data, function(i, d) {
			$(d).appendTo(table);
		});
	}
	if(data.length < 10) {
		if(!table) {
			$(".more-btn")
				.replaceWith("<div class='alert alert-warning'>{{ _("No products found.") }}</div>");
		} else {
			$(".more-btn")
				.replaceWith("<div class='text-muted'>{{ _("Nothing more to show.") }}</div>");
		}
	} else {
		$(".more-btn").toggle(true)
	}
	window.start += (data.length || 0);

	//number spinner management
	$(".product-item").on('click', '.number-spinner button', function () {

		var btn = $(this),
			input = btn.closest('.number-spinner').find('input'),
			oldValue = input.val().trim(),
			newVal = 0;

		if (btn.attr('data-dir') == 'up') {
			newVal = parseInt(oldValue) + 1;
		} else if (btn.attr('data-dir') == 'dwn')  {
			if (parseInt(oldValue) > 1) {
				newVal = parseInt(oldValue) - 1;
			}
			else {
				newVal = parseInt(oldValue);
			}
		}
		input.val(newVal);
	});

	$(".item-add-to-cart button").on("click", function() {
		frappe.provide('erpnext.shopping_cart');

		var btn = $(this),
			input = btn.closest('.number-spinner').find('input'),
			oldValue = input.val().trim(),
			newVal = 0;

		var item_code = input.attr("data-item-code");
		var newVal = input.val();

		erpnext.shopping_cart.update_cart({
			item_code: item_code,
			qty: newVal,
			callback: function(r) {
				if(!r.exc) {

				}
			},
			btn: this,
		});
	});
}
