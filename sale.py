# This file is part of the sale_invoice_grouping_by_address module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @property
    def _invoice_grouping_fields(self):
        res = super(Sale, self)._invoice_grouping_fields
        if self.shipment_address:
            if (self.party.sale_invoice_grouping_method ==
                    'shipment_address'):
                res = res + ('shipment_address',)
        return res

    def _get_grouped_invoice_domain(self, invoice):
        invoice_domain = super(Sale, self)._get_grouped_invoice_domain(invoice)
        if self.shipment_address:
            if (self.party.sale_invoice_grouping_method ==
                    'shipment_address'):
                if ('shipment_address', '=', None) in invoice_domain:
                    invoice_domain[
                        invoice_domain.index(('shipment_address', '=', None))
                        ] = ('shipment_address', '=', self.shipment_address)
                else:
                    invoice_domain.append(
                        ('shipment_address', '=', self.shipment_address))
        return invoice_domain

    def _get_invoice_sale(self):
        invoice = super(Sale, self)._get_invoice_sale()
        if not hasattr(invoice, 'shipment_address') and self.shipment_address:
            invoice.shipment_address = self.shipment_address
        return invoice
