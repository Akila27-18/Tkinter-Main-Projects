def calculate_totals(items):
    for item in items:
        qty = item['quantity']
        price = item['price']
        gst = item['gst_percent']
        subtotal = qty * price
        gst_amount = subtotal * gst / 100
        total = subtotal + gst_amount
        item['subtotal'] = subtotal
        item['gst_amount'] = gst_amount
        item['total'] = total
    return items
