import smtplib
import passwords

def enviarMail(subject, message):
	try:
		import smtplib
		from email.mime.text import MIMEText
		from email.mime.multipart import MIMEMultipart

		email = 'tienda.millma@gmail.com'
		password = passwords.mail
		send_to_email = 'tienda.millma@gmail.com'  #'carolareyesr@gmail.com'
	
		msg = MIMEMultipart()
		msg['From'] = email
		msg['To'] = send_to_email
		msg['Subject'] = subject

 		# Attach the message to the MIMEMultipart object
		msg.attach(MIMEText(message, 'plain'))

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email, password)
		text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
		server.sendmail(email, send_to_email, text)
		server.quit()
		return True
	except:
		print('Something went wrong...')
		return False


if __name__ == "__main__":
	enviarMail('prueba', 'This is a message')
