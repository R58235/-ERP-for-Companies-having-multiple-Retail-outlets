from .models import Invoice,Shop,Account,Hsn,Payment,PaymentMethod,FinanceCompany,Product

from reportlab.pdfgen import canvas
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Line,Drawing,colors

def invoicePdf(invoice):
    
    shop=invoice.shop
    account= invoice.account
    finance=invoice.finance
    
     # ////////////////////Company Data///////////
    companyName= "MY CHOICE"
    companyAddress= 'Address: '+shop.address+','+shop.city+','+shop.state
    companyOnlineContact= "Website: "+shop.website+", Email: "+shop.email
    companyOfflineContact= "Phone No: "+shop.phone_no1+", "+shop.phone_no2
    companyGstno= "GST No: "+shop.GST_no
        
    customerName= "Name: "+account.name
    customerAddress= "Address: "+account.address+","+account.city+","+account.state
    customerPhoneNo= "Phone No: "+account.phone_no
        
    product_list= Product.objects.filter(invoice=invoice)
    payment_list= Payment.objects.filter(invoice=invoice)
        
    buffer = io.BytesIO()
    invPdf = SimpleDocTemplate(buffer,pagesize=letter,topMargin=0.5*inch,bottomMargin=0.5*inch,leftMargin=0.5*inch,rightMargin=0.5*inch)
    width, height = letter
    width-=1*inch
    height-=1*inch
    pdf=[]
    # ////////////Header///////////
    header=[[companyName],[companyAddress],[companyOnlineContact],[companyOfflineContact],[companyGstno]]
    headerTable=Table(header,1*[width])
    headerTable.setStyle(TableStyle([('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                                         ('FONTSIZE',(0,0),(0,0),15),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    pdf.append(headerTable)
    # /////////////////Customer header///////////
    body=[["Tax Invoice"],["--Billed To--"],[customerName],[customerAddress],[customerPhoneNo]]
    bodyTable=Table(body,1*[width])
    bodyTable.setStyle(TableStyle([('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
                                       ('FONTSIZE',(0,0),(0,0),15),
                                       ('FONTNAME', (0,1), (0,1), 'Courier'),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    pdf.append(bodyTable)
    # ////////////////////Product Details////////////
    productData=[["Product Details:","","","","",""],["Sl.no","Product Name","Hsn Code","Qty","Price","Taxable value"]]
    i=1
    for product in product_list:
        data=[i,Paragraph(product.name),product.hsn.code,product.qty,product.price,product.taxable_value]
        productData.append(data)
        i+=1
    data=[i,"Total","",invoice.total_qty,"",invoice.taxable_amount]
    productData.append(data)
        
    productDataTable=Table(productData,[width*1/18,width*6/18,width*3/18,width*1/18,width*3/18,width*4/18],[0.35*inch]+[None]*(len(productData)-1))
    productDataTable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,0),15),
                        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('SPAN',(0,0),(-1,0)),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    pdf.append(productDataTable)
    # /////////Payment Detail//////////
    paymentBody=[["Payment Details:",""],["Payment Method","Amount"],["Finance",invoice.financeDisbursement]]
        
    for payment in payment_list:
        data=[payment.paymentMethod.paymentMethod,payment.amount]
        paymentBody.append(data)
           
    data=["Total Payment",(invoice.total_amount-invoice.due)]
    paymentBody.append(data)
        
    PaymentbodyTable=Table(paymentBody,[width*3/8,width*1/8],[0.35*inch]+[None]*(len(paymentBody)-1),hAlign='LEFT',vAlign='TOP')
    PaymentbodyTable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,0),15),
                        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('SPAN',(0,0),(-1,0)),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
        # pdf.append(PaymentbodyTable)
        # ///////////////Grand Total/////
    grandTotal=[["Grand Total:",""],["Particulars","Amount"],["Taxable Value:",invoice.taxable_amount],["CGST",invoice.cgst],["SGST",invoice.sgst],["IGST",invoice.igst],["Grand Total:",invoice.total_amount],["Due:",invoice.due]]
        
    grandTotalTable=Table(grandTotal,[width*3/8,width*1/8],[0.35*inch]+[None]*(len(grandTotal)-1),hAlign='RIGHT',vAlign='TOP')
    grandTotalTable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,0),15),
                        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                        ('FONTNAME', (-1,-1), (-1,-2), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('SPAN',(0,0),(-1,0)),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
        
    t = [[PaymentbodyTable,grandTotalTable]]
    temp = Table(t)
    pdf.append(temp)
    # ////////////Finance Detail/////////
    financeBody=[["Finance Details:",""],["Particulars:",""],["Company Name",finance.name],["EMI:",invoice.emi],["Downpayment:",invoice.downpayment]]

    financebodyTable=Table(financeBody,[width*3/8,width*1/8],[0.35*inch]+[None]*(len(financeBody)-1),hAlign='LEFT',vAlign='TOP')
    financebodyTable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,0),15),
                        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('SPAN',(0,0),(-1,0)),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    # ///////////////Remark///////
    remark= [["Remark:"],[Paragraph(invoice.remark)]]

        
    remarkTable=Table(remark,[width*1/2],[0.35*inch]+[1*inch],hAlign='LEFT',vAlign='TOP')
    remarkTable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,0),15),
                        ('FONTSIZE',(0,1),(-1,-1),10),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('SPAN',(0,0),(-1,0)),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    t = [[financebodyTable,remarkTable]]
    temp = Table(t)
    pdf.append(temp)
        # //////////////Footer///////
    footer= [["Reciever's Name:","For My Choice"],["",""],["Signature:","Authorised Signatory"],["--All Disputes are subject to Jamshedpur Jurisdiction--"]]

        
    footerTable=Table(footer,[width*1/2,width*1/2])
    footerTable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,-1),10),
                        ('ALIGN',(0,0),(0,0),'LEFT'),
                        ('ALIGN',(0,-2),(0,-2),'LEFT'),
                        ('ALIGN',(-1,0),(-1,0),'RIGHT'),
                        ('ALIGN',(-1,-2),(-1,-2),'RIGHT'),
                        ('FONTNAME', (0,-1), (0,-1), 'Courier'),
                        ('ALIGN',(0,-1),(0,-1),'CENTRE'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('SPAN',(0,-1),(-1,-1)),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    pdf.append(footerTable)
    invPdf.build(pdf)
    buffer.seek(0)
    filename=shop.shop_code+"-"+account.name+"-"+str(invoice.invoice_no)+".pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)