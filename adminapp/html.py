from email_templates.models import *
from settings.models import *
from .models import *


def Html(EMAIL_CONTENT,COPYRIGHT_TEXT):
    maincontaint = '''
            <p style="font-style: italic;color:grey;">Hi {},<br><br> Please use the below link to reset your referral site password.
              <br><br>
                <a href="{}"><button type="button" style="box-shadow: 0px 0px 8px 0px #bababa;width: 200px;height: 50px;margin: 0px 0px 0px 200px;background-color: #1C0955;border: 0px;color: white;">Reset My Password</button></a><br>
                <br>In case you did not request for password reset, please ignore this email.<br><br><br>
                  Thanks<br><br>
                  {}
              </p>

    '''.format(EMAIL_CONTENT["username"],EMAIL_CONTENT["rmpurl"],EMAIL_CONTENT['fromname'])

    footer = '''
                <div>
                 <hr>
                ##SOCIAL_ICONS##
              </div>
    '''

    COPYRIGHT = '''<strong>Copyright &copy; {} Admin LTE .</strong>
                    All rights reserved.'''.format(COPYRIGHT_TEXT["year"])


    mainemaillayoyt = MainEmailLayoutModel.objects.get()
    html = str(mainemaillayoyt.layout_html)
    html = html.replace("##BASE_URL##", "http://192.168.5.80/dashboard/", 1)
    if LogoFavIconsModel.objects.filter(slug='MAIN_LOGO').exists():
        mainlogo = LogoFavIconsModel.objects.get(slug='MAIN_FAVICON')
        html = html.replace('##SYSTEM_LOGO##',"http://192.168.5.80/{}/".format(mainlogo.config_value_file.url),1)
    else:
        html = html.replace('##SYSTEM_LOGO##', "", 1)
    html = html.replace("##EMAIL_CONTENT##", maincontaint, 1)
    sl = ''
    if SocialLinksmodel.objects.filter().exists():
        allsociallink = SocialLinksmodel.objects.all()

        for i in allsociallink:
            if not sl:
                sl += '''<a href="{}"><i class="{}" style="font-size:40px;color:grey;margin: 8px 0px 0px 220px;"></i></a>'''.format(i.url,i.iconclass)
            else:
                sl += '''<a href="{}"><i class="{}" style="font-size:40px;color:grey;margin: 8px 0px 0px 10px;"></i></a>'''.format(i.url,i.iconclass)
        footer = footer.replace("##SOCIAL_ICONS##",sl,1)
        html = html.replace("##EMAIL_FOOTER##", footer, 1)
    else:
        html = html.replace("##EMAIL_FOOTER##", "", 1)
    html = html.replace("##COPYRIGHT_TEXT##", COPYRIGHT, 1)
    return html

