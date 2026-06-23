# core/models.py

from django.db import models


# ─── HOME ───────────────────────────────────────────────
class Profile(models.Model):
    """The accountant's photo and bio shown on the homepage."""
    full_name   = models.CharField(max_length=200)
    tagline     = models.CharField(max_length=300, help_text="e.g. Certified Accountant | Financial Analyst")
    bio         = models.TextField()
    photo       = models.ImageField(upload_to='profile/')
    cv          = models.FileField(upload_to='cv/', blank=True, null=True, help_text="Optional downloadable CV")
    email       = models.EmailField()
    linkedin    = models.URLField(blank=True, null=True)
    twitter     = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Profile"


# ─── EXPERIENCE ─────────────────────────────────────────
class Experience(models.Model):
    company     = models.CharField(max_length=200)
    role        = models.CharField(max_length=200)
    description = models.TextField(help_text="What she did there")
    start_date  = models.DateField()
    end_date    = models.DateField(blank=True, null=True, help_text="Leave blank if current job")
    is_current  = models.BooleanField(default=False)
    company_logo = models.ImageField(upload_to='companies/', blank=True, null=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

    class Meta:
        ordering = ['-start_date']   # most recent first


# ─── SKILLS ─────────────────────────────────────────────
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('accounting', 'Accounting'),
        ('software',   'Software & Tools'),
        ('finance',    'Finance'),
        ('other',      'Other'),
    ]
    name        = models.CharField(max_length=100)
    category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='accounting')
    proficiency = models.PositiveIntegerField(
        default=80,
        help_text="Percentage 0–100, used to render a progress bar"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', '-proficiency']


# ─── PROJECTS ───────────────────────────────────────────
class Project(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack  = models.CharField(max_length=300, help_text="Comma-separated, e.g. QuickBooks, Excel, SAP")
    live_link   = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    image       = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [tag.strip() for tag in self.tech_stack.split(',') if tag.strip()]

    class Meta:
        ordering = ['-created_at']


# ─── CONTACT ────────────────────────────────────────────
class ContactMessage(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    subject    = models.CharField(max_length=300)
    message    = models.TextField()
    sent_at    = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.subject}"

    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Contact Message"