from passless_models import Receipt, Item, Vendor, Discount, Loyalty, Payment, TaxClass, Price, Fee
import dateutil
def map_receipt(receipt):
    items = []
    for orderline in receipt['orderlines']:
        item = Item(
            name=orderline['product_name'],
            quantity=orderline['quantity'],
            unit=orderline['unit_name'],
            unitPrice = Price(
                withoutTax = orderline['price_without_tax'], # TODO: Validate this is the unit price
                withTax = orderline['price_with_tax'], # TODO: Validate this is the unit price
                tax = orderline['tax'] # TODO: Validate this is tax per unit
            ),
            subtotal = Price(
                withoutTax = orderline['price_without_tax'] * orderline['quantity'], # TODO: Validate calculation
                withTax = orderline['price_with_tax'] * orderline['quantity'], # TODO: Validate calculation
                tax = orderline['tax'] * orderline['quantity'], # TODO: Validate calculation
            ),
            totalDiscount = Price(
                withoutTax = 0,
                withTax = 0,
                tax = 0
            ), # TODO: Include discounts
            totalPrice = Price(
                withoutTax = orderline['price_without_tax'] * orderline['quantity'], # TODO: Validate calculation
                withTax = orderline['price_with_tax'] * orderline['quantity'], # TODO: Validate calculation
                tax = orderline['tax'] * orderline['quantity'], # TODO: Validate calculation
            ), # TODO: Make sure this price is correct
            taxClass = TaxClass(
                name = "Zero rate",
                fraction = 0
            ), # TODO: Include actual tax rate
            shortDescription = None,
            description = orderline['product_description'] if orderline['product_description'] != False else None,
            brand=None, # TODO: Determine whether brand is none
            discounts=[
                Discount(
                    name="",
                    deduct=orderline['discount'] # TODO: Verify discount is no complex object
                )
            ] if orderline['discount'] > 0 else None # TODO: Make sure positive/negative is correct
        )
        items.append(item)
    
    # TODO: Include loyalty

    payments = []
    for paymentline in receipt['paymentlines']:
        payment = Payment(
            method=get_payment_method(paymentline['journal']),
            amount=paymentline['amount'],
            meta=None
        )
        payments.append(payment)
    
    company = receipt['company']
    vendor = Vendor(
        name=company['name'],
        address=company['contact_address'],
        phone=company['phone'],
        vatNumber=company['vat_label'] if company['vat'] else "",
        kvkNumber=company['company_registry'] if company['company_registry'] != False else "",
        logo=company['logo'],
        email=company['email'],
        web=company['website'],
        meta={
            "cashier": receipt['cashier']
        }
    )

    return Receipt(
        time = dateutil.parser.parse(receipt['date']['isoString']),
        currency = receipt['currency']['name'],
        subtotal=Price(
            withoutTax=receipt['total_without_tax'],
            withTax=receipt['total_with_tax'],
            tax=receipt['total_tax'] 
        ),
        totalDiscount=Price(
            withoutTax=0,
            withTax=0,
            tax=0
        ),
        totalPrice=Price(
            withoutTax=receipt['total_without_tax'],
            withTax=receipt['total_with_tax'],
            tax=receipt['total_tax'] 
        ),
        totalFee=Price(
            withoutTax=0,
            withTax=0,
            tax=0 
        ),
        totalPaid=receipt['total_paid'],
        items=items,
        payments=payments,
        vendor=vendor,
        vendorReference=receipt['name'],
        fees=None,
        loyalties=None
    )

def get_payment_method(journal):
    return "Cash"