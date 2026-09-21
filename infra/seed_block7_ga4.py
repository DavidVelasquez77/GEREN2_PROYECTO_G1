"""Instala el seguimiento GA4 y eventos de comercio electrónico en el portal."""

env = env  # noqa: F821 - proporcionado por odoo shell
website = env["website"].search([], limit=1)
measurement_id = "G-ZB34R27HPD"

tracking_js = r"""
(function () {
    if (window.__qm_ga4_loaded) { return; }
    window.__qm_ga4_loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', 'G-ZB34R27HPD', {send_page_view: true});

    function text(selector) {
        var node = document.querySelector(selector);
        return node ? (node.textContent || '').trim().replace(/\s+/g, ' ') : '';
    }
    function number(value) {
        var raw = String(value || '').replace(/[^0-9,.-]/g, '').trim();
        if (raw.indexOf(',') >= 0 && raw.indexOf('.') >= 0) {
            raw = raw.replace(/\./g, '').replace(',', '.');
        } else if (raw.indexOf(',') >= 0) {
            raw = raw.replace(',', '.');
        }
        var result = parseFloat(raw);
        return isNaN(result) ? 0 : result;
    }
    function fire(name, params) {
        params = params || {};
        params.currency = params.currency || 'GTQ';
        gtag('event', name, params);
        window.dataLayer.push({event: name, ecommerce: params});
    }
    function itemFrom(scope) {
        scope = scope || document;
        var name = text('#product_details h1, h1[itemprop="name"], .o_wsale_product_name, .oe_product_name');
        if (!name && scope !== document) {
            var n = scope.querySelector('[itemprop="name"], .o_wsale_product_name, h6, h5');
            name = n ? (n.textContent || '').trim().replace(/\s+/g, ' ') : '';
        }
        var priceNode = scope.querySelector('#product_details .oe_price .oe_currency_value, #product_details .oe_price, .oe_price .oe_currency_value, [itemprop="price"]');
        var price = priceNode ? (priceNode.getAttribute('content') || priceNode.textContent) : '';
        var idNode = scope.querySelector('input[name="product_template_id"], input[name="product_id"], [data-product-id], [data-product-template-id]');
        var id = idNode ? (idNode.value || idNode.getAttribute('data-product-id') || idNode.getAttribute('data-product-template-id')) : '';
        if (!id) { id = location.pathname.split('/').pop() || 'web-product'; }
        return {item_id: String(id), item_name: name || 'Producto QuetzalMart', price: number(price), quantity: 1};
    }
    function productView() {
        if (/\/shop\/product\//.test(location.pathname)) {
            fire('view_item', {value: itemFrom(document).price, items: [itemFrom(document)]});
        }
    }
    function checkoutView() {
        if (/\/shop\/checkout/.test(location.pathname)) {
            fire('begin_checkout', {items: []});
        }
    }
    function purchaseView() {
        if (!/\/shop\/confirmation/.test(location.pathname)) { return; }
        var body = document.body.innerText || '';
        var order = (body.match(/Orden\s+([A-Z0-9/.-]+)/i) || [])[1] || ('web-' + Date.now());
        var total = number(text('.amount_total_summary, #cart_total, .order_total, .order_total_untaxed'));
        fire('purchase', {transaction_id: order, value: total, items: []});
    }
    document.addEventListener('click', function (event) {
        var add = event.target.closest && event.target.closest('a.a-submit, button.a-submit, .js_add_cart_json, [name="add_to_cart"], form[action*="/shop/cart/update"] button');
        if (add) {
            var form = add.closest('form') || add.closest('.oe_product') || document;
            var item = itemFrom(form);
            fire('add_to_cart', {value: item.price, items: [item]});
        }
    }, true);
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { productView(); checkoutView(); purchaseView(); });
    } else {
        productView(); checkoutView(); purchaseView();
    }
}());
"""

arch = """<data inherit_id="website.layout" name="QuetzalMart GA4 tracking">
    <xpath expr="//head" position="inside">
        <script async="async" src="https://www.googletagmanager.com/gtag/js?id=G-ZB34R27HPD"></script>
        <script type="text/javascript"><![CDATA[%s]]></script>
    </xpath>
</data>""" % tracking_js

View = env["ir.ui.view"]
view = View.search([("key", "=", "qm_ga4_tracking")], limit=1)
values = {
    "name": "QuetzalMart GA4 tracking",
    "type": "qweb",
    "key": "qm_ga4_tracking",
    "arch": arch,
    "inherit_id": env.ref("website.layout").id,
    "website_id": website.id,
    "active": True,
}
if view:
    view.write(values)
else:
    View.create(values)
env.cr.commit()
print({"website": website.name, "measurement_id": measurement_id, "tracking_view": "qm_ga4_tracking"})
