

import requests
import json

customers_dict = json.loads(requests.get("https://gist.githubusercontent.com/udnay/d8e2ea75f2cfd7d75482f42549c31c59/raw/60da021e9f083f0c4bf0910f690baf5f38410bc6/customers.json").text)
orders_dict = json.loads(requests.get("https://gist.githubusercontent.com/udnay/20603ff9956064c8d1f1abf7a5e6f5b2/raw/9e841b973a3d9d51940bdffe162c1400a9bac022/orders.json").text)


customers_sorted = sorted(customers_dict, key=lambda x : x['cid'])
orders_sorted = sorted(orders_dict, key=lambda x : x['customer_id'])


#inner join
def inner_join(dict_one,value_one,dict_two,value_two):

    one_sorted = sorted(dict_one, key=lambda x : x[value_one])
    two_sorted = sorted(dict_two, key=lambda x : x[value_two])
    

    one_ittr = iter(one_sorted)
    two_ittr = iter(two_sorted)

    one = next(one_ittr,None)
    two = next(two_ittr,None)

    d = "["

    while (one is not None and two is not None):
        build_item = {}

        if(one is None or two is None):
            break

        if((one is not None and two is not None) and one.get(value_one) is two.get(value_two)):
            build_item.update(two)
            build_item.update(one)
            d = d + json.dumps(build_item)
            two = next(two_ittr,None)

        if((one is not None and two is not None) and one.get(value_one) < two.get(value_two)):
            one = next(one_ittr,None)

        if((one is not None and two is not None) and one.get(value_one) > two.get(value_two)):
            two = next(two_ittr,None)



    d = d + "]"
    d = d.replace("}{","},{")
    d = d.replace("'","/""")
    return d#print(d)

# #outer join
def outer_join(dict_one,value_one,dict_two,value_two):

    one_sorted = sorted(dict_one, key=lambda x : x[value_one])
    two_sorted = sorted(dict_two, key=lambda x : x[value_two])
    

    one_ittr = iter(one_sorted)
    two_ittr = iter(two_sorted)

    one = next(one_ittr,None)
    two = next(two_ittr,None)

    prev_one = None
    prev_two = None

    d = "["

    while (one is not None and two is not None):
        build_item = {}

        if(one is None or two is None):
            break

        if((one is not None and two is not None) and one.get(value_one) is two.get(value_two)):
            build_item.update(two)
            build_item.update(one)
            d = d + json.dumps(build_item)
            prev_two = two
            two = next(two_ittr,None)

        if((one is not None and two is not None) and one.get(value_one) < two.get(value_two)):
            if((one is not None and prev_two is not None) and one.get(value_one) is not prev_two.get(value_two)):
                build_item.update(two)
                build_item.update({k : "None" for k in build_item.keys()})
                build_item.update(one)
                d = d + json.dumps(build_item)
            prev_one = one
            one = next(one_ittr,None)

        if((one is not None and two is not None) and one.get(value_one) > two.get(value_two)):
            if((prev_one is not None and two is not None) and prev_one.get(value_one) is not two.get(value_two)):
                build_item.update(one) 
                build_item.update({k : "None" for k in build_item.keys()})
                build_item.update(two)
                d = d + json.dumps(build_item)
            prev_two = two
            two = next(two_ittr,None)

        if(one is None and two is not None):
            if((prev_one is not None and two is not None) and prev_one.get(value_one) is not two.get(value_two)):
                build_item.update(prev_one) 
                build_item.update({k : "None" for k in build_item.keys()})
                build_item.update(two)
                d = d + json.dumps(build_item)
            prev_two = two
            two = next(two_ittr,None)

        if(one is not None and two_sorted is None):
            if((one is not None and prev_two is not None) and one.get(value_one) is not prev_two.get(value_two)):
                build_item.update(prev_two)
                build_item.update({k : "None" for k in build_item.keys()})
                build_item.update(one)
                d = d + json.dumps(build_item)
            prev_one = one
            one = next(one_ittr,None)



    d = d + "]"
    d = d.replace("}{","},{")
    d = d.replace("'","/""")
    return d #print(d)

print(inner_join(customers_dict,"cid",orders_dict,"customer_id"))
print(outer_join(customers_dict,"cid",orders_dict,"customer_id"))