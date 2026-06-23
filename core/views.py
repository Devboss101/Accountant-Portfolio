# core/views.py

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Experience, Skill, Project, ContactMessage
from .forms import ContactForm


def portfolio(request):

    # ── Fetch all data ───────────────────────────────────────
    profile     = Profile.objects.first()
    experiences = Experience.objects.all()
    skills      = Skill.objects.all()
    projects    = Project.objects.all()

    # ── Group skills by category ─────────────────────────────
    skill_categories = {}
    for skill in skills:
        label = skill.get_category_display()
        skill_categories.setdefault(label, []).append(skill)

    # ── Contact form ─────────────────────────────────────────
    form = ContactForm(request.POST or None)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        if form.is_valid():

            # 1. Save to database
            contact = ContactMessage.objects.create(**form.cleaned_data)

            # 2. Send email to the accountant
            try:
                send_mail(
                    subject    = f"Portfolio Contact: {contact.subject}",
                    message    = (
                        f"From:    {contact.name}\n"
                        f"Email:   {contact.email}\n\n"
                        f"{contact.message}"
                    ),
                    from_email      = settings.DEFAULT_FROM_EMAIL,
                    recipient_list  = [
                        profile.email if profile else settings.DEFAULT_FROM_EMAIL
                    ],
                    fail_silently   = False,
                )
                email_sent = True
            except Exception as e:
                # Message is still saved to DB even if email fails
                email_sent = False

            if is_ajax:
                return JsonResponse({
                    'success'   : True,
                    'email_sent': email_sent,
                    'message'   : 'Your message was sent successfully!'
                })

        else:
            # Form has errors
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'errors' : form.errors
                }, status=400)

    context = {
        'profile'          : profile,
        'experiences'      : experiences,
        'skill_categories' : skill_categories,
        'projects'         : projects,
        'form'             : form,
    }
    return render(request, 'core/portfolio.html', context)



# # core/views.py

# from django.shortcuts import render
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Profile, Experience, Skill, Project, ContactMessage
# from .forms import ContactForm


# def portfolio(request):
#     # ── fetch everything in one view ──────────────────────
#     profile     = Profile.objects.first()   # only one profile record ever
#     experiences = Experience.objects.all()  # ordered by -start_date (model Meta)
#     skills      = Skill.objects.all()       # grouped in template by category
#     projects    = Project.objects.all()     # ordered by -created_at (model Meta)

#     # ── group skills by category for the template ─────────
#     skill_categories = {}
#     for skill in skills:
#         category_label = skill.get_category_display()
#         skill_categories.setdefault(category_label, []).append(skill)

#     # ── contact form handling ─────────────────────────────
#     form = ContactForm(request.POST or None)

#     if request.method == 'POST' and form.is_valid():
#         # 1. save to DB
#         contact = ContactMessage.objects.create(**form.cleaned_data)

#         # 2. send email to the accountant
#         send_mail(
#             subject  = f"Portfolio Contact: {contact.subject}",
#             message  = f"From: {contact.name} <{contact.email}>\n\n{contact.message}",
#             from_email = settings.DEFAULT_FROM_EMAIL,
#             recipient_list = [profile.email if profile else settings.DEFAULT_FROM_EMAIL],
#             fail_silently  = True,
#         )

#         messages.success(request, "Your message was sent successfully!")
#         form = ContactForm()   # reset form after success

#     context = {
#         'profile'          : profile,
#         'experiences'      : experiences,
#         'skill_categories' : skill_categories,
#         'projects'         : projects,
#         'form'             : form,
#     }
#     return render(request, 'core/portfolio.html', context)