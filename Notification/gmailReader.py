import imaplib, email
import config

user = 'your_email'
password = 'your_password'
imap_url = 'imap.gmail.com'
#Where you want your attachments to be saved (ensure this directory exists)
##attachment_dir = 'your_attachment_dir'

def auth(user,password,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user,password)
    return con

def searchBySenderOn(date, senderAddress):
    con = auth(config.EMAIL_ADDRESS, config.PASSWORD, imap_url)
    con.select('INBOX')
    _, data = con.uid('search', None, '(SINCE "{}" FROM "{}")'.format(date,senderAddress))
    return data,con

def searchBySubjectOn(date,subject):
    con = auth(config.EMAIL_ADDRESS, config.PASSWORD, imap_url)
    con.select('INBOX')
    _, data = con.uid('search', None, '(SINCE "{}" SUBJECT "{}")'.format(date, subject))
    return data,con

def getbody(data,con):
    body = []
    for num in data[0].split():
        result, data = con.uid('fetch', num, '(RFC822)')
        textbody = data[0][1]
        raw_email_string = textbody.decode('utf-8')
        mesage_matrix = email.message_from_string(raw_email_string)
        for part in mesage_matrix.walk():
            if part.get_content_type() == "text/plain":
                body.append(part.get_payload(decode=True))

    return body


def main():
    d,c = searchBySubjectOn("10-Jan-2019", "HKWZ35")
    x = getbody(d,c)[0].decode("utf-8")
    print(x)
    print(str(x.split("\r\n")))
    """if "" in x:
        print("good")"""


if __name__ == '__main__':
    main()
