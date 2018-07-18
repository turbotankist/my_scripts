from magento import MagentoAPI

magento = MagentoAPI("192.168.1.140", 30081, "sellbery", "1233455")
#magento = MagentoAPI("www.shirtee.de", 443, "feeds", "1234567890",proto='https')

#magento.help() # Prints out all resources discovered and available.
# cart: create, info, license, order, totals
# cart_coupon: add, remove
# ... (a bunch of other resources)
# sales_order: addComment, cancel, hold, info, list, unhold
#print  ("\nmagento.sales_order.help() \n")
#magento.sales_order.help() # 'sales_order' is a resource.
# sales_order: Order API
#   - addComment: Add comment to order
#   - cancel: Cancel order
#   - hold: Hold order
#   - info: Retrieve order information
#   - list: Retrieve list of orders by filters
#   - unhold: Unhold order
#magento.info

# Let's list sales and add their subtotals!
print ("let's start \n")
products = magento.catalog_product.list(1) #[1,3]#
print(products)
#orders = magento.sales_order.list(1)
#subtotals = [order["subtotal"] for order in orders]
#revenue = sum(subtotals)

# Additionally, you can get API metadata from these calls:
#json_description_of_resources = magento.resources()
#json_description_of_possible_global_exceptions = magento.global_faults()
#json_description_of_possible_resource_exceptions = magento.resource_faults("sales_order")


# print(magento.catalog_product.list(0) , "\n")
# print(magento.cataloginventory_stock_item.list(1))

inventory=[0]
a=0
b=len(products)
for product in products:
	#new = (magento.catalog_product.info(product['product_id']) )
	#print magento.cataloginventory_stock_item.list(product['product_id'])
	a +=1
	#print (new)
	inventory.append(product['product_id'])
	print(magento.catalog_product.info(product['product_id']) , "\n %s from %s" % (a,b))
	if a == 100: 
		break
print(magento.cataloginventory_stock_item.list(inventory))
#
#print magento.product_attribute.list(1)

#for i in range(a):
	