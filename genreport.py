import sys
import csv
import smtplib

from email.message import EmailMessage


class genReport:
    def entrypoint():
        if len(sys.argv) < 2:
            print("Error: Please enter date in dd/mm/yyyy format")
        else:
            # is_date_valid =
            try: 
                input_date = sys.argv[1].strip().split("/")
                if len(input_date) != 3:
                    raise
                input_date = "/".join(input_date).strip()
                file_data = None
                data_rows = []
                matched_rows = []
                with open("datafile.csv", 'r') as f:
                    file_data = csv.reader(f)
                    # fields = next(file_data)
                    for row in file_data:
                        data_rows.append(row)
                        if row[3] == input_date:
                            matched_rows.append(row)
                    print("matching records", matched_rows)
                if len(matched_rows):
                    # send mail
                    sender = 'sender@gmail.com'
                    receivers = ['receiver@gmail']

                    msg = EmailMessage()
                    msg['Subject'] = 'Here is the Cusips report for the requested date ' + input_date
                    msg['From'] = sender 
                    msg['To'] = receivers
                    table_rows = ''
                    for row in matched_rows:
                        table_rows += '''
                         <tr style="background-color:#eee;padding:10px 20px;">
                            <td>'''+row[0]+'''</td>
                            <td>'''+row[1]+'''</td>
                            <td>'''+row[2]+'''</td>
                            <td>'''+row[3]+'''</td>
                        </tr>
                        '''
                    msg.set_content('''
                    <!DOCTYPE html>
                    <html>
                        <body>
                            <table>
                                <thead style="background-color:red;padding:10px 20px;">
                                        <tr>
                                            <th>Company</th>
                                            <th>CUSIP</th>
                                            <th>Fund</th>
                                            <th>Date</th>
                                        </tr>
                                </thead>
                                <tbody>
                                   '''+table_rows+'''
                                </tbody>
                            </table>
                        </body>
                    </html>
                    ''', subtype='html')


                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(sender, "password string here") 
                        smtp.send_message(msg)
                        print("Email sent")
                else:
                    print("No records found for the requested date", input_date)


            except Exception as e:
                print("Error: Date must be in dd/mm/yyyy format!", e)
            pass



if __name__ == "__main__":
    genReport.entrypoint()