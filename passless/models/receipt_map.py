from passless_models import Wrapper, Receipt, Item, Vendor, Discount, Loyalty, Payment, TaxClass, Price, Fee
import dateutil
from decimal import Decimal, getcontext
import logging
_logger = logging.getLogger(__name__)

def map_receipt(receipt):
    items = []

    for orderline in receipt['orderlines']:

        price_without_tax = Decimal(orderline['price_without_tax']).quantize(Decimal('1.00'))
        price_with_tax = Decimal(orderline['price_with_tax']).quantize(Decimal('1.00'))
        price_tax = Decimal(orderline['tax']).quantize(Decimal('1.00'))
        withoutTax = (price_without_tax / ((Decimal(100)-orderline['discount']) / 100)).quantize(Decimal('1.00'))
        tax = (price_tax / ((Decimal(100)-orderline['discount']) / 100)).quantize(Decimal('1.00'))
        subtotal = Price(
            withoutTax = withoutTax, 
            withTax = withoutTax + tax,
            tax = tax
        )

        discount = Price(
            withoutTax = subtotal.withoutTax - price_without_tax,
            withTax = subtotal.withTax - price_with_tax,
            tax = subtotal.tax - price_tax
        )

        _logger.info("subtotal: " + str(subtotal.withoutTax))
        _logger.info("unitprice: " + str(subtotal.withoutTax / orderline['quantity']))
        _logger.info("quantity: " + str(orderline['quantity']))
        item = Item(
            name=orderline['product_name'],
            quantity=orderline['quantity'],
            unit=orderline['unit_name'],
            unitPrice = Price(
                withoutTax = subtotal.withoutTax / orderline['quantity'], 
                withTax = subtotal.withTax / orderline['quantity'], 
                tax = subtotal.tax / orderline['quantity'] 
            ),
            subtotal = subtotal,
            totalDiscount = discount,
            totalPrice = Price(
                withoutTax = price_without_tax, 
                withTax = price_with_tax, 
                tax = price_tax, 
            ), 
            taxClass = TaxClass(
                name = "Zero rate",
                fraction = 0
            ) if not receipt['tax_details'] else TaxClass(
                name = receipt['tax_details'][0]['tax']['name'],
                fraction = Decimal(receipt['tax_details'][0]['tax']['amount']) / 100 # TODO: This only 'works' with percentages
            ),
            shortDescription = None,
            description = orderline['product_description'] if orderline['product_description'] != False else None, # TODO: Make sure description is correct
            brand=None,
            discounts=[
                Discount(
                    name=str(orderline['discount']) + "% off",
                    deduct=discount
                )
            ] if orderline['discount'] > 0 else None
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

    result = Receipt(
        time = dateutil.parser.parse(receipt['date']['isostring']),
        currency = receipt['currency']['name'],
        subtotal=Price(
            withoutTax=sum(i.subtotal.withoutTax for i in items),
            withTax=sum(i.subtotal.withTax for i in items),
            tax=sum(i.subtotal.tax for i in items)
        ),
        totalDiscount=Price(
            withoutTax=sum(i.totalDiscount.withoutTax for i in items),
            withTax=sum(i.totalDiscount.withTax for i in items),
            tax=sum(i.totalDiscount.tax for i in items)
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

    return Wrapper(
        version="0.1.0",
        receipt=result
    )

def get_payment_method(journal):
    # TODO: Add more payment methods
    return "Cash"