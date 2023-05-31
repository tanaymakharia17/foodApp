import datetime
import simplejson as json


def generate_order_number(pk):
    now = datetime.datetime.now()
    return 'ORD-' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(pk)




def order_total_by_vendor(order, vendor):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor))
    subtotal = 0
    tax = 0
    tax_dict = {}
            
            
    for key, val in data.items():
        subtotal += float(key)
        val = val.replace("'", '"')
        val = json.loads(val)
        tax_dict.update(val)

        # calculate tax
        # {'CGST': {'9.00': '6.03'}, 'SGST': {'7.00': '4.69'}}
        for i in val:
            for j in val[i]:
                tax += float(val[i][j])
    grand_total = float(subtotal) + float(tax)
    context = {
        'subtotal': subtotal,
        'tax_dict': tax_dict, 
        'grand_total': grand_total,
    }

    return context